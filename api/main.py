from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.capture.live_capture import LiveCapture
from src.storage.database import Database
from src.alerts.alert_manager import AlertManager
from src.detectors.dos_detector import DoSDetector
from src.detectors.port_scan_detector import PortScanDetector
from src.detectors.dns_anomaly_detector import DNSAnomalyDetector
from src.detectors.ml_anomaly_detector import MLAnomalyDetector

app = FastAPI(title="CyberTrace API", version="2.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
capture_engine = LiveCapture()
db = Database()
alert_manager = AlertManager(db)
detectors = [
    DoSDetector(),
    PortScanDetector(),
    DNSAnomalyDetector(),
    MLAnomalyDetector()
]

active_websockets = []

async def capture_loop():
    while capture_engine.is_active():
        packets = capture_engine.get_packets(count=100)
        if packets:
            db.store_packets(packets)
            for pkt in packets:
                for detector in detectors:
                    alert = detector.detect(pkt)
                    if alert:
                        alert_manager.process_alert(alert)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    # Automatically start capture on boot for convenience
    capture_engine.start()
    asyncio.create_task(capture_loop())

@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "capture_active": capture_engine.is_active()
    }

@app.post("/api/capture/start")
async def start_capture():
    if not capture_engine.is_active():
        capture_engine.start()
        asyncio.create_task(capture_loop())
    return {"status": "started"}

@app.post("/api/capture/stop")
async def stop_capture():
    if capture_engine.is_active():
        capture_engine.stop()
    return {"status": "stopped"}

@app.get("/api/metrics")
async def get_metrics():
    # Calculate some basic metrics for the UI
    try:
        packets = db.get_recent_packets(limit=1000)
        alerts = db.get_recent_alerts(limit=100)
    except Exception as e:
        packets = []
        alerts = []
        
    return {
        "total_packets_seen": len(packets), # In real app, query count(*)
        "active_alerts": len(alerts),
        "capture_rate": "N/A"
    }

@app.get("/api/alerts")
async def get_alerts():
    try:
        alerts = db.get_recent_alerts(limit=50)
        # Convert Alert objects to dicts
        return [{"id": a.id, "timestamp": a.timestamp, "severity": a.severity.value, "title": a.title, "description": a.description} for a in alerts]
    except Exception as e:
        return []

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            # In a real app we'd stream real data, here we just ping pong or send periodic updates
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
