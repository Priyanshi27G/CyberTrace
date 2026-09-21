import time
from typing import List, Dict, Tuple
from src.models.alert import Alert, ThreatType
from src.storage.database import Database

class AlertManager:
    """Manages alert creation, deduplication and storage."""
    
    def __init__(self, db: Database):
        self.db = db
        # Structure: {(threat_type, source_ip): last_timestamp}
        self._recent_alerts: Dict[Tuple[ThreatType, str], float] = {}
        self.dedup_window = 60.0 # 60 seconds deduplication window
        
    def process_alert(self, alert: Alert) -> bool:
        """
        Process a new alert. Returns True if stored (not deduplicated).
        """
        now = time.time()
        key = (alert.threat_type, alert.source_ip)
        
        # Deduplication check
        if key in self._recent_alerts:
            last_time = self._recent_alerts[key]
            if now - last_time < self.dedup_window:
                return False # Skip, recently alerted
                
        self._recent_alerts[key] = now
        alert_id = self.db.store_alert(alert)
        alert.alert_id = alert_id
        return True
        
    def get_active_alerts(self) -> List[Alert]:
        return self.db.get_active_alerts()
        
    def acknowledge(self, alert_id: int):
        self.db.acknowledge_alert(alert_id)
