import time
from typing import Dict, List, Optional
from src.interfaces.detector import IDetector
from src.models.packet import PacketData
from src.models.alert import Alert

class BaseDetector(IDetector):
    """Base class for all detectors providing sliding window functionality."""
    
    def __init__(self, window_seconds: float = 60.0):
        self.window_seconds = window_seconds
        # Structure: {source_ip: [timestamp1, timestamp2, ...]}
        self._history: Dict[str, List[float]] = {}
        self._last_cleanup = time.time()
        
    def _cleanup_old_entries(self):
        now = time.time()
        # Only cleanup every 5 seconds to avoid overhead
        if now - self._last_cleanup < 5.0:
            return
            
        self._last_cleanup = now
        cutoff = now - self.window_seconds
        
        empty_ips = []
        for ip, timestamps in self._history.items():
            # Keep timestamps after cutoff
            self._history[ip] = [ts for ts in timestamps if ts >= cutoff]
            if not self._history[ip]:
                empty_ips.append(ip)
                
        for ip in empty_ips:
            del self._history[ip]
            
    def _add_event(self, ip: str, timestamp: float):
        if ip not in self._history:
            self._history[ip] = []
        self._history[ip].append(timestamp)
        self._cleanup_old_entries()
        
    def _count_in_window(self, ip: str) -> int:
        return len(self._history.get(ip, []))
        
    def reset(self):
        self._history.clear()
        
    def detect(self, packet: PacketData) -> Optional[Alert]:
        raise NotImplementedError
        
    def get_name(self) -> str:
        return self.__class__.__name__
