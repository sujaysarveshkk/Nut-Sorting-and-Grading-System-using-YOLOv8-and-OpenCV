import cv2
from ultralytics import YOLO
# import serial

# Load the trained YOLOv8 model
model = YOLO("runs/detect/train3/weights/best.pt")
# ser = serial.Serial('COM3', 9600)
# Open webcam (0 is the default camera, change if using an external one)
cap = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Perform detection
    results = model(frame)

    # Plot results on the frame
    annotated_frame = results[0].plot()

    # Display the frame with detections
    cv2.imshow("Almond Detection", annotated_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
