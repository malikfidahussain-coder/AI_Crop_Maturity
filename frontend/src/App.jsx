import { useEffect, useRef, useState } from "react";
import VideoCanvas from "./components/VideoCanvas";
import AnalysisPanel from "./components/AnalysisPanel";
import "./App.css";

const WS_URL =
  import.meta.env.VITE_WS_URL || "ws://127.0.0.1:8080/ws/detect";

const FRAME_WIDTH = 640;
const FRAME_HEIGHT = 480;
const JPEG_QUALITY = 0.6;
const RESPONSE_TIMEOUT_MS = 8000;

function App() {
  const [detections, setDetections] = useState([]);
  const [cameraError, setCameraError] = useState("");
  const [connectionState, setConnectionState] = useState("Connecting");

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const streamRef = useRef(null);
  const waitingForResponseRef = useRef(false);
  const timeoutRef = useRef(null);
  const mountedRef = useRef(false);

  useEffect(() => {
    mountedRef.current = true;

    const clearWait = () => {
      waitingForResponseRef.current = false;
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    };

    const captureAndSend = () => {
      if (!mountedRef.current) return;

      const ws = wsRef.current;
      const video = videoRef.current;
      const canvas = canvasRef.current;

      if (!ws || ws.readyState !== WebSocket.OPEN) return;
      if (waitingForResponseRef.current) return;
      if (!video || !canvas) {
        requestAnimationFrame(captureAndSend);
        return;
      }
      if (video.readyState < 2) {
        requestAnimationFrame(captureAndSend);
        return;
      }

      const context = canvas.getContext("2d");
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const image = canvas.toDataURL("image/jpeg", JPEG_QUALITY);

      waitingForResponseRef.current = true;
      timeoutRef.current = setTimeout(() => {
        waitingForResponseRef.current = false;
        timeoutRef.current = null;
        requestAnimationFrame(captureAndSend);
      }, RESPONSE_TIMEOUT_MS);

      try {
        ws.send(JSON.stringify({ image }));
      } catch (error) {
        console.error("Failed to send frame:", error);
        clearWait();
      }
    };

    const start = async () => {
      try {
        setConnectionState("Requesting camera");

        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: FRAME_WIDTH },
            height: { ideal: FRAME_HEIGHT },
          },
          audio: false,
        });

        if (!mountedRef.current) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }

        streamRef.current = stream;

        const video = videoRef.current;
        if (!video) {
          stream.getTracks().forEach((track) => track.stop());
          setCameraError("Video element is not available.");
          return;
        }

        video.srcObject = stream;
        await video.play();

        setConnectionState("Connecting");

        const ws = new WebSocket(WS_URL);
        wsRef.current = ws;

        ws.onopen = () => {
          setConnectionState("Connected");
          captureAndSend();
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            setDetections(data.detections || []);
            if (data.error) {
              console.error("Backend error:", data.error);
            }
          } catch (error) {
            console.error("Invalid WebSocket response:", error);
          } finally {
            clearWait();
            requestAnimationFrame(captureAndSend);
          }
        };

        ws.onclose = () => {
          setConnectionState("Disconnected");
          clearWait();
        };

        ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          setConnectionState("Error");
          clearWait();
        };
      } catch (error) {
        console.error("Camera error:", error);
        setCameraError(
          "Unable to access camera. Please allow camera permission."
        );
        setConnectionState("Camera Error");
      }
    };

    start();

    return () => {
      mountedRef.current = false;
      clearWait();

      if (wsRef.current) {
        wsRef.current.close();
      }

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>AI Crop Maturity Detection</h1>

        <div className="status">
          <span className="status-dot"></span>
          {cameraError ? "Camera Error" : connectionState}
        </div>
      </header>

      {cameraError && (
        <div className="camera-error">
          {cameraError}
        </div>
      )}

      <canvas
        ref={canvasRef}
        width={FRAME_WIDTH}
        height={FRAME_HEIGHT}
        className="capture-canvas"
      />

      <main className="main-content">
        <VideoCanvas
          detections={detections}
          videoRef={videoRef}
        />

        <AnalysisPanel detections={detections} />
      </main>
    </div>
  );
}

export default App;
