import random
import pygame
from plane import Plane
from airport import initialise_graph, render_airport
from utils import *
import configuration as config
from taxi_model import TaxiNet


def setup():
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(f"Airport Simulation - {config.AIRPORT_ICAO}")
    config.MARK_FONT = pygame.font.Font(None, 12)
    config.DATA_FONT = pygame.font.Font(None, 14)

    initialise_graph(f"data/airport_{config.AIRPORT_ICAO}.json")

    taxi = TaxiNet()
    taxi.load()
    config.TAXI_MODEL = taxi

    return screen


def spawn_planes_at_stands():
    available_stands = [stand for stand in config.STAND_LIST if stand.available]
    selected_stands = random.sample(available_stands, min(10, len(available_stands)))

    for stand in selected_stands:
        new_plane = Plane(stand.x, stand.y, stand.heading, stand)
        dijkstra_path_start, path_distance_start = dijkstra(
            stand.parent.start.id, get_edge_object(config.RUNWAY_IN_USE).start.id
        )
        dijkstra_path_end, path_distance_end = dijkstra(
            stand.parent.end.id, get_edge_object(config.RUNWAY_IN_USE).start.id
        )
        if path_distance_start < path_distance_end:
            dijkstra_path = [stand.parent.end.id] + dijkstra_path_start
        else:
            dijkstra_path = [stand.parent.start.id] + dijkstra_path_end
        new_plane.path = dijkstra_path
        config.PLANES.append(new_plane)
        stand.available = False


def spawn_planes_for_landing(distance_from_runway=1000):
    if find_available_stand() and random.randint(1, config.LANDING_PROBABILITY) == 1:
        runway_path = get_edge_object(config.RUNWAY_IN_USE)
        x_spawn = runway_path.start.x - distance_from_runway * math.sin(
            math.radians(runway_path.heading)
        )
        y_spawn = runway_path.start.y + distance_from_runway * math.cos(
            math.radians(runway_path.heading)
        )

        available_stand = find_available_stand()
        available_stand.available = False

        landing_plane = Plane(
            x_spawn,
            y_spawn,
            runway_path.heading,
            available_stand,
            state="landing",
        )

        landing_plane.drag = config.FLIGHT_DRAG
        landing_plane.speed = to_mps(150)
        landing_plane.thrust = 100
        config.PLANES.append(landing_plane)


def simulate_frame(screen):

    spawn_planes_for_landing()

    for plane in config.PLANES:
        if plane.state == "preparing":
            if random.randint(1, config.PUSHBACK_PROBABILITY) == 1:
                plane.update_state("pushback")

        plane.auto_move()
        plane.draw(screen)


def main():
    screen = setup()

    spawn_planes_at_stands()

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_airport(screen)
        simulate_frame(screen)

        # test_plane.move_manual()
        # test_plane.draw(screen)

        pygame.display.update()
        clock.tick(config.FPS)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
