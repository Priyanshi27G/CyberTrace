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

def apply_theme():
    theme = st.session_state.get('theme', 'dark')
    st.markdown(f"""
    <script>
        document.documentElement.setAttribute('data-theme', '{theme}');
    </script>
    <style>
        :root {{ --current-theme: {theme}; }}
        {'[data-theme="light"] *' if theme == 'light' else ''}
    </style>
    """, unsafe_allow_html=True)
    
    # Inject theme class via a hidden div trick since Streamlit doesn't let us set <html> attrs easily
    if theme == 'light':
        st.markdown("""<style>
        :root {
            --bg-primary: #F8FAFC !important;
            --bg-secondary: #F1F5F9 !important;
            --bg-card: #FFFFFF !important;
            --border-color: #E2E8F0 !important;
            --border-hover: #CBD5E1 !important;
            --text-primary: #1E293B !important;
            --text-secondary: #64748B !important;
            --text-muted: #94A3B8 !important;
            --shadow: rgba(0,0,0,0.08) !important;
        }
        .stApp { background-color: #F8FAFC !important; }
        section[data-testid="stSidebar"] { background-color: #F1F5F9 !important; }
        h1, h2, h3 { color: #1E293B !important; }
        p, span, div, label { color: #1E293B; }
        .stMarkdown { color: #1E293B; }
        </style>""", unsafe_allow_html=True)

def initialize_session_state():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
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

def process_live_packets():
    if st.session_state.capture_engine.is_active():
        packets = st.session_state.capture_engine.get_packets(count=100)
        st.session_state.db.store_packets(packets)
        
        for pkt in packets:
            for detector in st.session_state.detectors:
                alert = detector.detect(pkt)
                if alert:
                    st.session_state.alert_manager.process_alert(alert)

def render_header():
    is_active = st.session_state.capture_engine.is_active()
    badge_class = "ct-badge-active" if is_active else "ct-badge-inactive"
    badge_text = "● Live" if is_active else "● Idle"
    
    st.markdown(f"""
    <div class="ct-header-bar">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.3rem;">🔍</span>
            <span style="font-weight:700; font-size:1.1rem;">CyberTrace</span>
            <span class="ct-status-badge {badge_class}">{badge_text}</span>
        </div>
        <div style="font-size:0.8rem; color:var(--text-muted);">v2.0.0</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    load_css()
    initialize_session_state()
    apply_theme()
    process_live_packets()
    
    # Custom header
    render_header()
    
    # Sidebar navigation
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
