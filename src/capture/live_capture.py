import threading
import queue
import logging
from scapy.all import sniff, conf
from typing import List
from src.interfaces.data_source import IDataSource
from src.models.packet import PacketData
from src.capture.packet_parser import parse_packet
from src.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class LiveCapture(IDataSource):
    """Captures live network traffic in a background thread."""
    
    def __init__(self):
        config = ConfigLoader()
        self.interface = config.get("capture.default_interface", conf.iface)
        if str(self.interface).lower() == "auto":
            self.interface = conf.iface
        self.bpf_filter = config.get("capture.bpf_filter", "")
        self.max_buffer = config.get("capture.max_buffer", 5000)
        
        self.packet_queue = queue.Queue(maxsize=self.max_buffer)
        self.stop_event = threading.Event()
        self.capture_thread = None
        self._is_active = False
        
    def _packet_handler(self, raw_pkt):
        if self.stop_event.is_set():
            return
            
        try:
            parsed_pkt = parse_packet(raw_pkt)
            
            # Simple non-blocking put, drop if queue full (avoids memory leak)
            if not self.packet_queue.full():
                self.packet_queue.put_nowait(parsed_pkt)
        except Exception as e:
            logger.error(f"Error parsing packet: {e}")
            
    def _sniff_loop(self):
        try:
            sniff(
                iface=self.interface,
                filter=self.bpf_filter,
                prn=self._packet_handler,
                stop_filter=lambda _: self.stop_event.is_set(),
                store=0 # CRITICAL: Don't store in Scapy memory
            )
        except Exception as e:
            logger.error(f"Sniffer crashed: {e}")
            # Try to start in demo mode if permission denied
            if "Permission denied" in str(e) or "Operation not permitted" in str(e):
                logger.warning("Permission denied for live capture. Need root/sudo.")
        finally:
            self._is_active = False

    def start(self):
        if self._is_active:
            return
            
        self.stop_event.clear()
        # Empty queue
        while not self.packet_queue.empty():
            try:
                self.packet_queue.get_nowait()
            except queue.Empty:
                break
                
        self._is_active = True
        self.capture_thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.capture_thread.start()
        
    def stop(self):
        self.stop_event.set()
        self._is_active = False
        if self.capture_thread and self.capture_thread.is_alive():
            # Scapy sniff stop_filter will catch the event soon
            pass
            
    def get_packets(self, count: int = 100) -> List[PacketData]:
        packets = []
        for _ in range(count):
            try:
                packets.append(self.packet_queue.get_nowait())
            except queue.Empty:
                break
        return packets
        
    def is_active(self) -> bool:
        return self._is_active
