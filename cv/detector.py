import sys
import pathlib
import cv2
import torch


# Handle path systems across platforms
sys.modules["pathlib._local"] = pathlib

if sys.platform == "win32":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath


MODEL_PATH = "models/detection/yolov5s_trained.pt"
CONFIDENCE = 0.40


class FruitDetector:

    def __init__(self):
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else (
                "mps"
                if torch.backends.mps.is_available()
                else "cpu"
            )
        )

        print(f"Running inference on: {self.device.upper()}")

        self.model = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=MODEL_PATH,
            device=self.device
        )

        self.model.conf = CONFIDENCE

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.model(
            rgb_frame,
            size=640
        )

        detections = []

        for detection in results.xyxy[0]:

            x1, y1, x2, y2, confidence, class_id = detection.tolist()

            class_id = int(class_id)

            detections.append({
                "crop": self.model.names[class_id],
                "confidence": round(confidence, 2),
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ]
            })

        return detections