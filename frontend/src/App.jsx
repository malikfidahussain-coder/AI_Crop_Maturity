// frontend/src/App.jsx
import { useEffect, useState, useRef } from "react";
import VideoCanvas from "./components/VideoCanvas";
import AnalysisPanel from "./components/AnalysisPanel"; // Import the new panel
import "./App.css";

function App() {
  const [detections, setDetections] = useState([]);
  const [videoFrame, setVideoFrame] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://127.0.0.1:8000/ws/detect");

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      setDetections(data.detections && data.detections.length > 0 ? data.detections : []);

      if (data.frame) {
        setVideoFrame(`data:image/jpeg;base64,${data.frame}`);
      }
    };

    ws.current.onclose = () => console.log("WebSocket Disconnected");
    
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>AI Crop Maturity Detection</h1>
        <div className="status">
          <span className="status-dot"></span>
          Camera Active
        </div>
      </header>

      {/* Group the canvas and panel side-by-side */}
      <main className="main-content" style={{ display: "flex", gap: "20px", justifyContent: "center", alignItems: "flex-start", padding: "20px" }}>
        <VideoCanvas detections={detections} frame={videoFrame} />
        <AnalysisPanel detections={detections} />
      </main>
    </div>
  );
}

export default App;