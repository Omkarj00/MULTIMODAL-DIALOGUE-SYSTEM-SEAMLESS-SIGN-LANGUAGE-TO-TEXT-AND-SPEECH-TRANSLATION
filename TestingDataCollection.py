import cv2
import numpy as np
import os

# Constants
MODE = 'trainingData'
DIRECTORY = r'C:/Users/Omkar Jagtap/OneDrive/Desktop/data collection/dataSet/' + MODE
LABELS = ['0'] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]
ROI_SIZE = (300, 300)
MIN_VALUE = 70

# Function to create directories for labels
def ensure_directories(base_dir, labels):
    for label in labels:
        label_dir = os.path.join(base_dir, label)
        os.makedirs(label_dir, exist_ok=True)

# Initialize directories
ensure_directories(DIRECTORY, LABELS)

# Start video capture
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to access the camera. Exiting...")
        break

    # Mirror the frame
    frame = cv2.flip(frame, 1)

    # Count existing images for each label
    count = {label: len(os.listdir(os.path.join(DIRECTORY, label))) for label in LABELS}

    # Display counts on the frame
    for idx, label in enumerate(LABELS):
        cv2.putText(frame, f"{label}: {count[label]}", (10, 60 + idx * 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)

    # Define ROI coordinates
    x1, y1 = int(0.5 * frame.shape[1]), 10
    x2, y2 = frame.shape[1] - 10, int(0.5 * frame.shape[1])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Extract and process the ROI
    roi = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    _, test_image = cv2.threshold(th3, MIN_VALUE, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    test_image = cv2.resize(test_image, ROI_SIZE)

    # Display processed ROI and original frame
    cv2.imshow("Processed ROI", test_image)
    cv2.imshow("Frame", frame)

    # Handle key presses
    interrupt = cv2.waitKey(10) & 0xFF
    if interrupt == 27:  # ESC to exit
        print("Exiting...")
        break

    # Save image if corresponding label key is pressed
    for label in LABELS:
        if interrupt == ord(label.lower()):
            save_path = os.path.join(DIRECTORY, label, f"{count[label]}.jpg")
            cv2.imwrite(save_path, test_image)
            print(f"Image saved: {save_path}")
            cv2.putText(frame, "Saved!", (x1 + 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Release resources
capture.release()
cv2.destroyAllWindows()

