import time
from typing import Optional, Dict, Set
from src.detectors.base_detector import BaseDetector
from src.models.packet import PacketData
from src.models.alert import Alert, AlertSeverity, ThreatType
from src.config.config_loader import ConfigLoader

class PortScanDetector(BaseDetector):
    """Detects when a single IP attempts to connect to many different ports."""
    
    def __init__(self):
        super().__init__()
        config = ConfigLoader()
        self.min_ports = config.get_threshold("port_scan.min_ports", 10)
        self.window = config.get_threshold("port_scan.window_seconds", 30.0)
        self.severity = AlertSeverity(config.get_threshold("port_scan.severity", "high"))
        
        # Structure: {source_ip: {dst_port_1, dst_port_2, ...}}
        self._port_history: Dict[str, Set[int]] = {}
        # Tracking when we started observing the IP
        self._first_seen: Dict[str, float] = {}
        
    def detect(self, packet: PacketData) -> Optional[Alert]:
        if not packet.dst_port:
            return None
            
        now = time.time()
        ip = packet.src_ip
        
        if ip not in self._port_history:
            self._port_history[ip] = set()
            self._first_seen[ip] = now
            
        # Clean up if window expired
        if now - self._first_seen[ip] > self.window:
            self._port_history[ip] = set()
            self._first_seen[ip] = now
            
        self._port_history[ip].add(packet.dst_port)
        
        if len(self._port_history[ip]) >= self.min_ports:
            # We detected a scan! Alert and reset to avoid spamming
            port_count = len(self._port_history[ip])
            self._port_history[ip] = set()
            self._first_seen[ip] = now
            
            return Alert(
                timestamp=now,
                threat_type=ThreatType.PORT_SCAN,
                severity=self.severity,
                source_ip=ip,
                description=f"Port scan detected: accessed {port_count} unique ports in {self.window}s"
            )
            
        return None
        
    def reset(self):
        self._port_history.clear()
        self._first_seen.clear()
