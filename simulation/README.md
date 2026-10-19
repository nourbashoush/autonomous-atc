# Autonomous ATC Airport Simulation

## Overview
This repository contains the simulation code developed for the final year project “A Proof of Concept for Autonomous Air Traffic Control Using Deep Learning”. The simulation environment integrates reinforcement learning (RL), long short-term memory (LSTM) models, and computer vision to autonomously manage aircraft movement within a ground control context.

The primary objective is to visualise and evaluate trained deep learning models within a 2D simulation of Birmingham Airport, focusing on ground operations such as taxiing, take-off preparation, landing clearance, and runway occupancy.

> [!NOTE]
This repository only includes the simulation code. Training scripts for the the mentioned models are located in other sections of the repository.

## Requirements
- Python 3.9 or higher (3.9 recommended)
- Compatible operating system (Linux/macOS/Windows)
- Recommended 8GB RAM

## Requirements Installation
Before running the simulation, install the dependencies listed in `requirements.txt`.

_It is recommended to create a virtual environment to avoid conflicts with other projects._
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then, install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Simulation
Once dependencies are installed, the simulation can be launched using:
```bash
python main.py
```
The simulation will automatically render a cleaned, top-down visual of Birmingham Airport (EGBB), with dynamic elements such as taxiways, holding points, stands, and a single operational runway.

> [!NOTE]
On the first execution, it may take up to 2 minutes to initialise assets, load packages, and render the environment. Subsequent runs will be significantly faster due to caching.

## Simulation Behaviour

By default:
- 10 aircraft are spawned for departure (take-off).
- Aircraft for landing are spawned continuously at safe intervals until the airport becomes full.
- All aircraft are governed by reinforcement learning agents trained to navigate taxi routes autonomously.
- Conflict management and intersection logic are handled using LSTM-based future prediction models.
- Runway access is monitored via a YOLOv8 computer vision model that prevents incursions.
- Aircraft wait and queue when necessary.

### Notes
- The simulation is fully self-contained and does not require any external datasets or internet access.
- Trained model weights are preloaded and automatically initialised at runtime.
- No GUI interaction is required; the simulation is fully automated.
- Visual debugging features (e.g., taxi paths, decision markers) are enabled by default.