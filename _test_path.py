import pygame
import sys
import time
import math
from plane import Plane
from utils import distance_between

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 500, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Lines")
test_plane = Plane(100, 100, 180)

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
PIXEL_TO_METRE = 2.5
TIME_STEP = 1 / 30
path = [[(100, 100), (100, 400)], [(100, 400), (400, 400)]]


def move_along_path(plane, path):

    if path == []:
        return

    start_x, start_y = path[0][0]
    end_x, end_y = path[0][1]

    # TODO: Check distance and adjust speed
    if True:
        speed = 25
    else:
        speed = 10

    arrived_x = False
    arrived_y = False

    radian_heading = math.atan2(end_y - start_y, end_x - start_x)
    plane.x += (speed / PIXEL_TO_METRE) * math.cos(radian_heading) * TIME_STEP
    plane.y += (speed / PIXEL_TO_METRE) * math.sin(radian_heading) * TIME_STEP
    plane.heading = (math.degrees(radian_heading) + 90) % 360

    # Check if the plane has reached or passed the end point
    if (start_x <= end_x and plane.x >= end_x) or (
        start_x >= end_x and plane.x <= end_x
    ):
        plane.x = end_x
        arrived_x = True
    if (start_y <= end_y and plane.y >= end_y) or (
        start_y >= end_y and plane.y <= end_y
    ):
        plane.y = end_y
        arrived_y = True

    # If the plane has reached the end point, remove the path
    if arrived_x and arrived_y:
        path.pop(0)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    window.fill(white)

    # Draw lines
    pygame.draw.line(window, black, (100, 100), (100, 400), 2)
    pygame.draw.line(window, black, (100, 400), (400, 400), 2)
    test_plane.draw(window)
    move_along_path(test_plane, path)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
