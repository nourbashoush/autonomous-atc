import math


def to_knots(mps):
    return mps * 1.94384


def to_mps(knots):
    return knots / 1.94384


def distance_between(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


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


def get_angle_between_points(point1, point2):
    return math.degrees(math.atan2(point2.y - point1.y, point2.x - point1.x))


def get_distance_from_path(plane, point1, point2):
    _, _, distance = closest_point_on_line(
        plane.x, plane.y, point1.x, point1.y, point2.x, point2.y
    )
    return distance


import matplotlib.pyplot as plt
from IPython.display import clear_output

plt.ion()


def plot(scores, mean_scores):
    clear_output(wait=True)
    plt.figure(figsize=(8, 5))
    plt.clf()
    plt.title("Training Progress")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")
    plt.axhline(0, color="gray", linewidth=0.5)
    plt.plot(scores, label="Score", color="blue")
    plt.plot(mean_scores, label="Mean Score", color="red")
    plt.legend()

    if scores:
        plt.text(len(scores) - 1, scores[-1], f"{scores[-1]:.3f}", color="blue")
    if mean_scores:
        plt.text(
            len(mean_scores) - 1, mean_scores[-1], f"{mean_scores[-1]:.3f}", color="red"
        )

    plt.show()
    plt.pause(0.1)
