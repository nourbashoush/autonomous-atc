# Aircraft Agent Training Code

## Overview

This folder contains the original training scripts used to develop the aircraft movement policy via deep reinforcement learning, as outlined in Chapter 4 of the thesis.

The model was trained to enable individual aircraft agents to navigate taxi routes autonomously, simulating realistic speed, turning behaviour, and adherence to centrelines.

> [!NOTE]
> These files represent an early-stage development version. They are not maintained, and their structure may differ from the final integrated simulation environment.

## How to Inspect the Code
- The final Multi-Headed Deep Q-Network (MHDQN) architecture is implemented in `taxi_model.py`.
- The training loop and environment interaction are handled within the `agent.py` file.
- The training process can be initiated by running the main() function inside `agent.py`.
```bash
python agent.py
```

### Disclaimer
- This codebase is not guaranteed to run out-of-the-box.
- Due to its experimental and resource-intensive nature, training is slow and may require GPU acceleration for reasonable runtimes.
- This code was used solely to produce the trained models included in the final simulation. It has not been updated or tested beyond that purpose.

_For understanding the model’s behaviour and training process, it is best to review the code structure and comments rather than attempt to re-run the scripts. All implementation details and training methodology are fully documented in the thesis._