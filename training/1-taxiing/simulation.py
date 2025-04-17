import random
import pygame
import math
from plane import Plane
from utils import distance_between, to_mps
import configuration as config


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

        prev_x, prev_y = self.path[self.path_index - 1].x, self.path[self.path_index - 1].y
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
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.path_index = len(self.path) - 1
            self.destination = self.path[self.path_index]

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 0), (int(self.x), int(self.y)), 4)


class GroundTrainingAI:

    def __init__(self, w=config.WIDTH, h=config.HEIGHT):
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Training AI")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.path = self.generate_path()
        self.score = 0
        self.frame_iteration = 0
        start_radian = math.atan2(
            self.path[1].y - self.path[0].y, self.path[1].x - self.path[0].x
        )
        start_heading = (math.degrees(start_radian) + 90) % 360
        self.plane = Plane(self.path[0].x, self.path[0].y, start_heading)
        self.ideal_position = IdealPosition(
            self.path[0].x, self.path[0].y, self.path
        )

    def generate_path(self, num_nodes=4, min_distance=50, max_distance=500):
        current_path = []

        for i in range(num_nodes):
            while True:
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)

                if (
                    i == 0
                    or distance_between(x, y, current_path[-1].x, current_path[-1].y)
                    > min_distance
                    and distance_between(x, y, current_path[-1].x, current_path[-1].y)
                    < max_distance
                ):
                    current_path.append(Node(x, y))
                    break

        return current_path

    def run(self):
        while True:
            self.frame_iteration += 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.plane.thrust_up()
            elif keys[pygame.K_DOWN]:
                self.plane.thrust_down()
            if keys[pygame.K_LEFT]:
                self.plane.turn_left()
            elif keys[pygame.K_RIGHT]:
                self.plane.turn_right()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.move()
            self._update_display()

            pygame.display.update()
            self.clock.tick(config.FPS)

    def _update_display(self):
        self.display.fill((255, 255, 255))

        for i in range(len(self.path) - 1):
            pygame.draw.line(
                self.display,
                (0, 0, 255),
                (self.path[i].x, self.path[i].y),
                (self.path[i + 1].x, self.path[i + 1].y),
                1,
            )

        for node in self.path:
            pygame.draw.circle(self.display, (255, 0, 0), (node.x, node.y), 3)

        self.ideal_position.draw(self.display)

        self.plane.draw(self.display)

        pygame.display.update()

    def move(self):
        self.plane.move()
        self.ideal_position.move()


if __name__ == "__main__":
    pygame.init()
    config.DATA_FONT = pygame.font.Font("arial.ttf", 12)
    ai = GroundTrainingAI()
    ai.run()
