# AI Crop Maturity Detection System

## Overview
This is a real-time computer vision pipeline designed to analyze crops (tomatoes, mangoes, strawberries) through a live webcam. It provides object detection, persistence tracking, maturity scoring, and harvest predictions without requiring cloud deployment.

## Technology Stack
- **AI & Computer Vision:** YOLOv5 (PyTorch), OpenCV, NumPy
- **Backend Pipeline:** Python, FastAPI, WebSockets
- **Frontend:** React, Vite
- **Data Management:** YAML (Crop Knowledge Base)

## System Architecture
- **Video Capture:** OpenCV captures local webcam frames.
- **Object Detection:** YOLOv5 identifies the crop bounding boxes and confidence scores.
- **Centroid Tracking:** A custom tracker assigns persistent IDs to prevent duplicate scanning.
- **Maturity Engine:** Extracts the Region of Interest (ROI) and applies a Level 1 Computer Vision baseline (HSV color masking) to calculate a maturity score and stage.
- **Harvest Engine:** Maps the detected crop and maturity stage against `crops.yaml` to predict harvest readiness.
- **WebSocket Streaming:** FastAPI continuously encodes the video frames (Base64) and structured JSON analysis payload to the frontend.
- **React Dashboard:** Renders the live video feed with synced bounding boxes and a real-time analysis data panel.

## Repository Structure
```text
AI_Crop_Maturity/
├── analysis/
│   ├── harvest/
│   └── maturity/
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── schemas/
│   └── services/
├── config/
│   └── crops.yaml
├── cv/
│   ├── camera.py
│   ├── detector.py
│   ├── preprocessing.py
│   └── tracker.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── models/
    ├── detection/
    └── maturity/
```

## Installation & Setup

```bash
# 1. Setup Python Virtual Environment and Install Dependencies
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt

# 2. Start the FastAPI Backend
cd backend
uvicorn main:app --reload

# 3. Setup and Start the Frontend
cd ../frontend
npm install
npm run dev
```