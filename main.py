import random
import pygame
from plane import Plane
from airport import initialise_graph, render_airport
from utils import *
import configuration as config
from model_taxi_DQN import TaxiNet
from model_future_LSTM import PlaneTrajectoryLSTM, save_states_to_memory
from gui import render_ui
import cv2
from ultralytics import YOLO


def setup():
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(f"Airport Simulation - {config.AIRPORT_ICAO}")
    config.MARK_FONT = pygame.font.Font("assets/fonts/SpaceMono-Bold.ttf", 8)
    config.DATA_FONT = pygame.font.Font("assets/fonts/SpaceMono.ttf", 11)

    initialise_graph(f"data/airport_{config.AIRPORT_ICAO}.json")

    config.AIRPORT_IMG = pygame.image.load(f"assets/images/airport_{config.AIRPORT_ICAO}.jpg")
    config.GROUND_IMG = pygame.image.load(config.GROUND_IMG_PATH)
    config.AIRBORNE_IMG = pygame.image.load(config.AIRBORNE_IMG_PATH)

    taxi = TaxiNet()
    taxi.load()
    config.TAXI_MODEL = taxi

    lstm = PlaneTrajectoryLSTM()
    lstm.load()
    config.LSTM_MODEL = lstm

    yolo = YOLO(config.YOLO_MODEL_PATH)
    config.YOLO_MODEL = yolo

    return screen


def spawn_planes_at_stands():
    available_stands = [stand for stand in config.STAND_LIST if stand.available]
    selected_stands = random.sample(available_stands, min(10, len(available_stands)))

    for stand in selected_stands:
        new_plane = Plane(stand.x, stand.y, stand.heading, stand)
        dijkstra_path_start, path_distance_start = dijkstra(
            stand.parent.start.id, get_edge_object(config.TAKEOFF_RUNWAY).start.id
        )
        dijkstra_path_end, path_distance_end = dijkstra(
            stand.parent.end.id, get_edge_object(config.TAKEOFF_RUNWAY).start.id
        )
        if path_distance_start < path_distance_end:
            dijkstra_path = [stand.parent.end.id] + dijkstra_path_start
        else:
            dijkstra_path = [stand.parent.start.id] + dijkstra_path_end
        new_plane.path = dijkstra_path
        config.PLANES.append(new_plane)
        stand.available = False


def spawn_planes_for_landing(
    landing_frequency=config.FPS * config.TIME_BETWEEN_LANDINGS,
    distance_from_runway=to_pixels(config.LANDING_DISTANCE),
):
    update_landing_planes()

    if config.FRAME - config.LAST_SPAWN < landing_frequency:
        return

    if find_available_stand() and random.randint(1, config.LANDING_PROBABILITY) == 1:
        config.LAST_SPAWN = config.FRAME
        runway_path = get_edge_object(config.LANDING_RUNWAY)
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

        landing_plane.drag = config.LANDING_DRAG
        landing_plane.speed = to_mps(150)
        landing_plane.thrust = 72
        config.PLANES.append(landing_plane)


def simulate_frame(screen):

    spawn_planes_for_landing()

    for plane in config.PLANES:
        if plane.state == "preparing":
            if (
                safe_to_pushback(plane)
                and random.randint(1, config.PUSHBACK_PROBABILITY) == 1
            ):
                plane.state = "pushback"

        plane.auto_move()
        plane.draw(screen)

    is_final, is_approach, landing_plane = is_plane_on_final_approach()
    is_requested, requested_plane = is_runway_entry_requested()
    runway_occupied = is_runway_occupied()

    if runway_occupied:
        if is_final and not landing_plane.authority:
            landing_plane.state = "go_around"

    else:
        if is_approach and is_requested:
            if landing_plane.priority >= requested_plane.priority:
                landing_plane.authority = True
            else:
                requested_plane.authority = True
                config.PLANES_QUEUE_FOR_RUNWAY.remove(requested_plane)
                landing_plane.state = "go_around"

        elif is_final and not is_requested:
            landing_plane.authority = True

        elif not is_final and is_requested:
            requested_plane.authority = True
            config.PLANES_QUEUE_FOR_RUNWAY.remove(requested_plane)


