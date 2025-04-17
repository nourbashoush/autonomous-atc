import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
from lstm_model import PlaneTrajectoryLSTM
import ast
import os


# Custom Dataset Class
class PlaneDataset(Dataset):
    def __init__(self, csv_file):
        data = pd.read_csv(csv_file)

        # Extract input features and outputs
        self.inputs = data["input"].apply(ast.literal_eval).tolist()  # Input sequence
        self.outputs = (
            data[["output_3", "output_5", "output_7"]]
            .applymap(ast.literal_eval)
            .values.tolist()
        )  # Outputs for 3s, 5s, 7s

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        x = torch.tensor(self.inputs[idx], dtype=torch.float32).view(10, -1)  # (10, 11)
        y = torch.tensor(self.outputs[idx], dtype=torch.float32)  # (3, 3)
        return x, y


# Load Data
def load_data(file_path, batch_size=64):
    dataset = PlaneDataset(file_path)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader


# Training Function with Early Stopping and Learning Rate Scheduling
def train_model(
    model, train_loader, val_loader, num_epochs=50, learning_rate=0.001, patience=5
):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=3, verbose=True
    )

    best_val_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0

        total_batches = len(train_loader)
        for batch_idx, (inputs, targets) in enumerate(train_loader, 1):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            if batch_idx % 250 == 0 or batch_idx == total_batches:
                print(
                    f"Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx}/{total_batches}], Batch Loss: {loss.item():.6f}"
                )

        # Validation Phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)

        print(
            f"Epoch [{epoch+1}/{num_epochs}] Complete, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}"
        )

        # Learning Rate Scheduler Step
        scheduler.step(avg_val_loss)

        # Early Stopping Check
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            epochs_without_improvement = 0

            os.makedirs("models", exist_ok=True)

            torch.save(
                model.state_dict(), "models/best_model.pth"
            )  # Save the best model
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= patience:
            print(f"Early stopping triggered after {epoch+1} epochs")
            break


if __name__ == "__main__":
    input_size = 11  # Number of features per timestep
    hidden_size = 128  # Hidden units in LSTM
    num_layers = 2  # Number of LSTM layers
    output_size = 3  # x, y, heading

    model = PlaneTrajectoryLSTM(input_size, hidden_size, num_layers, output_size)

    print("Loading Data...")
    train_loader, val_loader = load_data("/content/drive/MyDrive/data/plane_states.csv")
    print("Data Loaded!")

    print("Training Model...")
    train_model(model, train_loader, val_loader, num_epochs=50, learning_rate=0.001)

    torch.save(model.state_dict(), "models/plane_trajectory_lstm.pth")
