import json
import math
import pygame
import configuration as config

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
        self.start = start_node
        self.end = end_node
        self.distance = distance
        self.heading = heading

    def __repr__(self):
        return f"Edge({self.start.id} -> {self.end.id}, distance={self.distance:.2f}, heading={self.heading:.2f})"


def initialise_graph(json_file):
    nodes = {}
    edges = []

    def load_nodes(data):
        for node in data["nodes"]:
            new_node = Node(node["id"], node["x"], node["y"])
            nodes[new_node.id] = new_node

    def load_edges(data):
        for edge in data["edges"]:
            start_node = nodes[edge["from"]]
            end_node = nodes[edge["to"]]
            distance = calculate_distance(start_node, end_node)
            heading = calculate_heading(start_node, end_node)
            edges.append(Edge(start_node, end_node, distance, heading))

    def calculate_distance(node1, node2):
        return math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)

    def calculate_heading(node1, node2):
        angle = math.degrees(math.atan2(node2.y - node1.y, node2.x - node1.x))
        return (angle + 90) % 360  # Normalize to 0-360 degrees
    
    # def calculate_heading(node1, node2):
    #     """
    #     Calculates the heading (angle) in degrees from node1 to node2.
    #     Adjusts for screen coordinate system where the y-axis is inverted.
    #     """
    #     dx = node2.x - node1.x
    #     dy = node1.y - node2.y  # Invert the y-difference due to screen coordinates
    #     angle = math.degrees(math.atan2(dy, dx))
    #     return (angle + 360) % 360  # Normalize to 0-360 degrees

    with open(json_file, "r") as file:
        data = json.load(file)
        load_nodes(data)
        load_edges(data)

    return list(nodes.values()), edges


def draw_nodes(screen):
    """
    Draw nodes as circles with their IDs labeled.
    :param screen: The pygame screen object.
    :param nodes: List of Node objects.
    :param font: A pygame font object for rendering text.
    """
    for node in config.NODE_LIST:
        # Draw a small circle at the node's location
        pygame.draw.circle(screen, (255, 0, 0), (node.x, node.y), 5)

        # Render the node ID as text to the right of the circle
        label = config.FONT.render(str(node.id), True, (255, 255, 255))
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
