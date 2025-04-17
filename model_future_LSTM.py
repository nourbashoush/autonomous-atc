import torch
import torch.nn as nn
import configuration as config
import math
from utils import get_node_object, distance_between, angle_between


class PlaneTrajectoryLSTM(nn.Module):
    def __init__(
        self, input_size=11, hidden_size=128, num_layers=2, output_size=3, dropout=0.2
    ):
        super(PlaneTrajectoryLSTM, self).__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,  # Input/output tensors will have shape (batch, seq, feature)
            dropout=(dropout if num_layers > 1 else 0),
        )

        self.fc = nn.Linear(hidden_size, output_size * 3)

    def forward(self, x):
        # LSTM Forward Pass
        lstm_out, _ = self.lstm(x)  # lstm_out: (batch, seq_len, hidden_size)

        # Predict multiple future points using the last timestep
        out = self.fc(lstm_out[:, -1, :])  # (batch, 9)

        # Reshape to (batch_size, 3 future steps, 3 outputs each)
        out = out.view(-1, 3, 3)

        return out

    def load(self):
        self.load_state_dict(torch.load(config.LSTM_MODEL_PATH))
        self.eval()


def save_states_to_memory():
    for plane in config.PLANES:
        normalised_x = plane.x / config.WIDTH
        normalised_y = plane.y / config.HEIGHT
        normalised_heading = plane.heading / 360
        normalised_speed = plane.speed / config.MAX_SPEED

        state_encoding = {
            "preparing": [1, 0, 0, 0],  # Stationary
            "parked": [1, 0, 0, 0],  # Stationary
            "taxiing": [0, 1, 0, 0],  # Taxiing
            "parking": [0, 1, 0, 0],  # Taxiing
            "landing": [0, 0, 1, 0],  # Landing Phase
            "rollout": [0, 0, 1, 0],  # Landing Phase
            "pushback": [0, 0, 0, 1],  # Active Movement
            "takeoff": [0, 0, 0, 1],  # Active Movement
        }
        encoded_state = state_encoding.get(plane.state, [0, 0, 0, 0])

        # Distance and direction
        if not plane.path:
            distance = 0
            direction = plane.heading
        else:
            node = get_node_object(plane.path[0])
            distance = distance_between(plane, node)
            direction = angle_between(plane, node)

        clipped_distance = min(distance, 200)
        normalised_distance = clipped_distance / 200

        direction_rad = math.radians(direction)
        direction_sin = math.sin(direction_rad)
        direction_cos = math.cos(direction_rad)

        # Final state vector
        state = [
            normalised_x,
            normalised_y,
            normalised_heading,
            normalised_speed,
            *encoded_state,  # One-hot encoded state
            normalised_distance,
            direction_sin,  # Replaces normalised_direction
            direction_cos,  # Replaces normalised_direction
        ]

        plane.memory.append(state)
        if len(plane.memory) > 30:
            plane.memory.popleft()
