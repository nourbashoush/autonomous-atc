import torch
import torch.nn as nn
import torch.optim as optim
import os


class MultiHeadQNet(nn.Module):
    def __init__(
        self, input_size, hidden_size, output_size_steering, output_size_throttle
    ):
        super(MultiHeadQNet, self).__init__()
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

    def save(self, file_name="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_path = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_path)

    def load(self, file_name="model.pth"):
        model_folder_path = "./model"
        file_path = os.path.join(model_folder_path, file_name)
        if os.path.exists(file_path):
            self.load_state_dict(torch.load(file_path))
        else:
            print(
                f"Model file '{file_path}' does not exist. Starting with a new model."
            )


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimiser = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done, target_model):
        device = next(self.model.parameters()).device

        state = torch.tensor(state, dtype=torch.float32, device=device)
        # Actions now are shape (batch_size, 2) with dtype long
        action = torch.tensor(action, dtype=torch.long, device=device)
        reward = torch.tensor(reward, dtype=torch.float32, device=device)
        next_state = torch.tensor(next_state, dtype=torch.float32, device=device)

        # Get predictions for the current state (two heads)
        pred_steer, pred_throttle = self.model(state)
        with torch.no_grad():
            next_pred_steer, next_pred_throttle = target_model(next_state)

        # Clone predictions to form targets
        target_steer = pred_steer.clone().detach()
        target_throttle = pred_throttle.clone().detach()

        for idx in range(len(done)):
            # reward[idx][0] for steering, reward[idx][1] for throttle
            Q_new_steer = reward[idx][0]
            Q_new_throttle = reward[idx][1]
            if not done[idx]:
                Q_new_steer = reward[idx][0] + self.gamma * torch.max(
                    next_pred_steer[idx]
                )
                Q_new_throttle = reward[idx][1] + self.gamma * torch.max(
                    next_pred_throttle[idx]
                )
            steering_action = action[idx][0]  # first element is steering action
            throttle_action = action[idx][1]  # second element is throttle action
            target_steer[idx][steering_action] = Q_new_steer
            target_throttle[idx][throttle_action] = Q_new_throttle

        self.optimiser.zero_grad()
        loss_steer = self.criterion(target_steer, pred_steer)
        loss_throttle = self.criterion(target_throttle, pred_throttle)
        loss = loss_steer + loss_throttle
        loss.backward()
        self.optimiser.step()
