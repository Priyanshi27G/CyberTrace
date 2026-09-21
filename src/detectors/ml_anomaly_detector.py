import time
import numpy as np
from typing import Optional, Dict
from collections import defaultdict
from src.detectors.base_detector import BaseDetector
from src.models.packet import PacketData
from src.models.alert import Alert, AlertSeverity, ThreatType
from src.config.config_loader import ConfigLoader

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class FlowStats:
    def __init__(self, start_time: float):
        self.pkt_count = 0
        self.byte_count = 0
        self.dst_ports = set()
        self.start_time = start_time
        self.last_time = start_time
        
    def add_packet(self, pkt: PacketData):
        self.pkt_count += 1
        self.byte_count += pkt.length
        if pkt.dst_port:
            self.dst_ports.add(pkt.dst_port)
        self.last_time = pkt.timestamp
        
    def get_features(self) -> list:
        duration = max(0.001, self.last_time - self.start_time)
        mean_pkt_len = self.byte_count / self.pkt_count if self.pkt_count > 0 else 0
        pkts_per_sec = self.pkt_count / duration
        return [self.pkt_count, self.byte_count, mean_pkt_len, len(self.dst_ports), pkts_per_sec]


class MLAnomalyDetector(BaseDetector):
    """Detects volumetric anomalies using Isolation Forest on flow data."""
    
    def __init__(self):
        super().__init__()
        config = ConfigLoader()
        self.contamination = config.get_threshold("ml_anomaly.contamination", 0.05)
        self.n_estimators = config.get_threshold("ml_anomaly.n_estimators", 100)
        self.min_samples = config.get_threshold("ml_anomaly.min_samples", 500)
        self.severity = AlertSeverity(config.get_threshold("ml_anomaly.severity", "medium"))
        
        self.flows: Dict[str, FlowStats] = {}
        self.training_data = []
        self.training_ips = []
        self.model = None
        self.scaler = None
        self.is_trained = False
        
        if SKLEARN_AVAILABLE:
            self.model = IsolationForest(
                n_estimators=self.n_estimators, 
                contamination=self.contamination,
                random_state=42
            )
            self.scaler = StandardScaler()
            
    def _train_model(self):
        if not SKLEARN_AVAILABLE or len(self.training_data) < self.min_samples:
            return
            
        X = np.array(self.training_data)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True
        
        # Clear training data to save memory
        self.training_data = []
        self.training_ips = []

    def detect(self, packet: PacketData) -> Optional[Alert]:
        if not SKLEARN_AVAILABLE:
            return None
            
        now = time.time()
        ip = packet.src_ip
        
        if ip not in self.flows:
            self.flows[ip] = FlowStats(packet.timestamp)
            
        flow = self.flows[ip]
        flow.add_packet(packet)
        
        # Evaluate flow every 10 packets
        if flow.pkt_count % 10 == 0:
            features = flow.get_features()
            
            if not self.is_trained:
                self.training_data.append(features)
                self.training_ips.append(ip)
                if len(self.training_data) >= self.min_samples:
                    self._train_model()
                return None
                
            # Predict
            X_test = self.scaler.transform([features])
            prediction = self.model.predict(X_test)[0]
            
            if prediction == -1: # Anomaly
                # Reset flow to avoid continuous alerting
                del self.flows[ip]
                return Alert(
                    timestamp=now,
                    threat_type=ThreatType.ML_ANOMALY,
                    severity=self.severity,
                    source_ip=ip,
                    description=f"ML Anomaly detected: unusual traffic pattern (pkts: {features[0]}, bytes: {features[1]})"
                )
                
        # Cleanup old flows
        if now - flow.last_time > 60.0:
            del self.flows[ip]
            
        return None
        
    def reset(self):
        self.flows.clear()
        self.is_trained = False
        self.training_data = []
        self.training_ips = []
