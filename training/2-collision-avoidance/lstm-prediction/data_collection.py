import csv
import configuration as config
from utils import *


def initialize_data_collection():
    file_path = "data/plane_states.csv"  # Ensure this path is correct

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Ensure the headers match the data structure
        writer.writerow(
            ["input", "output_1", "output_3", "output_5", "output_7", "output_10"]
        )


def save_states_to_memory():
    for plane in config.PLANES:
        normalised_x = plane.x / config.WIDTH
        normalised_y = plane.y / config.HEIGHT
        normalised_heading = plane.heading / 360
        normalised_speed = plane.speed / config.MAX_SPEED

        # One-hot encoding
        state_encoding = {
            "preparing":     [1, 0, 0, 0],  # Stationary
            "parked":        [1, 0, 0, 0],  # Stationary
            "taxiing":       [0, 1, 0, 0],  # Taxiing
            "parking":       [0, 1, 0, 0],  # Taxiing
            "landing":       [0, 0, 1, 0],  # Landing Phase
            "rollout":       [0, 0, 1, 0],  # Landing Phase
            "pushback":      [0, 0, 0, 1],  # Active Movement
            "takeoff":       [0, 0, 0, 1],  # Active Movement
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

        # Clipping distance for normalisation
        clipped_distance = min(distance, 200)
        normalised_distance = clipped_distance / 200

        # Sin/Cos for smooth directional encoding
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

        # Memory management
        plane.memory.append(state)
        if len(plane.memory) > 30:
            plane.memory.popleft()


def append_states_to_csv():
    def extract_output_from_state(state):
        # Extract relevant output data from the state
        output = [state[0], state[1], state[2]]
        return output

    for plane in config.PLANES:
        if len(plane.memory) == 30:  # Ensure the memory length is correct
            input_sequence = [
                item for state in list(plane.memory)[:10] for item in state
            ]

            with open("data/plane_states.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        input_sequence,  # Flattened input sequence
                        extract_output_from_state(
                            plane.memory[11]
                        ),  # Output at timestep 11
                        extract_output_from_state(
                            plane.memory[15]
                        ),  # Output at timestep 15
                        extract_output_from_state(
                            plane.memory[19]
                        ),  # Output at timestep 19
                        extract_output_from_state(
                            plane.memory[23]
                        ),  # Output at timestep 23
                        extract_output_from_state(
                            plane.memory[29]
                        ),  # Output at timestep 29
                    ]
                )
