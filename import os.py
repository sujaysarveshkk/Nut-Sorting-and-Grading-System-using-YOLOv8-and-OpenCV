import os
import shutil
import random

# Set paths
dataset_path = "C:/Users/matha/Downloads/B0187/Almond_Dataset"
train_img_dir = os.path.join(dataset_path, "train/images")
train_lbl_dir = os.path.join(dataset_path, "train/labels")
valid_img_dir = os.path.join(dataset_path, "valid/images")
valid_lbl_dir = os.path.join(dataset_path, "valid/labels")

# Ensure valid directories exist
os.makedirs(valid_img_dir, exist_ok=True)
os.makedirs(valid_lbl_dir, exist_ok=True)

# Get list of images
image_files = [f for f in os.listdir(train_img_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

# Select 20% of images randomly for validation
valid_sample_size = int(0.2 * len(image_files))
valid_images = random.sample(image_files, valid_sample_size)

# Move selected images and labels to valid/ directory
for img in valid_images:
    img_path = os.path.join(train_img_dir, img)
    lbl_path = os.path.join(train_lbl_dir, img.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt"))

    # Move image
    shutil.move(img_path, os.path.join(valid_img_dir, img))

    # Move label (if it exists)
    if os.path.exists(lbl_path):
        shutil.move(lbl_path, os.path.join(valid_lbl_dir, os.path.basename(lbl_path)))

print(f"Moved {valid_sample_size} images and labels to validation set.")