def check_future_conflicts():
    planes = [
        plane
        for plane in config.PLANES
        if plane.future and plane.state not in ["landing", "takeoff", "rollout"]
    ]
    for plane in planes:
        for other_plane in planes:
            if plane != other_plane:
                if any(
                    check_collision(
                        plane.future[i][0],
                        plane.future[i][1],
                        other_plane.future[i][0],
                        other_plane.future[i][1],
                    )
                    for i in range(3)
                ) or (
                    check_collision(
                        plane.future[0][0],
                        plane.future[0][1],
                        other_plane.x,
                        other_plane.y,
                        seperation_distance=True,
                    )
                    and other_plane.speed == 0
                ):
                    plane_path_distance = get_distance_to_end(
                        [Node("", plane.x, plane.y)] + plane.path
                    )
                    other_plane_path = get_distance_to_end(
                        [Node("", other_plane.x, other_plane.y)] + other_plane.path
                    )
                    if plane_path_distance < other_plane_path:
                        other_plane.hold()
                    else:
                        plane.hold()


def safe_to_pushback(plane):
    position = get_stand_entrance(plane.stand)
    other_planes = [
        p
        for p in config.PLANES
        if p != plane
        and p.future
        and p.state not in ["landing", "takeoff", "rollout", "preparing"]
    ]
    for other_plane in other_planes:
        if any(
            check_collision(
                position.x,
                position.y,
                other_plane.future[i][0],
                other_plane.future[i][1],
            )
            for i in range(3)
        ):
            return False
    return True


def is_plane_on_final_approach():
    if config.LANDING_PLANES:
        landing_plane, distance = config.LANDING_PLANES[0]

        final_distance = to_pixels(config.FINAL_DISTANCE)
        approach_distance = to_pixels(config.APPROACH_DISTANCE)

        is_final = distance < final_distance
        is_approach = distance < approach_distance

        return (is_final, is_approach, landing_plane)

    return (False, False, None)


def is_runway_entry_requested():
    if config.PLANES_QUEUE_FOR_RUNWAY:
        sorted_planes = sorted(
            config.PLANES_QUEUE_FOR_RUNWAY, key=lambda p: p.priority, reverse=True
        )
        return (True, sorted_planes[0])

    return (False, None)


def is_runway_occupied():
    return config.RUNWAY_OCCUPATION > 0


def check_runway_availability(screen, radar_rect=pygame.Rect(0, 316, 1200, 90)):

    plane_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    noise_intensity = 150
    noise_background = np.random.randint(
        255 - noise_intensity,
        255,
        (screen.get_height(), screen.get_width(), 3),
        dtype=np.uint8,
    )
    noise_surface = pygame.surfarray.make_surface(noise_background)

    plane_surface.blit(noise_surface, (0, 0))

    for plane in config.PLANES:
        plane.draw(plane_surface, False, False)

    planes_array = pygame.surfarray.array3d(plane_surface)
    planes_array = np.transpose(planes_array, (1, 0, 2))

    radar_array = planes_array[
        radar_rect.y : radar_rect.y + radar_rect.height,
        radar_rect.x : radar_rect.x + radar_rect.width,
    ]

    radar_image = cv2.cvtColor(radar_array, cv2.COLOR_RGB2BGR)

    results = config.YOLO_MODEL(radar_image, verbose=False)

    config.BOUNDING_BOXES.clear()

    for result in results:
        boxes = result.boxes
        for box in boxes:
            top_left_x, top_left_y, bottom_right_x, bottom_right_y = map(
                int, box.xyxy[0]
            )

            x1 = top_left_x + radar_rect.x
            y1 = top_left_y + radar_rect.y
            x2 = bottom_right_x - top_left_x
            y2 = bottom_right_y - top_left_y

            config.BOUNDING_BOXES.append((x1, y1, x2, y2))

    config.RUNWAY_OCCUPATION = len(results[0].boxes) if results else 0


def main():
    screen = setup()

    spawn_planes_at_stands()

    running = True

    clock = pygame.time.Clock()

    while running:
        config.FRAME += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if config.FRAME % (config.FPS // 2) == 0:
            save_states_to_memory()
            for plane in config.PLANES:
                plane.predict_future_positions()

        if config.FRAME % config.HOLD_PERIOD == 0:
            check_future_conflicts()

        render_airport(screen)
        simulate_frame(screen)
        render_ui(screen)
        pygame.display.update()

        if config.FRAME % (config.FPS // 2) == 0:
            check_runway_availability(screen)

        if config.NORMAL_SPEED:
            clock.tick(config.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
