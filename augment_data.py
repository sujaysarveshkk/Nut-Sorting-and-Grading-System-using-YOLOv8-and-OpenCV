import os
import cv2
import albumentations as A
import numpy as np

# Define the augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),      
    A.VerticalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.Rotate(limit=30, p=0.5),
    A.GaussianBlur(blur_limit=(3, 7), p=0.2),
    A.RandomScale(scale_limit=0.2, p=0.3),
    A.GaussNoise(var_limit=(10, 50), p=0.3)



], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))  # Important for YOLO

# Input and output paths
base_dir = "Dataset_Base"
output_dir = "Augmented_Dataset"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

num_aug_per_image = 1000  # Number of augmentations per image

# Process each grade folder
for grade in os.listdir(base_dir):
    grade_path = os.path.join(base_dir, grade)
    output_grade_path = os.path.join(output_dir, grade)

    if not os.path.exists(output_grade_path):
        os.makedirs(output_grade_path)

    for img_name in os.listdir(grade_path):
        if not img_name.endswith(".jpg"):  # Only process image files
            continue

        img_path = os.path.join(grade_path, img_name)
        txt_path = img_path.replace(".jpg", ".txt")  # YOLO annotation file

        image = cv2.imread(img_path)
        if image is None:
            print(f"Could not read {img_path}, skipping...")
            continue

        h, w, _ = image.shape  # Image dimensions

        # Read annotation file if it exists
        bboxes = []
        class_labels = []
        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id = int(parts[0])
                        x, y, bw, bh = map(float, parts[1:])
                        bboxes.append([x, y, bw, bh])
                        class_labels.append(class_id)

        for i in range(num_aug_per_image):
            augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            aug_image = augmented['image']
            aug_bboxes = augmented['bboxes']

            # Save augmented image
            aug_img_name = f"aug_{i}_{img_name}"
            aug_img_path = os.path.join(output_grade_path, aug_img_name)
            cv2.imwrite(aug_img_path, aug_image)

            # Save augmented annotation file
            if bboxes:
                aug_txt_name = aug_img_name.replace(".jpg", ".txt")
                aug_txt_path = os.path.join(output_grade_path, aug_txt_name)

                with open(aug_txt_path, "w") as f:
                    for bbox, label in zip(aug_bboxes, class_labels):
                        f.write(f"{label} {' '.join(map(str, bbox))}\n")

print("Augmentation complete! Images and YOLO annotations saved.")


