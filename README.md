# CyberTrace 🔍

A real-time network traffic analysis and threat detection system built with Python (FastAPI), Scapy, and a modern React (Vite) frontend. Designed for educational purposes, it visualizes network packets and uses rule-based + ML techniques to identify potential cyber threats.

## Features
- **Live Packet Capture:** Sniff network traffic directly from interfaces.
- **PCAP Forensics:** Upload and analyze existing `.pcap` files.
- **Threat Detection:**
  - DoS (ICMP/SYN Flood) Detection
  - Port Scan Detection
  - DNS Anomaly (DGA) Detection via Shannon Entropy
  - ML-based Volumetric Anomaly Detection (Isolation Forest)
- **Modern Dashboard:** Built with React, TailwindCSS, and DaisyUI for a premium dark/light mode experience.

## Requirements
- Python 3.9+
- Node.js & npm (for the frontend)
- Root/Admin privileges (for live packet sniffing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Priyanshi27G/CyberTrace.git
   cd CyberTrace
   ```

2. Install Backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Usage

Start the backend API server:
```bash
sudo uvicorn api.main:app --host 0.0.0.0 --port 8000
```
*(Note: `sudo` is required to capture live network interfaces).*

Start the frontend development server:
```bash
cd frontend
npm run dev
```

## Project Structure
- `api/`: FastAPI server and endpoints.
- `src/`: Core backend logic (Capture engine, parsers, AI models, SQLite storage)
- `frontend/`: React + Vite frontend application.
- `config/`: YAML configuration and thresholds
- `tests/`: Unit testing suite

## Disclaimer
This project is created for academic and learning purposes. It should not be used as a primary security appliance in a production environment.

---
**Author:** Priyanshi Gupta  
**Co-Author:** Avi Mishra
