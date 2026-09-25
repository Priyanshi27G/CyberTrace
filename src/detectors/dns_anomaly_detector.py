import time
import math
from collections import Counter
from typing import Optional
from src.detectors.base_detector import BaseDetector
from src.models.packet import PacketData
from src.models.alert import Alert, AlertSeverity, ThreatType
from src.config.config_loader import ConfigLoader

class DNSAnomalyDetector(BaseDetector):
    """Detects suspicious DNS queries (DGA domains) using Shannon Entropy."""
    
    def __init__(self):
        super().__init__()
        config = ConfigLoader()
        self.entropy_threshold = config.get_threshold("dns_anomaly.entropy_threshold", 3.5)
        self.max_length = config.get_threshold("dns_anomaly.max_query_length", 253)
        self.severity = AlertSeverity(config.get_threshold("dns_anomaly.severity", "high"))
        
    def _calculate_entropy(self, s: str) -> float:
        """Calculates the Shannon entropy of a string."""
        if not s:
            return 0.0
        # Remove TLD and dots for more accurate entropy calculation of the base domain
        clean_s = s.split('.')[0] if '.' in s else s
        if not clean_s:
            return 0.0
            
        p, lns = Counter(clean_s), float(len(clean_s))
        return -sum(count/lns * math.log2(count/lns) for count in p.values())
        
    def detect(self, packet: PacketData) -> Optional[Alert]:
        if packet.protocol != "DNS" or not packet.summary.startswith("DNS Query: "):
            return None
            
        domain = packet.summary.replace("DNS Query: ", "").strip()
        if not domain or domain == "<malformed>":
            return None
            
        now = packet.timestamp
        
        # Check length anomaly
        if len(domain) > self.max_length:
            return Alert(
                timestamp=now,
                threat_type=ThreatType.DNS_ANOMALY,
                severity=self.severity,
                source_ip=packet.src_ip,
                description=f"Anomalous DNS Query: length {len(domain)} exceeds threshold (domain: {domain[:20]}...)"
            )
            
        # Check entropy anomaly (DGA detection)
        entropy = self._calculate_entropy(domain)
        if entropy > self.entropy_threshold:
            return Alert(
                timestamp=now,
                threat_type=ThreatType.DNS_ANOMALY,
                severity=self.severity,
                source_ip=packet.src_ip,
                description=f"Potential DGA domain detected: '{domain}' (Entropy: {entropy:.2f})"
            )
            
        return None
