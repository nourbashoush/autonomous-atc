# Training

How each model was made, in thesis chapter order. The trained models are already in
[`simulation/models`](../simulation/models), so you don't need any of this to run the simulation.
It's here to show how they were built, and so you can retrain them.

| Folder | Model | Thesis | Result |
| --- | --- | --- | --- |
| [`1-taxiing`](1-taxiing) | Multi-headed deep Q-network | Chapter 4 | Taxis within about 7 m of the centreline, at an average of 16 knots |
| [`2-collision-avoidance`](2-collision-avoidance) | LSTM, after multi-agent RL and classifiers | Chapter 5 | No collisions, and at least about 45 m between queueing aircraft |
| [`3-runway-detection`](3-runway-detection) | YOLOv8 | Chapter 6 | Precision 1.00 and recall 1.00 on the validation set |
| [`4-pilot-requests`](4-pilot-requests) | BERT and DistilBERT | Chapter 7 | 100% request type accuracy and 96% top-1 flight accuracy on the test set |

## Setup

Everything uses the same packages as the simulation, from
[`requirements.txt`](../requirements.txt). Each folder's README says what to run. Some parts are
Jupyter notebooks, which you open by running `jupyter notebook` in that folder.

> [!NOTE]
> Full training runs take hours on a normal computer. The final taxiing model alone took about four
> hours, and I trained some of the collision avoidance models on cloud GPUs.

## Large files that aren't in the repository

- **Generated datasets.** These are the LSTM's 2.1 GB of aircraft movement data and the runway
  detector's 5,000 radar images. Each folder's README explains how to make them again.
- **The two pilot request models**, about 670 MB together. They're on the
  [Releases](https://github.com/nourbashoush/autonomous-atc/releases) page, and
  [`4-pilot-requests`](4-pilot-requests) explains where to put them.
