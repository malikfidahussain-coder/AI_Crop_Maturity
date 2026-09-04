# backend/routes/analysis.py
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File
from backend.services.pipeline import DetectionPipeline
from backend.schemas.detection import DetectionResponse

router = APIRouter(prefix="/analysis", tags=["Analysis"])
pipeline = DetectionPipeline()

@router.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    image_array = np.frombuffer(contents, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image"}

    result = pipeline.process_frame(frame)
    return result