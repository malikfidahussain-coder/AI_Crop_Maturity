# cv/camera.py
import cv2

class Camera:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        # Cap stream size to match optimization in previous detection script
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def read_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def release(self):
        if self.cap.isOpened():
            self.cap.release()