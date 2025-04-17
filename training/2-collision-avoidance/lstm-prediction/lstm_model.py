import torch
import torch.nn as nn
import configuration as config


class PlaneTrajectoryLSTM(nn.Module):
    def __init__(self, input_size=11, hidden_size=128, num_layers=2, output_size=3, dropout=0.2):
        super(PlaneTrajectoryLSTM, self).__init__()

        # LSTM Layer
        self.lstm = nn.LSTM(
            input_size=input_size,  
            hidden_size=hidden_size,
            num_layers=num_layers,  # Number of stacked LSTM layers
            batch_first=True,  # Input/output tensors will have shape (batch, seq, feature)
            dropout=(
                dropout if num_layers > 1 else 0
            ),
        )

        # Fully Connected Layer (Output Layer)
        self.fc = nn.Linear(
            hidden_size, output_size * 3
        )  # 3 time horizons - Maps LSTM output to (x, y, heading)

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