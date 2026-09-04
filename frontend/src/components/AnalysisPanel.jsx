// frontend/src/components/AnalysisPanel.jsx

function AnalysisPanel({ detections }) {
  return (
    <div className="analysis-panel" style={styles.panel}>
      <h2>Live Analysis</h2>
      {detections.length === 0 ? (
        <p style={{ color: "#aaa" }}>No crops detected in frame.</p>
      ) : (
        <div className="metrics-list">
          {detections.map((det, index) => (
            <div key={det.object_id || index} style={styles.card}>
              <h3 style={{ margin: "0 0 10px 0", color: "#0f0" }}>
                {det.crop.toUpperCase()} 
                <span style={styles.idBadge}>ID: {det.object_id}</span>
              </h3>
              <p style={styles.text}><strong>Confidence:</strong> {Math.round(det.confidence * 100)}%</p>
              
              {/* --- NEW MATURITY & HARVEST CODE PATCH START --- */}
              <p style={styles.text}>
                <strong>Maturity:</strong> {det.maturity?.stage || "Unknown"} ({det.maturity?.score || 0}%)
              </p>
              <p style={styles.text}>
                <strong>Harvest Readiness:</strong> {det.harvest?.readiness || "Unknown"} 
                <br/>
                <span style={{ color: "#aaa", fontSize: "0.9em" }}>Est: {det.harvest?.estimated_time || "N/A"}</span>
              </p>
              {/* --- NEW MATURITY & HARVEST CODE PATCH END --- */}

              {/* --- NEW: Render Temperature --- */}
              <p style={styles.text}>
                <strong>Optimal Temp:</strong> {det.temperature || "N/A"}
              </p>
              
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  panel: {
    width: "350px",
    backgroundColor: "#1e1e1e",
    padding: "20px",
    borderRadius: "8px",
    color: "#fff",
    maxHeight: "480px",
    overflowY: "auto",
  },
  card: {
    backgroundColor: "#2a2a2a",
    padding: "15px",
    marginBottom: "15px",
    borderLeft: "4px solid #00ff00",
    borderRadius: "4px",
  },
  idBadge: {
    fontSize: "0.75em",
    backgroundColor: "#444",
    padding: "2px 6px",
    borderRadius: "4px",
    marginLeft: "10px",
    color: "#ccc",
  },
  text: {
    margin: "5px 0",
    fontSize: "0.9em",
  }
};

export default AnalysisPanel;