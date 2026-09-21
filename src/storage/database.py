import sqlite3
import os
import threading
from typing import List, Dict, Any, Optional
from src.models.packet import PacketData
from src.models.alert import Alert, AlertSeverity, ThreatType
from src.config.config_loader import ConfigLoader

class Database:
    """SQLite database manager for CyberTrace."""
    
    def __init__(self):
        config = ConfigLoader()
        self.db_path = config.get("storage.db_path", "data/cybertrace.db")
        self.max_packets = config.get("storage.max_packets", 50000)
        self.local = threading.local()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        
    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self.local, "conn"):
            self.local.conn = sqlite3.connect(self.db_path)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
        
    def _init_db(self):
        conn = self._get_conn()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
        conn.commit()
        
    def store_packets(self, packets: List[PacketData]):
        if not packets:
            return
            
        conn = self._get_conn()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO packets (timestamp, src_ip, dst_ip, protocol, length, src_port, dst_port, flags, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        data = [
            (p.timestamp, p.src_ip, p.dst_ip, p.protocol, p.length, p.src_port, p.dst_port, p.flags, p.summary)
            for p in packets
        ]
        
        cursor.executemany(query, data)
        conn.commit()
        
        # Simple cleanup if we exceed max packets (approximate, runs occasionally)
        if len(packets) > 0 and (int(packets[-1].timestamp) % 100 == 0):
            cursor.execute(f"DELETE FROM packets WHERE id NOT IN (SELECT id FROM packets ORDER BY id DESC LIMIT {self.max_packets})")
            conn.commit()
            
    def store_alert(self, alert: Alert) -> int:
        conn = self._get_conn()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO alerts (timestamp, threat_type, severity, source_ip, description, acknowledged)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            alert.timestamp, alert.threat_type.value, alert.severity.value, 
            alert.source_ip, alert.description, int(alert.is_acknowledged)
        ))
        conn.commit()
        return cursor.lastrowid
        
    def get_recent_packets(self, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM packets ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]
        
    def get_active_alerts(self) -> List[Alert]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts WHERE acknowledged = 0 ORDER BY timestamp DESC")
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append(Alert(
                alert_id=row['id'],
                timestamp=row['timestamp'],
                threat_type=ThreatType(row['threat_type']),
                severity=AlertSeverity(row['severity']),
                source_ip=row['source_ip'],
                description=row['description'],
                is_acknowledged=bool(row['acknowledged'])
            ))
        return alerts
        
    def acknowledge_alert(self, alert_id: int):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE alerts SET acknowledged = 1 WHERE id = ?", (alert_id,))
        conn.commit()
