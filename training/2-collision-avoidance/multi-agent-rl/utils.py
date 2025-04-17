import math
import heapq
import configuration as config
import numpy as np
import random


class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Node({self.id}, x={self.x}, y={self.y})"


class Edge:
    def __init__(self, start_node, end_node, distance, heading):
        self.id = f"{start_node.id}-{end_node.id}"
        self.start = start_node  # Node object
        self.end = end_node  # Node object
        self.distance = distance
        self.heading = heading

    def __repr__(self):
        return f"Edge({self.start.id} -> {self.end.id}, distance={self.distance:.2f}, heading={self.heading:.2f})"


class Stand:
    def __init__(self, stand_id, x, y, heading, parent):
        self.id = stand_id
        self.x = x
        self.y = y
        self.heading = heading
        self.parent = parent  # Edge object with order to follow to leave the stand
        self.available = True

    def __repr__(self):
        return f"Stand({self.id})"


def to_knots(mps):
    return mps * 1.94384


def to_mps(knots):
    return knots / 1.94384


def distance_between(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def distance_between_points(point1_x, point1_y, point2_x, point2_y):
    return math.sqrt((point1_x - point2_x) ** 2 + (point1_y - point2_y) ** 2)


def get_node_object(node_id):
    if isinstance(node_id, Node) or isinstance(node_id, Stand):
        return node_id
    return config.NODE_DICT[node_id]


def get_edge_object(edge_id):
    return config.EDGE_DICT[edge_id]


# def get_edge_object(node1, node2):
#     return config.EDGE_DICT[f"{node1}-{node2}"]


def dijkstra(start_node_id, end_node_id):

    nodes = config.NODE_LIST
    edges = config.EDGE_LIST

    # Map nodes by their IDs for quick lookup
    node_map = {node.id: node for node in nodes}
    adjacency_list = {node.id: [] for node in nodes}

    # Build the adjacency list
    for edge in edges:
        adjacency_list[edge.start.id].append((edge.end.id, edge.distance))

    # Priority queue to store (distance, node_id)
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node_id))

    # Dictionary to store the shortest distance to each node
    distances = {node.id: float("inf") for node in nodes}
    distances[start_node_id] = 0

    # Dictionary to store the path
    previous_nodes = {node.id: None for node in nodes}

    while priority_queue:
        current_distance, current_node_id = heapq.heappop(priority_queue)

        # If we reach the end_node, stop early
        if current_node_id == end_node_id:
            break

        # Process each neighbour
        for neighbour_id, edge_distance in adjacency_list[current_node_id]:
            new_distance = current_distance + edge_distance
            if new_distance < distances[neighbour_id]:
                distances[neighbour_id] = new_distance
                previous_nodes[neighbour_id] = current_node_id
                heapq.heappush(priority_queue, (new_distance, neighbour_id))

    # Reconstruct the shortest path
    path = []
    current = end_node_id
    while current:
        path.append(current)
        current = previous_nodes[current]

    path.reverse()  # Reverse to get the path from start to end
    return path, distances[end_node_id]


def closest_point_on_line(x, y, a1, a2, b1, b2):
    # Vector AB
    ABx, ABy = b1 - a1, b2 - a2
    # Vector AP
    APx, APy = x - a1, y - a2
    # Length squared of AB
    AB_len_sq = ABx**2 + ABy**2

    if AB_len_sq == 0:  # A and B are the same point
        return (a1, a2, math.sqrt((x - a1) ** 2 + (y - a2) ** 2))

    # Projection factor t
    t = (APx * ABx + APy * ABy) / AB_len_sq
    # Clamp t to the range [0, 1]
    t = max(0, min(1, t))

    # Closest point on AB
    closest_x = a1 + t * ABx
    closest_y = a2 + t * ABy

    # Distance to closest point
    distance = math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)

    return (closest_x, closest_y, distance)


def get_taxi_state(plane):
    plane_x, plane_y = plane.x, plane.y
    next_node = get_node_object(plane.path[0])
    prev_node = get_node_object(plane.visited[-1])

    angles = [-90, 0, 90]
    distances = []

    for angle in angles:
        absolute_angle = (plane.heading + angle - 90) % 360
        radian_angle = math.radians(absolute_angle)

        dx, dy = math.cos(radian_angle), math.sin(radian_angle)

        current_x, current_y = plane_x, plane_y
        step_size = 1

        while True:
            current_x += dx * step_size
            current_y += dy * step_size

            _, _, distance_to_path = closest_point_on_line(
                current_x,
                current_y,
                prev_node.x,
                prev_node.y,
                next_node.x,
                next_node.y,
            )

            if distance_to_path >= config.MAX_DEVIATION:
                break

        distance_to_boundary = distance_between_points(
            plane_x, plane_y, current_x, current_y
        )
        distances.append(distance_to_boundary)

    distances = np.array(distances) / 150.0

    delta_x = next_node.x - plane_x
    delta_y = next_node.y - plane_y
    angle_to_target = (math.degrees(math.atan2(delta_y, delta_x)) + 360) % 360
    angle_diff = (angle_to_target - plane.heading + 90) % 360

    if angle_diff > 180:
        angle_diff -= 360
    turn_angle = angle_diff / 180

    speed = plane.speed / 100.0

    distance_to_target = (
        distance_between_points(plane_x, plane_y, next_node.x, next_node.y) / 150.0
    )

    thrust = plane.thrust / 100

    state = np.append(
        distances,
        [turn_angle, speed, distance_to_target, thrust],
    )

    return state.astype(np.float32)


def find_available_stand():
    available_stands = [stand for stand in config.STAND_LIST if stand.available]
    if available_stands:
        return random.choice(available_stands)
    return False


def is_exit_ahead(plane, exit):
    exit_node = get_node_object(exit)
    radian_heading = math.radians(plane.heading)
    plane_to_exit_x = exit_node.x - plane.x
    plane_to_exit_y = exit_node.y - plane.y
    dot_product = plane_to_exit_x * math.sin(
        radian_heading
    ) + plane_to_exit_y * -math.cos(radian_heading)
    return dot_product > 0


def get_stand_entrance(stand):
    if stand is None:
        return None

    x, y, _ = closest_point_on_line(
        stand.x,
        stand.y,
        stand.parent.start.x,
        stand.parent.start.y,
        stand.parent.end.x,
        stand.parent.end.y,
    )

    return Node(f"{stand.id}-entrance", x, y)


def angle_between(point1, point2):
    return math.degrees(math.atan2(point2.y - point1.y, point2.x - point1.x))


def check_collision(plane_x, plane_y, other_x, other_y):
    distance = distance_between_points(plane_x, plane_y, other_x, other_y)
    return distance < config.COLLISION_THRESHOLD


def get_distance_to_end(path):
    distance = 0
    for i in range(len(path) - 1):
        start_node = get_node_object(path[i])
        end_node = get_node_object(path[i + 1])
        distance += distance_between(start_node, end_node)
    return distance


def snap_to_path(path, x, y):
    closest_distance = float("inf")
    closest_x, closest_y = None, None

    for i in range(len(path) - 1):
        start_node = get_node_object(path[i])
        end_node = get_node_object(path[i + 1])

        x_snap, y_snap, distance = closest_point_on_line(
            x, y, start_node.x, start_node.y, end_node.x, end_node.y
        )

        if distance < closest_distance:
            closest_distance = distance
            closest_x, closest_y = x_snap, y_snap

    return closest_x, closest_y
