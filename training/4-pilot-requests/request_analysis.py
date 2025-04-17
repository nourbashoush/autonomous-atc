import torch
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
)
from torch.nn.functional import softmax
from utils.flights import generate_flights
from utils.requests import generate_request
from utils.digit_text_conversion import convert_digits_to_words

# --- Config ---
NUM_PLANES = 10
NUM_REQUESTS = 5

LABELS = ["Pushback", "Taxi", "Takeoff", "Landing"]
LABEL_TO_INDEX = {label: idx for idx, label in enumerate(LABELS)}

def bold(text):
    return f"\033[1m{text}\033[0m"

# --- Load flight extraction model ---
flight_model_path = "bert_flight_ranking"
flight_tokenizer = DistilBertTokenizer.from_pretrained(flight_model_path)
flight_model = DistilBertForSequenceClassification.from_pretrained(flight_model_path)
flight_model.eval()
flight_model.to(torch.device("cpu"))

# --- Load request classification model ---
classifier_model_path = "bert_request_classifier"
request_tokenizer = BertTokenizer.from_pretrained(classifier_model_path)
classifier = BertForSequenceClassification.from_pretrained(classifier_model_path)
classifier.eval()
classifier.to(torch.device("cpu"))

# --- Collect requests ---
requests = []

for _ in range(NUM_REQUESTS):
    flights = generate_flights(NUM_PLANES)
    template_text, correct_flight, correct_type, candidates = generate_request(flights)

    print(f"\nPlease read this aloud: {bold(template_text)}")
    raw_input = str(input("Transcribed speech: ")).strip()
    user_input = convert_digits_to_words(raw_input)

    requests.append((user_input, correct_flight, correct_type, candidates))


# --- Flight Extraction using BERT ranking model ---
def infer_flight(request, candidates):
    input_texts = [f"{request} [SEP] {candidate}" for candidate in candidates]
    encodings = flight_tokenizer(
        input_texts, padding=True, truncation=True, return_tensors="pt"
    ).to(flight_model.device)

    with torch.no_grad():
        outputs = flight_model(**encodings)

    scores = outputs.logits.squeeze().tolist()
    if isinstance(scores, float):  # Handle single candidate case
        scores = [scores]

    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return ranked


# --- Request Classification ---
def classify_request(text):
    inputs = request_tokenizer(
        text, return_tensors="pt", truncation=True, padding=True
    ).to(classifier.device)
    with torch.no_grad():
        outputs = classifier(**inputs)
        probs = softmax(outputs.logits, dim=1).squeeze()
    predicted_idx = torch.argmax(probs).item()
    return predicted_idx, probs


# --- Run the pipeline ---
print("\nRunning extraction and classification...\n")

for idx, (spoken_text, expected_flight, expected_type, candidates) in enumerate(
    requests, 1
):
    print(f"--- Request {idx} ---")
    print(f"Spoken Input:      {spoken_text}")

    # Flight extraction
    ranked_flights = infer_flight(spoken_text, candidates)
    predicted_flight = ranked_flights[0][0]

    # Request classification
    predicted_label_idx, label_probs = classify_request(spoken_text)
    expected_label_idx = expected_type
    predicted_label = LABELS[predicted_label_idx]

    # Print results
    print(f"Extracted Flight:  {predicted_flight}")
    print(f"Predicted Type:    {predicted_label}")
    print(f"Expected Flight:   {expected_flight}")
    print(f"Expected Type:     {LABELS[expected_label_idx]}")

    # Flight misclassification analysis
    if predicted_flight != expected_flight:
        print(f"Incorrect Flight — full ranking:")
        for i, (flight, score) in enumerate(ranked_flights):
            print(f"   #{i+1}: {flight} ({score:.4f})")
            if flight == expected_flight:
                break

    # Request type misclassification analysis
    if predicted_label_idx != expected_label_idx:
        sorted_indices = torch.argsort(label_probs, descending=True)
        rank = (sorted_indices == expected_label_idx).nonzero(as_tuple=True)[
            0
        ].item() + 1
        print(
            f"Misclassified Type — true label ranked #{rank} with confidence {label_probs[expected_label_idx]:.4f}"
        )
        print(f"🔍 Top predictions up to rank {rank}:")
        for i in range(rank):
            label_idx = sorted_indices[i].item()
            label_name = LABELS[label_idx]
            confidence = label_probs[label_idx].item()
            print(f"   #{i+1}: {label_name} ({confidence:.4f})")

    print("")
