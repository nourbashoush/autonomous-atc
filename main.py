import pygame
from plane import Plane
from airport import initialise_graph, render_airport
from utils import *
import configuration as config


def setup():
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(f"Airport Simulation - {config.AIRPORT_ICAO}")
    config.MARK_FONT = pygame.font.Font(None, 12)
    config.DATA_FONT = pygame.font.Font(None, 14)

    initialise_graph(f"data/airport_{config.AIRPORT_ICAO}.json")

    return screen


def spawn_plane():
    test_plane = Plane(
        config.STAND_DICT["41"].x,
        config.STAND_DICT["41"].y,
        config.STAND_DICT["41"].heading,
        config.STAND_DICT["41"],
    )
    dijkstra_path, distance = dijkstra("V1", "S1")
    test_plane.path = dijkstra_path
    return test_plane


def main():
    screen = setup()

    test_plane = spawn_plane()

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            test_plane.thrust_up()
        elif keys[pygame.K_DOWN]:
            test_plane.thrust_down()
        if keys[pygame.K_LEFT]:
            test_plane.turn_left()
        elif keys[pygame.K_RIGHT]:
            test_plane.turn_right()

        # test_plane.move_manual()
        test_plane.auto_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_airport(screen)

        test_plane.draw(screen)

        pygame.display.update()
        clock.tick(config.FPS)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
