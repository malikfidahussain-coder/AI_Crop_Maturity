import sys
import pathlib
import time  
import cv2
import torch

# Handle path systems across platforms
sys.modules['pathlib._local'] = pathlib
if sys.platform == 'win32':
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

MODEL_PATH = "models/detection/yolov5s_trained.pt"  
CONFIDENCE = 0.40

# SPEED OPTIMIZATION 1: Use GPU (CUDA/MPS) if available
device = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
print(f"Running inference on: {device.upper()}")

# Load model onto the selected device
model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path=MODEL_PATH,
    device=device
)
model.conf = CONFIDENCE

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

# SPEED OPTIMIZATION 2: Cap the camera capture stream size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # SPEED OPTIMIZATION 3: Force the neural network to evaluate at a lower resolution (320 or 640)
    results = model(rgb_frame, size=640)  
    detections = results.xyxy[0]

    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection.tolist()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        class_name = model.names[int(class_id)]

        # Draw bounding boxes
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # --- Calculate & Display FPS Counter ---
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show processed frame
    cv2.imshow("Fruit Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
