# backend/schemas/detection.py
from pydantic import BaseModel
from typing import List, Optional

class DetectionItem(BaseModel):
    object_id: Optional[str]
    crop: str
    confidence: float
    bbox: List[int]

class DetectionResponse(BaseModel):
    detections: List[DetectionItem]