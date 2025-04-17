# Natural Language Processing (NLP) for Pilot Speech

## Overview

This folder contains all training and evaluation code related to the NLP models described in Chapter 7 of the thesis. The two key tasks include:

1. Request Classification – Identifying pilot intent (e.g. taxi, takeoff, pushback, landing)
2. Flight Entity Extraction – Determining which aircraft sent the request from a list of candidates

These components work together to simulate pilot-controller communication in an automated air traffic control system.

## Directory Structure

-   `process_dataset.ipynb` – Preprocessing and augmentation pipeline for the NLP dataset
-   `train_classification.ipynb` – Fine-tuning of the BERT-based intent classification model
-   `fuzzy_extraction.ipynb` – Baseline Levenshtein distance approach for entity matching
-   `train_extraction.ipynb` – Final DistilBERT-based ranking model for flight entity recognition
-   `request_analysis.py` – Python script that runs the full practical experiment (as in Section 7.6 of the thesis)
-   `data/` – Contains the full NLP dataset including request texts and labels
-   `utils/` – Helper scripts such as homophone and rhyme generation

## Classifier Model Files

Due to Git storage constraints, the `bert_request_classifier` folder (required to run `request_analysis.py`) was compressed and split into five parts:

    bert_classifier_part_aa
    bert_classifier_part_ab
    bert_classifier_part_ac
    bert_classifier_part_ad
    bert_classifier_part_ae

## Setup Instructions

1. **Reconstruct the Classifier Folder**
   
   To extract the bert_request_classifier directory from the split files, run the following command from within this folder:
    ```bash
    cat bert_classifier_part_* > bert_request_classifier.zip
    unzip bert_request_classifier.zip
    ```

    This will generate a folder named `bert_request_classifier/` containing the pretrained BERT model required for classification.

    > [!NOTE]
    > Ensure all five parts are present before running the cat command.

2. **Install Required Libraries**

    The code requires several Python libraries. To install them, run the following command:

     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Practical NLP Experiment**

    Once the model folder is reconstructed and libraries installed, you can run the `request_analysis.py` script to perform the full classification and entity extraction experiment:

    ```bash
    python request_analysis.py
    ```

    This script simulates the evaluation procedure described in Section 7.6 of the thesis with request classification, and candidate ranking.

    > [!NOTE]
    > You will require some transcription software such as MacBook's Built-in dictation to transcribe speech.