// frontend/src/components/VideoCanvas.jsx
import DetectionOverlay from "./DetectionOverlay";

function VideoCanvas({ detections, frame }) {
  return (
    <div className="video-container" style={{ position: "relative", width: "640px", height: "480px" }}>
      
      {/* Live streaming frame from backend */}
      {frame ? (
        <img 
          src={frame} 
          alt="Live Camera Feed" 
          style={{ width: "100%", height: "100%", objectFit: "cover" }} 
        />
      ) : (
        <div style={{ width: "100%", height: "100%", background: "#222", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <p>Connecting to Camera...</p>
        </div>
      )}

      {/* HARD DOM RESET: This container only exists if crops are actively detected */}
      {detections && detections.length > 0 && (
        <div className="overlay-kill-switch">
          {detections.map((detection, index) => (
            <DetectionOverlay
              // Combining object_id and index prevents any lingering React key collisions
              key={`${detection.object_id}-${index}`}
              detection={detection}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default VideoCanvas;