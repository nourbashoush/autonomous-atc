import math
import pygame
import numpy as np
import torch
from configuration import *
from utils import *
from collections import deque


class Plane:
    def __init__(self, x, y, heading, stand, state="preparing"):
        self.x = x
        self.y = y
        self.heading = heading
        self.thrust = 0
        self.speed = 0
        self.path = []
        self.visited = []
        self.state = state
        self.stand = stand
        self.drag = config.GROUND_DRAG
        if self.state == "preparing":
            self.image = pygame.image.load(config.GROUND_IMG)
        else:
            self.image = pygame.image.load(config.AIRBORNE_IMG)
        self.memory = deque(maxlen=30)
        self.future = None

    def __repr__(self):
        return (
            f"Plane(x={self.x}, y={self.y}, heading={self.heading}, state={self.state})"
        )

    def draw(self, window):
        if self.future:
            opacities = [153, 102, 51]  # 60%, 40%, 20% of 255
            for i, pred in enumerate(self.future[:3]):
                x, y, heading = pred
                rotated_image = pygame.transform.rotate(self.image, -heading)
                rotated_image.set_alpha(opacities[i])
                rotated_rect = rotated_image.get_rect(center=(x, y))
                window.blit(rotated_image, rotated_rect.topleft)

        rotated_image = pygame.transform.rotate(self.image, -self.heading)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, rotated_rect.topleft)

        data = config.DATA_FONT.render(
            f"{to_knots(self.speed):.0f} kts {self.thrust}%", True, (255, 255, 0)
        )
        window.blit(data, (self.x - 15, self.y - 20))

    def update_state(self, state):
        self.state = state

    def thrust_up(self):
        self.thrust += THRUST_CHANGE_RATE
        if self.thrust > 100:
            self.thrust = 100

    def thrust_down(self):
        self.thrust -= THRUST_CHANGE_RATE
        if self.thrust < 0:
            self.thrust = 0
            self.brake()

    def brake(self):
        self.speed *= BRAKE_MULTIPLIER
        if self.speed <= 0.1:
            self.speed = 0

    def update_speed(self):
        acceleration = (self.thrust / 100) * MAX_ACCELERATION

        self.speed += acceleration * TIME_STEP
        self.speed -= self.drag * self.speed * TIME_STEP

        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        elif self.speed < 0:
            self.speed = 0

    def move(self):
        self.update_speed()

        radian_heading = math.radians(self.heading)
        self.x += (self.speed / PIXEL_TO_METRE) * math.sin(radian_heading) * TIME_STEP
        self.y -= (self.speed / PIXEL_TO_METRE) * math.cos(radian_heading) * TIME_STEP

    def auto_move(self):
        if self.state == "takeoff":
            self.takeoff()
        if self.state == "pushback":
            self.pushback()
        if self.state == "taxiing" or self.state == "parking":
            self.taxi()
        if self.state == "landing":
            self.land()
        if self.state == "rollout":
            self.roll()
        if self.state == "parked":
            self.park()

    def get_turn_angle(self):
        if self.speed == 0:
            return 0
        return MAX_TURN_ANGLE / (1 + TURN_SPEED_SCALING * self.speed)

    def turn_left(self):
        turn_angle = self.get_turn_angle()
        self.heading = (self.heading - turn_angle) % 360

    def turn_right(self):
        turn_angle = self.get_turn_angle()
        self.heading = (self.heading + turn_angle) % 360

    # def taxi(self):
    #     if not self.path:
    #         return

    #     end_node = get_node_object(self.path[0])
    #     end_x, end_y = end_node.x, end_node.y

    #     distance_next = distance_between(self, end_node)
    #     distance_prev = (
    #         distance_between(self, end_node)
    #         if not self.visited
    #         else distance_between(self, get_node_object(self.visited[-1]))
    #     )

    #     if distance_next < SLOW_DISTANCE or distance_prev < SLOW_DISTANCE:
    #         self.speed = to_mps(SLOW_SPEED)
    #     else:
    #         self.speed = to_mps(TAXI_SPEED)

    #     radian_heading = math.atan2(end_y - self.y, end_x - self.x)
    #     self.heading = (math.degrees(radian_heading) + 90) % 360

    #     self.x += (self.speed / PIXEL_TO_METRE) * math.cos(radian_heading) * TIME_STEP
    #     self.y += (self.speed / PIXEL_TO_METRE) * math.sin(radian_heading) * TIME_STEP

    #     if distance_next < self.speed * TIME_STEP:
    #         self.x = end_x
    #         self.y = end_y
    #         self.speed = 0
    #         self.visited.append(self.path.pop(0))

    #         runway_path = get_edge_object(config.RUNWAY_IN_USE)

    #         if self.visited[-1] == runway_path.start.id:
    #             self.state = "takeoff"
    #             self.heading = runway_path.heading
    #             self.x = runway_path.start.x
    #             self.y = runway_path.start.y

    def taxi(self):
        if not self.path:
            return

        distance_next = distance_between(self, get_node_object(self.path[0]))

        if distance_next <= MAX_DEVIATION:
            self.visited.append(self.path.pop(0))

            if self.state == "taxiing":
                runway_path = get_edge_object(config.RUNWAY_IN_USE)

                if self.visited[-1] == runway_path.start.id:
                    self.state = "takeoff"
                    self.heading = runway_path.heading
                    return

            elif self.state == "parking":
                if self.visited[-1] == self.stand:
                    self.state = "parked"
                    return

        state = np.array(get_taxi_state(self)).astype(np.float32)
        state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0)

        with torch.no_grad():
            steering_q_values, throttle_q_values = config.TAXI_MODEL(state_tensor)

        steering_action = torch.argmax(steering_q_values, dim=1).item()
        throttle_action = torch.argmax(throttle_q_values, dim=1).item()

        if steering_action == 1:
            self.turn_left()
        elif steering_action == 2:
            self.turn_right()

        if throttle_action == 1:
            self.thrust_up()
        elif throttle_action == 2:
            self.thrust_down()

        self.move()

    def pushback(self):
        pushback_line_start = self.stand.parent.start
        pushback_line_end = self.stand.parent.end
        point_x, point_y, distance = closest_point_on_line(
            self.x,
            self.y,
            pushback_line_start.x,
            pushback_line_start.y,
            pushback_line_end.x,
            pushback_line_end.y,
        )

        if distance <= 1:
            self.x = point_x
            self.y = point_y
            self.state = "taxiing"
            self.visited.append(self.path.pop(0))
            self.stand.available = True
            self.stand = None
            return

        radian_heading = math.radians(self.heading)
        self.x -= math.sin(radian_heading) / 10
        self.y += math.cos(radian_heading) / 10

    def takeoff(self):
        self.thrust = 100
        self.drag = config.TAKEOFF_DRAG
        if self.speed > to_mps(140):
            self.image = pygame.image.load(config.AIRBORNE_IMG)
        self.move()

        if (
            self.x < -1000
            or self.x > config.WIDTH + 1000
            or self.y < -1000
            or self.y > config.HEIGHT + 1000
        ):
            self.unload()

    def land(self, touch_down_deviation=120):
        self.move()

        runway_path = get_edge_object(config.RUNWAY_IN_USE)

        x_touchdown = runway_path.start.x + touch_down_deviation * math.sin(
            math.radians(runway_path.heading)
        )
        y_touchdown = runway_path.start.y - touch_down_deviation * math.cos(
            math.radians(runway_path.heading)
        )

        distance_to_touchdown = distance_between_points(
            self.x, self.y, x_touchdown, y_touchdown
        )

        if distance_to_touchdown < touch_down_deviation * 2:
            self.thrust = max(0, self.thrust - 1)

        if distance_to_touchdown < 1:
            self.state = "rollout"
            self.image = pygame.image.load(config.GROUND_IMG)
            self.thrust = 0
            # self.drag = config.GROUND_DRAG

    def roll(self):
        self.move()
        exits = config.EXIT_DICT[config.RUNWAY_IN_USE]
        exits_ahead = [exit for exit in exits if is_exit_ahead(self, exit)]
        exits_passed = [exit for exit in exits if not is_exit_ahead(self, exit)]

        if self.speed < to_mps(30):
            dijkstra_path_start, path_distance_start = dijkstra(
                exits_ahead[0], self.stand.parent.start.id
            )
            dijkstra_path_end, path_distance_end = dijkstra(
                exits_ahead[0], self.stand.parent.end.id
            )

            self.visited = [exits_passed[-1]]

            if path_distance_start < path_distance_end:
                self.path = dijkstra_path_start
            else:
                self.path = dijkstra_path_end

            stand_entrance = get_stand_entrance(self.stand)
            self.path = self.path + [stand_entrance, self.stand]

            self.state = "parking"
            self.drag = config.GROUND_DRAG

    def park(self):
        if self.speed == 0:
            return

        self.heading = self.stand.heading
        self.thrust = 0
        self.visited = []
        self.path = []

        self.brake()
        self.move()

    def unload(self):
        if self in config.PLANES:
            config.PLANES.remove(self)
        del self

    def predict_future_positions(self):
        if len(self.memory) < 10:
            return

        input_sequence = torch.tensor(
            list(self.memory)[-10:], dtype=torch.float32
        ).unsqueeze(
            0
        )  # Shape: (1, 10, 11)

        with torch.no_grad():
            predictions = config.LSTM_MODEL(input_sequence)

        predictions = predictions.squeeze(0).tolist()

        real_predictions = [
            [
                pred[0] * config.WIDTH,
                pred[1] * config.HEIGHT,
                pred[2] * 360,
            ]
            for pred in predictions
        ]

        self.future = real_predictions
