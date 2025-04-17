import pygame
import cv2
import numpy as np
import random
import os
import csv

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 600))

# Load Images
original_background = pygame.image.load("airport_EGBB.jpg")
plane_image = pygame.image.load("plane_ground.png")

# Define Radar Section
radar_rect = pygame.Rect(0, 316, 1200, 90)

# Plane Variables
plane_width, plane_height = plane_image.get_size()

# Create folders
os.makedirs("radar_images", exist_ok=True)

# CSV file setup
csv_filename = "labels.csv"
csv_exists = os.path.exists(csv_filename)


def augment_background(noise_intensity=0.07):
    background = pygame.surfarray.array3d(original_background)
    background = np.transpose(background, (1, 0, 2))  # Convert to (Height, Width, RGB)
    background = cv2.cvtColor(background, cv2.COLOR_RGB2BGR)

    # Apply Random Rotation
    angle = random.uniform(-2, 2)
    center = (background.shape[1] // 2, background.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    background = cv2.warpAffine(
        background, rotation_matrix, (background.shape[1], background.shape[0])
    )

    # Apply Small Brightness & Contrast Adjustments
    brightness = random.uniform(0.95, 1.05)
    contrast = random.uniform(0.95, 1.05)
    background = np.clip((background * contrast) + (brightness * 30), 0, 255).astype(
        np.uint8
    )

    # Add Noise with Adjustable Intensity
    if noise_intensity > 0:
        noise = np.random.normal(0, noise_intensity * 10, background.shape).astype(
            np.uint8
        )
        background = cv2.add(background, noise)

    # Convert back to Pygame format
    background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
    return pygame.surfarray.make_surface(np.transpose(background, (1, 0, 2)))


def generate_plane_position(image_count):
    include_plane = image_count % 2 == 0

    if include_plane:
        plane_x = random.randint(
            radar_rect.x, radar_rect.x + radar_rect.width
        )
        plane_y = random.randint(
            radar_rect.y, radar_rect.y + radar_rect.height
        )
        plane_heading = random.uniform(0, 360)
        return include_plane, plane_x, plane_y, plane_heading
    return include_plane, None, None, None  # No plane case


def capture_radar_section(image_count):
    pygame.display.flip()
    screen_surface = pygame.display.get_surface()
    screen_array = pygame.surfarray.array3d(screen_surface)
    screen_array = np.transpose(screen_array, (1, 0, 2))

    # Extract only the radar section
    radar_image = screen_array[
        radar_rect.y : radar_rect.y + radar_rect.height,
        radar_rect.x : radar_rect.x + radar_rect.width,
    ]

    # Convert from RGB (Pygame) to BGR (OpenCV)
    radar_image = cv2.cvtColor(radar_image, cv2.COLOR_RGB2BGR)

    image_filename = f"radar_{image_count}.png"
    image_path = os.path.join("radar_images", image_filename)
    cv2.imwrite(image_path, radar_image)

    return image_filename


def save_label(image_filename, plane_x, plane_y):
    csv_filename = "labels.csv"
    file_exists = os.path.exists(csv_filename)

    if radar_rect.collidepoint(plane_x, plane_y):
        img_width, img_height = radar_rect.width, radar_rect.height
        x_norm = (plane_x - radar_rect.x) / img_width
        y_norm = (plane_y - radar_rect.y) / img_height
        w_norm = plane_width / img_width
        h_norm = plane_height / img_height

        with open(csv_filename, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)

            if not file_exists:
                csv_writer.writerow(
                    ["filename", "x_center", "y_center", "width", "height"]
                )

            csv_writer.writerow([image_filename, x_norm, y_norm, w_norm, h_norm])
            print(f"Saved: {image_filename} with plane label in {csv_filename}")
    else:
        print(f"Saved: {image_filename} (NO PLANE)")


def main_loop(num_images):
    running = True
    image_count = 0

    while image_count < num_images and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step 1: Augment Background
        background_surface = augment_background()

        # Step 2: Generate Plane Position
        include_plane, plane_x, plane_y, plane_heading = generate_plane_position(image_count)

        # Step 3: Draw Everything
        screen.blit(background_surface, (0, 0))

        if include_plane:
            rotated_plane = pygame.transform.rotate(plane_image, -plane_heading)
            plane_rect = rotated_plane.get_rect(center=(plane_x, plane_y))
            screen.blit(rotated_plane, plane_rect.topleft)

        # Step 4: Capture Radar Section
        image_filename = capture_radar_section(image_count)

        # Step 5: Save Label (Only if Plane is Inside Radar)
        if include_plane:
            save_label(image_filename, plane_x, plane_y)

        image_count += 1


main_loop(num_images=5_000)

pygame.quit()
