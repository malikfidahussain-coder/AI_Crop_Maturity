import DetectionOverlay from "./DetectionOverlay";

function VideoCanvas({ detections, videoRef }) {
  return (
    <div className="video-container">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="camera-video"
      />

      {detections.length > 0 && (
        <div className="overlay-layer">
          {detections.map((detection, index) => (
            <DetectionOverlay
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
