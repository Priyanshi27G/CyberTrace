import streamlit as st
import os

# Must be the first Streamlit command
st.set_page_config(
    page_title="CyberTrace",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.components.sidebar import render_sidebar
from dashboard.pages.live_monitor import render_live_monitor
from dashboard.pages.pcap_forensics import render_pcap_forensics
from dashboard.pages.settings import render_settings

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'styles', 'custom.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def initialize_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Live Monitor'
    if 'capture_engine' not in st.session_state:
        from src.capture.live_capture import LiveCapture
        st.session_state.capture_engine = LiveCapture()
    if 'db' not in st.session_state:
        from src.storage.database import Database
        st.session_state.db = Database()
    if 'alert_manager' not in st.session_state:
        from src.alerts.alert_manager import AlertManager
        st.session_state.alert_manager = AlertManager(st.session_state.db)
    if 'detectors' not in st.session_state:
        from src.detectors.dos_detector import DoSDetector
        from src.detectors.port_scan_detector import PortScanDetector
        from src.detectors.dns_anomaly_detector import DNSAnomalyDetector
        from src.detectors.ml_anomaly_detector import MLAnomalyDetector
        st.session_state.detectors = [
            DoSDetector(),
            PortScanDetector(),
            DNSAnomalyDetector(),
            MLAnomalyDetector()
        ]

def main():
    load_css()
    initialize_session_state()
    
    # Process any pending packets and run detectors
    if st.session_state.capture_engine.is_active():
        packets = st.session_state.capture_engine.get_packets(count=100)
        st.session_state.db.store_packets(packets)
        
        for pkt in packets:
            for detector in st.session_state.detectors:
                alert = detector.detect(pkt)
                if alert:
                    st.session_state.alert_manager.process_alert(alert)

    # Sidebar Navigation
    selected_page = render_sidebar()
    
    # Route to page
    if selected_page == "Live Monitor":
        render_live_monitor()
    elif selected_page == "PCAP Forensics":
        render_pcap_forensics()
    elif selected_page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()
