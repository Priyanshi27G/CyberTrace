# CyberTrace Project - Handoff & Context History

## Project Overview
CyberTrace is a real-time network security monitoring and PCAP forensics dashboard. The project was initially built to sniff packets, detect anomalies (like DoS, Port Scans, etc.) using machine learning and basic rule-based detectors, and visualize this data on a dashboard.

## Architectural Evolution

### Phase 1: Python Streamlit (Original Architecture)
* **Stack**: Python, Streamlit, Scapy, Pandas, Plotly.
* **Why Streamlit?** Streamlit was chosen initially because it excels at Rapid Application Development (RAD) for data science. It makes rendering complex, interactive data visualizations (like Geo Maps with Folium, interactive Plotly timeline charts, and dynamic dataframes) incredibly easy without needing a separate frontend codebase. 
* **The Problem**: While the graphs were superior and functional, the UI looked very basic, lacked a premium "SaaS" feel, and customizing the CSS for a true dark mode or modern glassmorphism effect was buggy and unaligned.

### Phase 2: FastAPI + React (Current Architecture)
* **Stack**: Python (FastAPI backend), React + Vite (Frontend), TailwindCSS + DaisyUI.
* **The Migration**: Because of the UI limitations in Streamlit (alignment issues, contrast problems, lack of a premium dark mode), the architecture was completely decoupled. 
  * The backend capture engine and detectors were wrapped in a **FastAPI** server (`api/main.py`).
  * A brand new **React** frontend was scaffolded (`frontend/src`) with extremely polished aesthetics, modern routing (`react-router-dom`), and premium UI components.
* **Restored Functionality**: PCAP forensics upload (`/api/upload_pcap`) was wired back up, and dummy alert triggers were added to UI buttons for demonstration purposes (viva prep).

## User's Core Concern & Future Development Notes

**User's Direct Feedback**: 
> *"The current React UI looks much better than Python Streamlit, BUT the graphs and data visualizations in Streamlit were significantly better. Was Streamlit chosen originally just because it visualizes data better?"*

**Answer/Context for the next Agent**: 
Yes, exactly! Streamlit natively integrates with powerful data libraries like Plotly and Folium out-of-the-box, making complex visualizations trivial. In React, we have to manually build these charts using libraries like `recharts`, which look clean but lack the deep, out-of-the-box interactivity of Plotly unless heavily customized.

### Next Steps for the New Agent
1. **Enhance React Visualizations**: The user misses the high-quality graphs from Streamlit. In the React app, you should look into integrating `react-plotly.js` or upgrading the current `recharts` implementations to bring back that rich, interactive data visualization feel while maintaining the beautiful new UI.
2. **Continue Development**: The UI is currently mostly a beautifully styled shell with functional API integration for PCAP uploads. The Live Monitor (WebSockets) and detailed Threats database still need to be fully wired up to the frontend state.
3. **Run Instructions**:
   - Backend: `sudo python3 run.py`
   - Frontend: `cd frontend && npm run dev`
