import json
import math
import pygame
import configuration as config
from utils import *


def initialise_graph(json_file):
    nodes = {}
    edges = []
    stands = {}

    def load_nodes(data):
        for node in data["nodes"]:
            new_node = Node(node["id"], node["x"], node["y"])

            if node["id"] in data["holding_points"]:
                new_node.holding_point = True

            nodes[new_node.id] = new_node

        config.NODE_LIST = list(nodes.values())
        config.NODE_DICT = nodes

    def load_edges(data):
        for edge in data["edges"]:
            start_node = nodes[edge["from"]]
            end_node = nodes[edge["to"]]
            distance = calculate_distance(start_node, end_node)
            heading = calculate_heading(start_node, end_node)
            edges.append(Edge(start_node, end_node, distance, heading))
            edges.append(Edge(end_node, start_node, distance, (heading + 180) % 360))

        config.EDGE_LIST = edges
        config.EDGE_DICT = {edge.id: edge for edge in edges}

    def load_stands(data):
        for stand in data["stands"]:
            new_stand = Stand(
                stand["id"],
                stand["x"],
                stand["y"],
                stand["heading"],
                get_edge_object(stand["parent"]),
            )
            stands[new_stand.id] = new_stand

        config.STAND_LIST = list(stands.values())
        config.STAND_DICT = stands

    def load_runway_exits(data):
        for runway in data["runway_exits"]:
            config.EXIT_DICT[runway["id"]] = runway["exits"]

    def calculate_distance(node1, node2):
        return math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)

    def calculate_heading(node1, node2):
        angle = math.degrees(math.atan2(node2.y - node1.y, node2.x - node1.x))
        return (angle + 90) % 360

    with open(json_file, "r") as file:
        data = json.load(file)
        load_nodes(data)
        load_edges(data)
        load_stands(data)
        load_runway_exits(data)


def render_airport(screen):
    screen.blit(config.AIRPORT_IMG, (0, 0))

    if config.RENDER_EDGES:
        draw_edges(screen)
    if config.RENDER_NODES:
        draw_nodes(screen)
    if config.RENDER_STANDS:
        draw_stands(screen)
    if config.RENDER_BOXES:
        draw_bounding_boxes(screen)

    show_next_landing_aircraft(screen)


def show_next_landing_aircraft(screen):

    def behind_threshold(plane):
        delta_x = plane.x - threshold.x
        delta_y = plane.y - threshold.y
        angle_to_plane = (math.degrees(math.atan2(delta_y, delta_x)) + 360) % 360

        inverse_runway_heading = get_edge_object(config.LANDING_RUNWAY).heading - 180

        angle_diff = (angle_to_plane - inverse_runway_heading - 270) % 360

        angle_diff -= 360 if angle_diff > 180 else 0
        angle_diff = math.radians(angle_diff)

        return math.cos(angle_diff) > 0

    landing_planes = [plane for plane in config.PLANES if plane.state == "landing"]

    threshold = get_edge_object(config.LANDING_RUNWAY).start
    distance = float("inf")

    text = f"X [{len(landing_planes)}]"

    for plane in landing_planes:
        if behind_threshold(plane) and distance_between(plane, threshold) < distance:
            distance = distance_between(plane, threshold)
            text = f"{(distance / config.PIXEL_TO_METRE)/1000:.2f}km [{len(landing_planes)}]"

    label = config.MARK_FONT.render(text, True, (255, 255, 255))
    screen.blit(label, (threshold.x - 15, threshold.y - 30))


def draw_nodes(screen):
    """
    Draw nodes as circles with their IDs labeled.
    :param screen: The pygame screen object.
    :param nodes: List of Node objects.
    :param font: A pygame font object for rendering text.
    """
    for node in config.NODE_LIST:
        # Draw a small circle at the node's location
        pygame.draw.circle(screen, (255, 0, 0), (node.x, node.y), 3)

        # Render the node ID as text to the right of the circle
        label = config.MARK_FONT.render(str(node.id), True, (255, 255, 255))
        screen.blit(
            label, (node.x + 5, node.y - 5)
        )  # Offset slightly to the right and up


def draw_edges(screen):
    """
    Draw edges as lines connecting the nodes.
    :param screen: The pygame screen object.
    :param edges: List of Edge objects.
    """
    for edge in config.EDGE_LIST:
        # Draw a line between the two nodes
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (edge.start.x, edge.start.y),
            (edge.end.x, edge.end.y),
            1,
        )


def draw_stands(screen):
    """
    Draw stands as rectangles with their IDs labeled.
    :param screen: The pygame screen object.
    :param stands: List of Stand objects.
    :param font: A pygame font object for rendering text.
    """
    for stand in config.STAND_LIST:
        # Draw a rectangle at the stand's location
        pygame.draw.rect(screen, (0, 0, 255), (stand.x - 1, stand.y - 1, 2, 2))

        # Render the stand ID as text above the rectangle
        label = config.MARK_FONT.render(str(stand.id), True, (255, 255, 255))
        screen.blit(
            label, (stand.x - 5, stand.y - 15)
        )  # Offset slightly up from the rectangle


def draw_bounding_boxes(screen):
    for box in config.BOUNDING_BOXES:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(box),
            2,
        )
