import torch
import random
import time
import numpy as np
import configuration as config
from collections import deque
from game import GroundTrainingAI
from model import MultiHeadQNet, QTrainer
from utils import plot

# Constants
MAX_MEMORY = 500_000
BATCH_SIZE = 5_000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.99
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = MultiHeadQNet(7, 16, 3, 3).to(self.get_device())
        self.target_model = MultiHeadQNet(7, 16, 3, 3).to(self.get_device())
        self.update_target_model()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_device(self):
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            return torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        states = np.array(states, dtype=np.float32)
        actions = np.array(actions, dtype=np.float32)
        rewards = np.array(rewards, dtype=np.float32)
        next_states = np.array(next_states, dtype=np.float32)
        dones = np.array(dones, dtype=np.float32)

        self.trainer.train_step(
            states, actions, rewards, next_states, dones, self.target_model
        )

    def train_short_memory(self, state, action, reward, next_state, done):
        state = np.array([state], dtype=np.float32)
        action = np.array([action], dtype=np.float32)
        reward = np.array([reward], dtype=np.float32)
        next_state = np.array([next_state], dtype=np.float32)
        done = np.array([done], dtype=np.float32)
        self.trainer.train_step(
            state, action, reward, next_state, done, self.target_model
        )

    def get_action(self, state):
        self.epsilon = max(0.05, 1.0 * (0.995**self.n_games))
        if random.random() < self.epsilon:
            steering_action = random.randint(
                0, 2
            )  # 0: no turn, 1: turn left, 2: turn right
            throttle_action = random.randint(
                0, 2
            )  # 0: no thrust change, 1: thrust up, 2: thrust down
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(self.get_device())
            steering_q, throttle_q = self.model(state0)
            steering_action = torch.argmax(steering_q).item()
            throttle_action = torch.argmax(throttle_q).item()
        return [steering_action, throttle_action]


def train():
    agent = Agent()
    game = GroundTrainingAI()

    record = float("-inf")
    total_score = 0
    plot_scores = []
    plot_mean_scores = []

    while True:
        start_time = time.time()

        state_old = game.get_state()
        final_move = agent.get_action(state_old)
        reward_steer, reward_throttle, done, score = game.play_step(final_move)
        reward_pair = [reward_steer, reward_throttle]
        state_new = game.get_state()

        agent.train_short_memory(state_old, final_move, reward_pair, state_new, done)
        agent.remember(state_old, final_move, reward_pair, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            elif agent.n_games % 250 == 0:
                agent.model.save()

            total_score += score
            mean_score = total_score / agent.n_games
            plot_scores.append(score)
            plot_mean_scores.append(mean_score)

            end_time = time.time()
            duration = end_time - start_time

            if agent.n_games % 5 == 0:
                if config.RENDER:
                    print(
                        f"{agent.n_games}: \tScore: {score:.2f} \tAvg: {mean_score:.2f} \tMem: {len(agent.memory)} \tDuration: {duration:.2f}s"
                    )
                else:
                    agent.update_target_model()
                    plot(plot_scores, plot_mean_scores)


def test_model(model_file="steering_and_speed.pth", num_test_games=10):
    game = GroundTrainingAI(config.WIDTH, config.HEIGHT)

    input_size = 7
    hidden_size = 16
    output_size_steering = 3
    output_size_throttle = 3

    model = MultiHeadQNet(
        input_size, hidden_size, output_size_steering, output_size_throttle
    )
    model.load(model_file)
    model.eval()

    for game_idx in range(1, num_test_games + 1):
        game.reset()
        total_score = 0
        done = False

        while not done:
            state = np.array(game.get_state()).astype(np.float32)
            state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0)

            with torch.no_grad():
                steering_q_values, throttle_q_values = model(state_tensor)

            steering_action = torch.argmax(steering_q_values, dim=1).item()
            throttle_action = torch.argmax(throttle_q_values, dim=1).item()

            action_vector = [steering_action, throttle_action]

            reward_steer, reward_throttle, done, score = game.play_step(action_vector)
            total_score += reward_steer + reward_throttle

            if config.RENDER:
                game._update_display()

        print(f"Test Game {game_idx}: Score = {total_score:.2f}")


if __name__ == "__main__":
    train()
    # test_model()
