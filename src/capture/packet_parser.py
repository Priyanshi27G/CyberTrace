from scapy.all import Packet, IP, TCP, UDP, ICMP, DNS, DNSQR
from src.models.packet import PacketData
from src.utils.constants import PROTOCOL_MAP
import time

def parse_packet(raw_pkt: Packet) -> PacketData:
    """Parses a Scapy packet into a PacketData model."""
    ts = float(raw_pkt.time) if hasattr(raw_pkt, 'time') else time.time()
    
    if not raw_pkt.haslayer(IP):
        return PacketData(
            timestamp=ts,
            src_ip="Unknown",
            dst_ip="Unknown",
            protocol="Other",
            length=len(raw_pkt),
            summary="Non-IP Packet"
        )
        
    ip_layer = raw_pkt[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    length = len(raw_pkt)
    
    proto_num = ip_layer.proto
    protocol = PROTOCOL_MAP.get(proto_num, str(proto_num))
    
    src_port = None
    dst_port = None
    flags = None
    summary = ""
    
    if raw_pkt.haslayer(TCP):
        tcp_layer = raw_pkt[TCP]
        src_port = tcp_layer.sport
        dst_port = tcp_layer.dport
        flags = str(tcp_layer.flags)
        
        # Check if HTTP/HTTPS
        if dst_port in [80, 443] or src_port in [80, 443]:
            protocol = PROTOCOL_MAP.get(dst_port, PROTOCOL_MAP.get(src_port, "TCP"))
            
    elif raw_pkt.haslayer(UDP):
        udp_layer = raw_pkt[UDP]
        src_port = udp_layer.sport
        dst_port = udp_layer.dport
        
        if raw_pkt.haslayer(DNS) and raw_pkt.haslayer(DNSQR):
            protocol = "DNS"
            try:
                qname = raw_pkt[DNSQR].qname.decode('utf-8')
                summary = f"DNS Query: {qname}"
            except Exception:
                summary = "DNS Query: <malformed>"
                
    elif raw_pkt.haslayer(ICMP):
        icmp_layer = raw_pkt[ICMP]
        summary = f"ICMP Type: {icmp_layer.type}"

    return PacketData(
        timestamp=ts,
        src_ip=src_ip,
        dst_ip=dst_ip,
        protocol=protocol,
        length=length,
        src_port=src_port,
        dst_port=dst_port,
        flags=flags,
        summary=summary
    )
