from dataclasses import dataclass
from enum import Enum

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(str, Enum):
    DOS_ICMP = "dos_icmp"
    DOS_SYN = "dos_syn"
    PORT_SCAN = "port_scan"
    DNS_ANOMALY = "dns_anomaly"
    ML_ANOMALY = "ml_anomaly"

@dataclass
class Alert:
    timestamp: float
    threat_type: ThreatType
    severity: AlertSeverity
    source_ip: str
    description: str
    is_acknowledged: bool = False
    alert_id: int = 0
