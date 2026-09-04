# backend/main.py
from fastapi import FastAPI
from backend.routes.analysis import router as analysis_router
from backend.routes.websocket import router as websocket_router

app = FastAPI(title="AI Crop Maturity Detection API")

# Register routes
app.include_router(analysis_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {"message": "AI Crop Detection Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}