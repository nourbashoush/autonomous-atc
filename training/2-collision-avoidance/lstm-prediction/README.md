# LSTM Conflict Prediction

## Overview

This folder contains the training code for the LSTM-based model developed to predict future aircraft positions and support collision avoidance and conflict management, as described in Chapter 5.3 of the thesis.

The LSTM model was trained on synthetic data collected directly from the simulation and was used to forecast future x, y positions and heading angles of aircraft across a defined time horizon. These predictions were later used to inform real-time conflict resolution decisions.

> [!NOTE]
> While this is not the final iteration of the model that was integrated into the simulation, this version is a fully working training pipeline that successfully produced the original LSTM model used during development.

## Structure

-   `data_collection.py`: Script for generating the training dataset from the simulation environment. This exports a CSV file containing aircraft movement sequences.
-   `train.py`: Contains the full training loop and LSTM model definition.
-   `data/`: Folder containing the collected dataset (CSV format) used for training.

## Disclaimer

-   This version does not reflect the most recent changes made during simulation integration.
-   The code was not updated after successful model training, so structure and naming may differ slightly from what appears in later chapters of the thesis.
-   Despite this, the training pipeline is functional and can be used to inspect the architecture and methodology behind the conflict prediction model.
