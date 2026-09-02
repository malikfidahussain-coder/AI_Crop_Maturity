import cv2
import torch

MODEL_PATH = "models/detection/yolov5s_trained.pt"  # Ensure this file is in this folder path
CONFIDENCE = 0.50

import sys
import pathlib
sys.modules['pathlib._local'] = pathlib
if sys.platform == 'win32':
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath


# 1. Load the model using PyTorch Hub automatically
model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=MODEL_PATH
)
model.conf = CONFIDENCE

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")


while True:
    success, frame = cap.read()

    if not success:
        break

    # Convert BGR (OpenCV standard) to RGB (YOLOv5 standard)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run inference on RGB frame
    results = model(rgb_frame)
    detections = results.xyxy[0]

    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection.tolist()

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        class_id = int(class_id)

        class_name = model.names[class_id]

        # Draw on the original 'frame' (since OpenCV displays BGR)
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        label = f"{class_name} {confidence:.2f}"

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Show processed frame
    cv2.imshow("Fruit Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
