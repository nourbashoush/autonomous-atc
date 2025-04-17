import numpy as np
from collections import Counter

# Load the dataset
data = np.load("training_data.npy", allow_pickle=True)

# Check total samples
print(f"Total samples collected: {len(data)}")

# Extract actions from (state, action) pairs
states, actions = zip(*data)
states = np.array(states)
actions = np.array(actions)

# Count occurrences of each action
action_counts = Counter(actions)
print(f"Action distribution: {action_counts}")
