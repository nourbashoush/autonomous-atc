import os
import shutil
import random

IMAGES_DIR = "radar_images"  # Where all images are stored
LABELS_DIR = "labels"  # Where YOLO labels are stored
DATASET_DIR = "dataset"  # Main dataset folder

TRAIN_RATIO = 0.8  # 80% training, 20% validation

os.makedirs(f"{DATASET_DIR}/images/train", exist_ok=True)
os.makedirs(f"{DATASET_DIR}/images/val", exist_ok=True)
os.makedirs(f"{DATASET_DIR}/labels/train", exist_ok=True)
os.makedirs(f"{DATASET_DIR}/labels/val", exist_ok=True)

all_images = [f for f in os.listdir(IMAGES_DIR) if f.endswith(".png")]

random.shuffle(all_images)
split_index = int(len(all_images) * TRAIN_RATIO)
train_images = all_images[:split_index]
val_images = all_images[split_index:]


def move_files(image_list, split_type):
    for image in image_list:
        src_img = os.path.join(IMAGES_DIR, image)
        dst_img = os.path.join(DATASET_DIR, "images", split_type, image)
        shutil.copy(src_img, dst_img)

        label_file = os.path.splitext(image)[0] + ".txt"
        src_label = os.path.join(LABELS_DIR, label_file)
        dst_label = os.path.join(DATASET_DIR, "labels", split_type, label_file)

        if os.path.exists(src_label):
            shutil.copy(src_label, dst_label)

move_files(train_images, "train")
move_files(val_images, "val")

print(
    f"Dataset organised: {len(train_images)} training images, {len(val_images)} validation images."
)
