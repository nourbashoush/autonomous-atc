import requests

rhyme_cache = {}


def get_rhymes(word, max_results=3):
    if word in rhyme_cache:
        return rhyme_cache[word]

    url = f"https://api.datamuse.com/words?rel_rhy={word}&max={max_results}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        rhymes = [item["word"] for item in data]
        rhyme_cache[word] = rhymes
        return rhymes

    except requests.exceptions.RequestException as e:
        print(f"Error fetching rhymes for '{word}': {e}")
        return []


if __name__ == "__main__":
    word = "clearance"
    rhyming_words = get_rhymes(word)
    print(rhyming_words)
