import cv2
import os

# Define dataset paths (Update these paths)
image_folder = "Augmented_Dataset/Grade_2"  # Change this to your dataset path
annotation_folder = "Augmented_Dataset/Grade_2"  # Same as image folder

# Get all images
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    annotation_path = os.path.join(annotation_folder, image_file.replace('.jpg', '.txt'))

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        continue

    h, w, _ = image.shape  # Image dimensions
    bboxes = []  # Store bounding boxes

    if os.path.exists(annotation_path):
        with open(annotation_path, "r") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Invalid annotation in {annotation_path}: {line}")
                    continue

                class_id = int(parts[0])
                x_center, y_center, bbox_width, bbox_height = map(float, parts[1:])

                # Convert YOLO format to pixel values
                x1 = int((x_center - bbox_width / 2) * w)
                y1 = int((y_center - bbox_height / 2) * h)
                x2 = int((x_center + bbox_width / 2) * w)
                y2 = int((y_center + bbox_height / 2) * h)

                # Append bounding box to list
                bboxes.append((x1, y1, x2, y2, class_id))

    # Print the bounding boxes for verification
    print(f"Bounding Boxes for {image_file}: {bboxes}")


    # Draw bounding boxes
    for (x1, y1, x2, y2, class_id) in bboxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(class_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show image with bounding boxes
    cv2.imshow("Bounding Box Check", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()

