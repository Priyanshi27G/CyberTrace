CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    length INTEGER,
    src_port INTEGER,
    dst_port INTEGER,
    flags TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    threat_type TEXT,
    severity TEXT,
    source_ip TEXT,
    description TEXT,
    acknowledged INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_packets_timestamp ON packets(timestamp);
CREATE INDEX IF NOT EXISTS idx_packets_src_ip ON packets(src_ip);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
