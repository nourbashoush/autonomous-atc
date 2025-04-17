import torch
import torch.nn as nn
from configuration import TAXI_MODEL_PATH


class TaxiNet(nn.Module):
    def __init__(
        self,
        input_size=7,
        hidden_size=16,
        output_size_steering=3,
        output_size_throttle=3,
    ):
        super(TaxiNet, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.steering_head = nn.Linear(hidden_size, output_size_steering)
        self.throttle_head = nn.Linear(hidden_size, output_size_throttle)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        steering_output = self.steering_head(x)
        throttle_output = self.throttle_head(x)
        return steering_output, throttle_output

    def load(self, file_path=TAXI_MODEL_PATH):
        self.load_state_dict(torch.load(file_path))
        self.eval()