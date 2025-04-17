import random
import math
import configuration as config
from plane import Plane
from utils import (
    distance_between,
    to_mps,
    to_knots,
    get_distance_from_path,
    closest_point_on_line,
)
import numpy as np

if config.RENDER:
    import pygame

    pygame.init()
    config.DATA_FONT = pygame.font.Font("arial.ttf", 12)
    config.SCORE_FONT = pygame.font.Font("arial.ttf", 23)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class IdealPosition:
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.heading = 0
        self.speed = 0
        self.path_index = 1
        self.path = path
        self.destination = path[self.path_index]

    def move(self):
        end_x, end_y = self.destination.x, self.destination.y
        distance_next = distance_between(self.x, self.y, end_x, end_y)

        prev_x, prev_y = (
            self.path[self.path_index - 1].x,
            self.path[self.path_index - 1].y,
        )
        distance_prev = distance_between(self.x, self.y, prev_x, prev_y)

        if distance_next < config.SLOW_DISTANCE or distance_prev < config.SLOW_DISTANCE:
            self.speed = to_mps(config.SLOW_SPEED)
        else:
            self.speed = to_mps(config.TAXI_SPEED)

        radian_heading = math.atan2(end_y - self.y, end_x - self.x)
        self.heading = (math.degrees(radian_heading) + 90) % 360

        self.x += (
            (self.speed / config.PIXEL_TO_METRE)
            * math.cos(radian_heading)
            * config.TIME_STEP
        )
        self.y += (
            (self.speed / config.PIXEL_TO_METRE)
            * math.sin(radian_heading)
            * config.TIME_STEP
        )

        if distance_next < self.speed * config.TIME_STEP:
            self.x = end_x
            self.y = end_y
            self.speed = 0

    def update_destination(self):
        self.path_index += 1
        if self.path_index >= len(self.path):
            self.path_index = len(self.path) - 1
        self.destination = self.path[self.path_index]

    def draw(self, window):
        if not config.RENDER:
            return

        pygame.draw.circle(
            window,
            (255, 255, 0),
            (int(self.x), int(self.y)),
            config.MAX_DEVIATION,
        )


