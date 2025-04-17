# Multi-Agent Reinforcement Learning for Collision Avoidance

## Overview

This folder contains the source code used for training the multi-agent reinforcement learning (MARL) model for aircraft coordination and conflict avoidance, as discussed in Chapter 5 of the thesis.

The MARL agents were designed to learn decentralised decision-making strategies (e.g. when to stop or yield) through shared experience in a dynamic airport simulation environment.

This folder also contains the training data used to train the machine machine learning models detailed in Chapter 5.5 of the thesis.

## Contents
- Base training scripts and utility modules are provided as `.py` files.
- The most up-to-date and complete implementation is located in the `CollisionAvoidanceTraining.ipynb` Jupyter notebook.
- This notebook consolidates:
  - The current reward shaping logic
  - The updated state observation definitions
  - Implementations of Prioritised Experience Replay (PER) and Balanced Experience Replay (BER)

> [!NOTE]
> Training was conducted on external GPU-enabled cloud services. As a result, the .py files may be slightly outdated compared to the notebook version. For the most reliable and reproducible results, refer exclusively to the notebook.
