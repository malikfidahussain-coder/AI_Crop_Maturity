import asyncio
import base64
import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.pipeline import DetectionPipeline
from cv.camera import Camera

router = APIRouter(tags=["Real-Time Analysis"])
pipeline = DetectionPipeline()

@router.websocket("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    camera = Camera(source=0)
    
    try:
        while True:
            frame = camera.read_frame()
            if frame is None:
                break
                
            # 1. Get structured JSON detections
            result = pipeline.process_frame(frame)
            
            # 2. Encode the frame as a Base64 JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # 3. Send both the image and the detections
            payload = {
                "detections": result["detections"],
                "frame": frame_base64
            }
            await websocket.send_json(payload)
            
            # Yield control to event loop (~30 FPS max)
            await asyncio.sleep(0.03) 
            
    except WebSocketDisconnect:
        print("Frontend client disconnected.")
    finally:
        camera.release()