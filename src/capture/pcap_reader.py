import os
from scapy.all import rdpcap
from typing import List, Iterator
from src.interfaces.data_source import IDataSource
from src.models.packet import PacketData
from src.capture.packet_parser import parse_packet

class PCAPReader(IDataSource):
    """Reads network traffic from a PCAP file."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.packets_iterator: Iterator = iter([])
        self._is_active = False
        
    def start(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"PCAP file not found: {self.filepath}")
            
        # rdpcap reads everything into memory. For large files, PcapReader is better, 
        # but for a student project, rdpcap is simpler and sufficient for small demo files.
        raw_packets = rdpcap(self.filepath)
        parsed_packets = [parse_packet(p) for p in raw_packets]
        self.packets_iterator = iter(parsed_packets)
        self._is_active = True
        
    def stop(self):
        self._is_active = False
        self.packets_iterator = iter([])
        
    def get_packets(self, count: int = 100) -> List[PacketData]:
        if not self._is_active:
            return []
            
        packets = []
        for _ in range(count):
            try:
                packets.append(next(self.packets_iterator))
            except StopIteration:
                self._is_active = False
                break
        return packets
        
    def is_active(self) -> bool:
        return self._is_active
