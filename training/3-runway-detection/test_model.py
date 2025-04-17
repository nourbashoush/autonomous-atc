from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

image_path = "radar_images/radar_2.png"
results = model(image_path)


for result in results:
    boxes = result.boxes
    for box in boxes:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = map(
            int, box.xyxy[0]
        )  # Top-left (x1, y1) and bottom-right (x2, y2)
        x_center, y_center, width, height = map(
            int, box.xywh[0]
        )  # Center (x, y) and box size

        conf = box.conf[0].item()
        class_id = int(box.cls[0].item())

        print(f"Detected Class: {class_id}, Confidence: {conf:.2f}")
        print(f"Top-Left: ({x1}, {y1}), Bottom-Right: ({x2}, {y2})")
        print(f"Center: ({x_center}, {y_center}), Width: {width}, Height: {height}")
        print("-" * 50)