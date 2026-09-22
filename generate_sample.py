from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, wrpcap
import time
import random
import os

def generate_sample_pcap(filename="sample_traffic.pcap"):
    packets = []
    base_time = time.time() - 3600 # 1 hour ago
    
    # 1. Normal Traffic
    print("Generating normal traffic...")
    for i in range(50):
        pkt = IP(src=f"192.168.1.{random.randint(10, 50)}", dst="8.8.8.8") / UDP(sport=random.randint(1024, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com"))
        pkt.time = base_time + i * 2
        packets.append(pkt)
        
        pkt2 = IP(src=f"203.0.113.{random.randint(1, 20)}", dst="192.168.1.10") / TCP(sport=random.randint(1024, 65535), dport=443, flags="PA")
        pkt2.time = base_time + i * 2 + 1
        packets.append(pkt2)

    # 2. DoS ICMP Flood
    print("Generating DoS ICMP Flood...")
    attacker_ip = "185.15.20.100"
    for i in range(150):
        pkt = IP(src=attacker_ip, dst="192.168.1.10") / ICMP(type=8)
        pkt.time = base_time + 100 + (i * 0.01)
        packets.append(pkt)
        
    # 3. Port Scan
    print("Generating Port Scan...")
    scanner_ip = "45.22.10.55"
    for port in range(20, 100):
        pkt = IP(src=scanner_ip, dst="192.168.1.50") / TCP(sport=55555, dport=port, flags="S")
        pkt.time = base_time + 200 + (port * 0.1)
        packets.append(pkt)
        
    # 4. DNS Anomaly (DGA)
    print("Generating DNS Anomaly...")
    dga_domain = "xkqjfzmnbvcxdswert.com"
    pkt = IP(src="192.168.1.20", dst="1.1.1.1") / UDP(sport=33333, dport=53) / DNS(rd=1, qd=DNSQR(qname=dga_domain))
    pkt.time = base_time + 300
    packets.append(pkt)

    # Write to file
    wrpcap(filename, packets)
    print(f"Generated {len(packets)} packets and saved to {filename}")

if __name__ == "__main__":
    generate_sample_pcap()
