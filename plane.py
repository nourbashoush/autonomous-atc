import math
import pygame
from configuration import *
from utils import *


class Plane:
    def __init__(self, x, y, heading, stand):
        self.image = pygame.image.load("images/plane.png")
        self.x = x
        self.y = y
        self.heading = heading
        self.thrust = 0
        self.speed = 0
        self.path = []
        self.visited = []
        self.state = "pushback"
        self.stand = stand

    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.image, -self.heading)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        window.blit(rotated_image, rotated_rect.topleft)
        
        data = config.DATA_FONT.render(
            f"{to_knots(self.speed):.0f} kts", True, (255, 255, 0)
        )
        window.blit(data, (self.x - 15, self.y - 30))

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
        # Calculate acceleration based on thrust
        acceleration = (self.thrust / 100) * MAX_ACCELERATION

        # Update speed with acceleration and drag
        self.speed += acceleration * TIME_STEP
        self.speed -= DRAG_COEFFICIENT * self.speed * TIME_STEP

        # Ensure speed does not exceed max speed
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        elif self.speed < 0:
            self.speed = 0

    def move_manual(self):
        # Update speed based on thrust and drag
        self.update_speed()

        # Update position based on speed
        radian_heading = math.radians(self.heading)
        self.x += (self.speed / PIXEL_TO_METRE) * math.sin(radian_heading) * TIME_STEP
        self.y -= (self.speed / PIXEL_TO_METRE) * math.cos(radian_heading) * TIME_STEP

    def auto_move(self):
        if self.state == "pushback":
            self.pushback()
        if self.state == "taxiing":
            self.taxi()

    def get_turn_angle(self):
        # Calculate turn angle based on speed
        if self.speed == 0:
            return 0  # No turning when stationary
        return MAX_TURN_ANGLE / (1 + TURN_SPEED_SCALING * self.speed)

    def turn_left(self):
        turn_angle = self.get_turn_angle()
        self.heading = (self.heading - turn_angle) % 360

    def turn_right(self):
        turn_angle = self.get_turn_angle()
        self.heading = (self.heading + turn_angle) % 360

    def taxi(self):
        if not self.path:
            return

        # Get the next waypoint
        end_node = get_node_object(self.path[0])
        end_x, end_y = end_node.x, end_node.y

        # Calculate the distance to the next waypoint
        distance_next = distance_between(self, end_node)
        distance_prev = (
            distance_between(self, end_node)
            if not self.visited
            else distance_between(self, get_node_object(self.visited[-1]))
        )

        # Adjust speed based on distance
        if distance_next < SLOW_DISTANCE or distance_prev < SLOW_DISTANCE:
            self.speed = to_mps(SLOW_SPEED)
        else:
            self.speed = to_mps(TAXI_SPEED)

        # Calculate the heading to the next waypoint
        radian_heading = math.atan2(end_y - self.y, end_x - self.x)
        self.heading = (math.degrees(radian_heading) + 90) % 360

        # Move towards the waypoint
        self.x += (self.speed / PIXEL_TO_METRE) * math.cos(radian_heading) * TIME_STEP
        self.y += (self.speed / PIXEL_TO_METRE) * math.sin(radian_heading) * TIME_STEP

        # Check if the plane has reached the waypoint
        if distance_next < self.speed * TIME_STEP:
            self.x = end_x
            self.y = end_y
            self.speed = 0
            self.visited.append(self.path.pop(0))

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

        # TODO: Add pathfinding to takeoff node
        if distance <= 1:
            self.x = point_x
            self.y = point_y
            self.state = "taxiing"
            return

        # Move 1 pixel towards the pushback line backwards
        radian_heading = math.radians(self.heading)
        self.x -= math.sin(radian_heading) / 10
        self.y += math.cos(radian_heading) / 10

