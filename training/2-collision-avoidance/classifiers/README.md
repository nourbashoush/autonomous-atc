# Supervised Learning – Collision Avoidance

## Overview

This folder contains the supervised learning experiments that were conducted as an alternative to multi-agent reinforcement learning (MARL), as described in Chapter 5.5 of the thesis.

These models were designed to predict binary stop/go actions for aircraft in conflict scenarios using classic machine learning techniques: decision trees, logistic regression, and random forests.

## Contents
- `CollisionAvoidanceClassifier.ipynb`: The main notebook containing:
  - All preprocessing steps
  - Feature engineering (e.g. relative angle, projected distance)
  - Final classifier training and evaluation
- Datasets used for training and validation are included in the folder.
- Min–Max and standardisation parameters used during training are stored and applied consistently to ensure fair preprocessing during inference.