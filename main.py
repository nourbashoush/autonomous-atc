import pygame
from plane import Plane
from airport import initialise_graph, draw_nodes, draw_edges
from utils import *
from configuration import WIDTH, HEIGHT, AIRPORT_ICAO, FPS
import configuration as config

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airport Simulation")
config.FONT = pygame.font.Font(None, 36)

config.NODE_LIST, config.EDGE_LIST = initialise_graph(
    f"data/airport_{AIRPORT_ICAO}.json"
)
config.NODE_DICT = {node.id: node for node in config.NODE_LIST}
config.EDGE_DICT = {edge.id: edge for edge in config.EDGE_LIST}

test_plane = Plane(
    config.NODE_DICT["V2"].x, config.NODE_DICT["V2"].y, config.EDGE_DICT["V2-V1"].heading
)
dijkstra_path, distance = dijkstra(config.NODE_LIST, config.EDGE_LIST, "V2", "S1")

test_plane.path = dijkstra_path

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_UP]:
    #     test_plane.thrust_up()
    # elif keys[pygame.K_DOWN]:
    #     test_plane.thrust_down()
    # if keys[pygame.K_LEFT]:
    #     test_plane.turn_left()
    # elif keys[pygame.K_RIGHT]:
    #     test_plane.turn_right()

    # test_plane.move()

    test_plane.move_along_path()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.blit(pygame.image.load(f"images/airport_{AIRPORT_ICAO}.jpg"), (0, 0))
    draw_nodes(screen)
    draw_edges(screen)

    # Draw the plane
    test_plane.draw(screen)

    # Render thrust and speed text
    thrust_text = config.FONT.render(f"Thrust: {test_plane.thrust:.0f}%", True, (0, 0, 0))
    speed_text = config.FONT.render(
        f"Speed: {test_plane.speed:.1f} m/s", True, (0, 0, 0)
    )
    knotts_text = config.FONT.render(
        f"Speed: {to_knotts(test_plane.speed):.1f} knotts", True, (0, 0, 0)
    )
    screen.blit(thrust_text, (WIDTH - 200, 20))  # Position text top-right
    screen.blit(speed_text, (WIDTH - 200, 60))
    screen.blit(knotts_text, (WIDTH - 200, 100))

    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
