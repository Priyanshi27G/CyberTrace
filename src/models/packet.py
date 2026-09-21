from dataclasses import dataclass
from typing import Optional

@dataclass
class PacketData:
    timestamp: float
    src_ip: str
    dst_ip: str
    protocol: str
    length: int
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    flags: Optional[str] = None
    summary: str = ""

@dataclass
class FlowData:
    flow_id: str
    src_ip: str
    dst_ip: str
    protocol: str
    pkt_count: int
    byte_count: int
    start_time: float
    end_time: float
