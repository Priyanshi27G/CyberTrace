import time
from typing import Optional, Dict, List
from src.detectors.base_detector import BaseDetector
from src.models.packet import PacketData
from src.models.alert import Alert, AlertSeverity, ThreatType
from src.config.config_loader import ConfigLoader

class DoSDetector(BaseDetector):
    """Detects ICMP and SYN flood Denial of Service attacks."""
    
    def __init__(self):
        # We'll use two separate sliding windows for ICMP and SYN
        super().__init__(window_seconds=10.0) # Base window not strictly used, we manage two
        config = ConfigLoader()
        
        self.icmp_max = config.get_threshold("dos.icmp_flood.max_packets", 50)
        self.icmp_window = config.get_threshold("dos.icmp_flood.window_seconds", 10.0)
        self.icmp_severity = AlertSeverity(config.get_threshold("dos.icmp_flood.severity", "critical"))
        
        self.syn_max = config.get_threshold("dos.syn_flood.max_packets", 100)
        self.syn_window = config.get_threshold("dos.syn_flood.window_seconds", 10.0)
        self.syn_severity = AlertSeverity(config.get_threshold("dos.syn_flood.severity", "critical"))
        
        self._icmp_history: Dict[str, List[float]] = {}
        self._syn_history: Dict[str, List[float]] = {}
        
    def _cleanup_specific(self, history: Dict[str, List[float]], window: float):
        now = time.time()
        cutoff = now - window
        for ip in list(history.keys()):
            history[ip] = [ts for ts in history[ip] if ts >= cutoff]
            if not history[ip]:
                del history[ip]
                
    def detect(self, packet: PacketData) -> Optional[Alert]:
        now = time.time()
        
        # ICMP Flood Check
        if packet.protocol == "ICMP":
            ip = packet.src_ip
            if ip not in self._icmp_history:
                self._icmp_history[ip] = []
            self._icmp_history[ip].append(packet.timestamp)
            self._cleanup_specific(self._icmp_history, self.icmp_window)
            
            if len(self._icmp_history[ip]) > self.icmp_max:
                return Alert(
                    timestamp=now,
                    threat_type=ThreatType.DOS_ICMP,
                    severity=self.icmp_severity,
                    source_ip=ip,
                    description=f"ICMP Flood detected: {len(self._icmp_history[ip])} packets in {self.icmp_window}s"
                )
                
        # SYN Flood Check
        if packet.protocol == "TCP" and packet.flags == "S": # Only SYN flag set
            ip = packet.src_ip
            if ip not in self._syn_history:
                self._syn_history[ip] = []
            self._syn_history[ip].append(packet.timestamp)
            self._cleanup_specific(self._syn_history, self.syn_window)
            
            if len(self._syn_history[ip]) > self.syn_max:
                return Alert(
                    timestamp=now,
                    threat_type=ThreatType.DOS_SYN,
                    severity=self.syn_severity,
                    source_ip=ip,
                    description=f"SYN Flood detected: {len(self._syn_history[ip])} SYN packets in {self.syn_window}s"
                )
                
        return None
        
    def reset(self):
        self._icmp_history.clear()
        self._syn_history.clear()
