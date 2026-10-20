# LSTM prediction

Training for the LSTM that predicts where aircraft will be, from Chapter 5.3 of the thesis. This is
the approach the simulation uses. [`../README.md`](../README.md) explains how its predictions decide
who gives way.

The LSTM learns from data recorded in the simulation. It predicts each aircraft's x and y position
and heading over the next few seconds.

> [!NOTE]
> The model in the simulation is a later version than this code produces. This pipeline still works
> end to end, and it's the one that trained the original LSTM during development.

## Running it

There are two steps, both from this folder.

**1. Collect the data.** This runs 65 simulations with the trained taxiing model and records how the
aircraft move:
```bash
python main.py
```
The data goes to `data/plane_states.csv`. The original dataset was about 2.1 GB, so it's not in the
repository.

> [!WARNING]
> A new collection replaces any existing `data/plane_states.csv`.

**2. Train the LSTM:**
```bash
python train.py
```
This trains for up to 50 epochs and stops early once the validation loss stops improving. The best
model is saved to `models/best_model.pth`.

## Files

- `main.py` – Runs the simulations that make the dataset.
- `data_collection.py` – The functions `main.py` uses to record each aircraft's movement and write it to the CSV.
- `train.py` – The LSTM model and its training loop.
- `data/` – The airport layout, and the dataset once you've collected it.
- `models/` – The trained models.

> [!NOTE]
> I didn't update this code after the model trained successfully. Some names and structure differ
> from later chapters of the thesis and from the simulation.
