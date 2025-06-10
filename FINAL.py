from ultralytics import YOLO
import cvzone
import cv2
import math
import serial

# Running real-time from webcam
s1 = s2 = s3 = s4 = 0
count = 0
cap = cv2.VideoCapture(1)
ser = serial.Serial('COM7', 9600)
# Load YOLOv8 model
model = YOLO('runs/detect/train3/weights/best.pt')

# Define class names (Ensure these match your trained model's labels)
classnames = ['grade1', 'grade2', 'grade3', 'grade4']

# count += 1
# if (count == 20):
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = cv2.resize(frame, (640, 480))
    
    # Perform object detection
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0].item()  # Convert to a Python float
            confidence = math.ceil(confidence * 100)

            Class = int(box.cls[0].item())  # Convert to Python int
            
            if Class < len(classnames):  # Ensure index is within bounds
                print(f"Confidence: {confidence}%")

                if confidence > 20:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to integers

                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

                    # Display class name and confidence
                    cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', 
                                    (x1 + 6, y1 + 18), scale=1.5, thickness=2)
                    
                    if classnames[Class] == "grade1":
                        s1+=1
                        if s1>=10:
                            ser.write(b'A')
                            print("A")
                            s1=0
                    
                    elif classnames[Class] == "grade2":
                        # s2=+1
                        # if s2>=10:
                            ser.write(b'B')
                            print("B")
                            # s2=0
                        
                    elif classnames[Class] == "grade3":
                        # s3=+1
                        # if s3>=10:
                            ser.write(b'C')
                            print("C")
                            # s3=0
                    
                    elif classnames[Class] == "grade4":
                        s4=+1
                        if s4>=10:
                            ser.write(b'D')
                            print("D")
                            s4 = 0
                    
                    print(f"Detected: {classnames[Class]}")
            # else:
            #     print(f"Warning: Detected an unknown class index {Class} (Not in classnames)")

    # Show frame
    cv2.imshow('Almond Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# if (count == 20):
#     count = 0
# Release resources
cap.release()
cv2.destroyAllWindows() 
