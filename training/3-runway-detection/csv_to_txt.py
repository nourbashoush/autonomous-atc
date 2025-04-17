import os
import csv

# Paths
CSV_FILE = "labels.csv"
IMAGES_DIR = "radar_images"
LABELS_DIR = "labels"

os.makedirs(LABELS_DIR, exist_ok=True)

# Read CSV and convert to YOLO format
with open(CSV_FILE, newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        filename, x_center, y_center, width, height = row

        # Convert values to YOLO format
        class_id = 0
        yolo_data = f"{class_id} {x_center} {y_center} {width} {height}\n"

        # Generate corresponding label file
        label_filename = os.path.splitext(filename)[0] + ".txt"
        label_path = os.path.join(LABELS_DIR, label_filename)

        with open(label_path, "w") as label_file:
            label_file.write(yolo_data)

print(f"YOLO labels saved in '{LABELS_DIR}'")
