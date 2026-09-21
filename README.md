# CyberTrace 🔍

A real-time network traffic analysis and threat detection system built with Python, Scapy, and Streamlit. Designed for educational purposes, it visualizes network packets and uses rule-based + ML techniques to identify potential cyber threats.

## Features
- **Live Packet Capture:** Sniff network traffic directly from interfaces.
- **PCAP Forensics:** Upload and analyze existing `.pcap` files.
- **Threat Detection:**
  - DoS (ICMP/SYN Flood) Detection
  - Port Scan Detection
  - DNS Anomaly (DGA) Detection via Shannon Entropy
  - ML-based Volumetric Anomaly Detection (Isolation Forest)
- **Interactive Dashboard:** Live metrics, protocol distribution, and GeoIP mapping of source IPs.

## Requirements
- Python 3.9+
- Root/Admin privileges (for live packet sniffing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Priyanshi27G/CyberTrace.git
   cd CyberTrace
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the interactive Streamlit dashboard:
```bash
sudo python3 run.py
```
*(Note: `sudo` is required to capture live network interfaces. If you only want to use PCAP forensics, you can run it without sudo).*

## Project Structure
- `src/`: Core backend logic (Capture engine, parsers, AI models, SQLite storage)
- `dashboard/`: Streamlit frontend (Pages, components, styling)
- `config/`: YAML configuration and thresholds
- `tests/`: Unit testing suite

## Disclaimer
This project is created for academic and learning purposes. It should not be used as a primary security appliance in a production environment.

---
**Author:** Priyanshi Gupta  
**Co-Author:** Avi Mishra