class GroundTrainingAI:

    def __init__(self, w=config.WIDTH, h=config.HEIGHT):
        self.width = w
        self.height = h
        if config.RENDER:
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Training AI")
            self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.score = 0
        self.frame_iteration = 0
        self.path, self.path_distance = self.generate_path()
        start_radian = math.atan2(
            self.path[1].y - self.path[0].y, self.path[1].x - self.path[0].x
        )
        start_heading = (
            (math.degrees(start_radian) + 90) + random.randint(-60, 60)
        ) % 360
        self.plane = Plane(self.path[0].x, self.path[0].y, start_heading)
        self.ideal_position = IdealPosition(self.path[0].x, self.path[0].y, self.path)

        self.previous_node = self.path[0]
        self.next_node = self.path[1]
        self.previous_distance = distance_between(
            self.previous_node.x,
            self.previous_node.y,
            self.next_node.x,
            self.next_node.y,
        )

    def generate_path(
        self, num_nodes=4, min_distance=50, max_distance=150, max_attempts=20
    ):
        current_path = []

        # Generate the first node randomly
        start_x = random.randint(50, self.width - 50)
        start_y = random.randint(50, self.height - 50)
        current_path.append(Node(start_x, start_y))

        # Set a random initial heading (0° = right, 90° = down, 180° = left, 270° = up)
        heading = random.uniform(0, 360)

        i = 1  # Start from second node
        while i < num_nodes:
            attempts = 0  # Reset attempt counter
            valid_node_found = False

            while attempts < max_attempts:
                attempts += 1

                # Choose a random angle within a forward-facing range (-90° to +90°)
                angle_offset = random.uniform(-90, 90)
                new_heading = (
                    heading + angle_offset
                ) % 360  # Keep heading within 0-360°

                # Convert heading to movement vector
                radian_angle = math.radians(new_heading)
                distance = random.randint(min_distance, max_distance)
                new_x = int(current_path[-1].x + distance * math.cos(radian_angle))
                new_y = int(current_path[-1].y + distance * math.sin(radian_angle))

                # Ensure the new point is within bounds
                if 50 <= new_x <= self.width - 50 and 50 <= new_y <= self.height - 50:
                    current_path.append(Node(new_x, new_y))
                    heading = new_heading  # Update heading to maintain smooth path
                    valid_node_found = True
                    break  # Exit loop once a valid node is found

            if not valid_node_found:
                while True:
                    x = random.randint(0 + 50, self.width - 50)
                    y = random.randint(0 + 50, self.height - 50)

                    if (
                        i == 0
                        or distance_between(
                            x, y, current_path[-1].x, current_path[-1].y
                        )
                        > min_distance
                        and distance_between(
                            x, y, current_path[-1].x, current_path[-1].y
                        )
                        < max_distance
                    ):
                        current_path.append(Node(x, y))
                        break

            i += 1

        # Compute total distance of the path
        total_distance = sum(
            distance_between(
                current_path[i].x,
                current_path[i].y,
                current_path[i + 1].x,
                current_path[i + 1].y,
            )
            for i in range(len(current_path) - 1)
        )

        return current_path, total_distance

    def play_step(self, action):
        self.frame_iteration += 1
        state = self.get_state()

        if config.RENDER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    # Reset action to default [0, 0]
                    action = [0, 0]
                    if event.key == pygame.K_UP:
                        action[1] = 1  # Throttle up
                    elif event.key == pygame.K_DOWN:
                        action[1] = 2  # Throttle down
                    elif event.key == pygame.K_LEFT:
                        action[0] = 1  # Turn left
                    elif event.key == pygame.K_RIGHT:
                        action[0] = 2  # Turn right

        self._move(action)

        if config.RENDER:
            self._update_display()

        steering_reward = 0
        throttle_reward = 0
        game_over = False

        if self._is_idle() or self._is_too_far():
            game_over = True
            steering_reward -= 5
            throttle_reward -= 5
            self.score += steering_reward + throttle_reward
            return steering_reward, throttle_reward, game_over, self.score

        if self._is_reached()[0]:
            steering_reward += 5
            throttle_reward += 5
            self.ideal_position.update_destination()
            if self._is_reached()[1]:
                game_over = True
                self.score += steering_reward + throttle_reward
                return steering_reward, throttle_reward, game_over, self.score

        steering_reward += self._calculate_steering_reward(state, action)
        throttle_reward += self._calculate_throttle_reward(state, action)

        self.score += steering_reward + throttle_reward
        return steering_reward, throttle_reward, game_over, self.score

    def _calculate_steering_reward(self, state, action):
        reward = 0

        if state[-4] < -0.03:  # Turn left
            if action[0] == 1:
                reward += 0.5
            else:
                reward -= 1
        elif state[-4] > 0.03:  # Turn right
            if action[0] == 2:
                reward += 0.5
            else:
                reward -= 1
        else:
            reward += 0.1

        return reward

    def _calculate_throttle_reward(self, state, action):
        current_speed_knots = to_knots(self.plane.speed)
        reward = 0

        # Reward for being in correct speed range (15-25 knots)
        if 15 <= current_speed_knots <= 20:
            reward += 0.5
        else:
            reward -= 0.2

        return reward

    def _update_display(self):
        if not config.RENDER:
            return

        self.display.fill((255, 255, 255))

        for i in range(len(self.path) - 1):
            pygame.draw.line(
                self.display,
                (0, 0, 255),
                (self.path[i].x, self.path[i].y),
                (self.path[i + 1].x, self.path[i + 1].y),
                1,
            )

        pygame.draw.circle(
            self.display,
            (0, 255, 0),
            (self.next_node.x, self.next_node.y),
            config.MAX_DEVIATION,
        )

        for node in self.path:
            pygame.draw.circle(self.display, (255, 0, 0), (node.x, node.y), 3)

        # self.ideal_position.draw(self.display)

        self.plane.draw(self.display)

        score_text = config.SCORE_FONT.render(
            f"Score: {self.score:.2f}",
            True,
            (0, 0, 0),
        )
        frame_text = config.SCORE_FONT.render(
            f"Frame: {self.frame_iteration}/{config.EPISODE_LENGTH_MULTIPLIER * self.path_distance:.0f}",
            True,
            (0, 0, 0),
        )

        self.display.blit(score_text, (0, 0))
        self.display.blit(frame_text, (0, 30))

        pygame.display.update()
        self.clock.tick(config.FPS)

    def _update_close_distance(self):
        if self._is_closer():
            distance_to_next = distance_between(
                self.plane.x, self.plane.y, self.next_node.x, self.next_node.y
            )
            self.previous_distance = distance_to_next

    def _is_too_far(self):
        distance_from_path = get_distance_from_path(
            self.plane, self.previous_node, self.next_node
        )

        return distance_from_path > config.MAX_DEVIATION

    def _is_closer(self):
        distance_to_next = distance_between(
            self.plane.x, self.plane.y, self.next_node.x, self.next_node.y
        )

        if self.previous_distance - distance_to_next >= config.DISTANCE_CHECKPOINTS:
            return True
        else:
            return False

    def _is_reached(self):
        radius = config.MAX_DEVIATION

        is_reached = (
            distance_between(
                self.plane.x, self.plane.y, self.next_node.x, self.next_node.y
            )
            < radius
        )

        is_reached_end = False

        if is_reached:
            index = self.path.index(self.next_node)
            self.previous_node = self.path[index]

            if index + 1 < len(self.path):
                self.next_node = self.path[index + 1]
            else:
                is_reached_end = True

        return is_reached, is_reached_end

    def _is_out_of_bounds(self):
        return (
            self.plane.x > self.width
            or self.plane.x < 0
            or self.plane.y > self.height
            or self.plane.y < 0
        )

    def _is_idle(self):
        return (
            self.frame_iteration > config.EPISODE_LENGTH_MULTIPLIER * self.path_distance
        )

    def _move(self, action):
        # action: [steering_action, throttle_action]
        # Steering: 0 = no turn, 1 = turn left, 2 = turn right
        # Throttle: 0 = no thrust change, 1 = thrust up, 2 = thrust down
        if action[0] == 1:
            self.plane.turn_left()
        elif action[0] == 2:
            self.plane.turn_right()

        if action[1] == 1:
            self.plane.thrust_up()
        elif action[1] == 2:
            self.plane.thrust_down()

        self.plane.move()
        self.ideal_position.move()

    def get_state(self):
        angles = [-90, 0, 90]
        distances = []

        plane_x, plane_y = self.plane.x, self.plane.y

        for angle in angles:
            # Compute absolute angle in world space
            absolute_angle = (self.plane.heading + angle - 90) % 360
            radian_angle = math.radians(absolute_angle)

            # Direction vector (unit length)
            dx, dy = math.cos(radian_angle), math.sin(radian_angle)

            # Start at the plane's position
            current_x, current_y = plane_x, plane_y
            step_size = 1  # Step 1 pixel at a time

            while True:
                # Move along the direction vector
                current_x += dx * step_size
                current_y += dy * step_size

                # Compute distance to closest point on the path
                closest_x, closest_y, distance_to_path = closest_point_on_line(
                    current_x,
                    current_y,
                    self.previous_node.x,
                    self.previous_node.y,
                    self.next_node.x,
                    self.next_node.y,
                )

                # Stop when we reach the max deviation boundary
                if distance_to_path >= config.MAX_DEVIATION:
                    break

            # Compute the final distance from the plane to this intersection
            distance_to_boundary = distance_between(
                plane_x, plane_y, current_x, current_y
            )
            distances.append(distance_to_boundary)

            if config.RENDER:
                pygame.draw.circle(
                    self.display, (0, 0, 255), (int(current_x), int(current_y)), 3
                )

        if config.RENDER:
            pygame.display.update()

        # Calculate the angle to the next checkpoint
        delta_x = self.next_node.x - self.plane.x
        delta_y = self.next_node.y - self.plane.y
        angle_to_checkpoint = (math.degrees(math.atan2(delta_y, delta_x)) + 360) % 360

        # Get the difference in angles (relative to the plane’s heading)
        angle_diff = (angle_to_checkpoint - self.plane.heading + 90) % 360

        # Normalize the angle difference to the range [-180, 180]
        if angle_diff > 180:
            angle_diff -= 360

        # Scale the angle difference to the range [-1, 1]
        turn_direction = angle_diff / 180

        normalised_distances = np.array(distances) / 150.0
        normalised_speed = self.plane.speed / 100.0

        distance_to_checkpoint = distance_between(
            self.plane.x, self.plane.y, self.next_node.x, self.next_node.y
        )
        normalised_distance_to_checkpoint = distance_to_checkpoint / 150.0
        normalised_thrust = self.plane.thrust / 100.0

        state = np.append(
            normalised_distances,
            [
                turn_direction,
                normalised_speed,
                normalised_distance_to_checkpoint,
                normalised_thrust,
            ],
        )

        return state.astype(np.float32)


# if __name__ == "__main__":
#     env = GroundTrainingAI()
#     env.reset()

#     while True:
#         steering_reward, thrust_reward, game_over, score = env.play_step([0, 0])
#         if game_over:
#             env.reset()
#             break
