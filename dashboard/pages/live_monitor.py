import streamlit as st
from dashboard.components.metric_cards import render_metric_cards
from dashboard.components.protocol_chart import render_protocol_chart
from dashboard.components.timeline_chart import render_timeline_chart
from dashboard.components.geo_map import render_geo_map
from dashboard.components.packet_table import render_packet_table
from dashboard.components.alert_panel import render_alert_panel
from dashboard.components.top_talkers_chart import render_top_talkers
from dashboard.components.severity_chart import render_severity_chart
from src.config.config_loader import ConfigLoader
from streamlit_autorefresh import st_autorefresh

def render_live_monitor():
    st.markdown('<div class="ct-section-title">Live Network Monitor</div>', unsafe_allow_html=True)
    
    config = ConfigLoader()
    refresh_rate = config.get("dashboard.refresh_interval", 2)
    display_limit = config.get("dashboard.max_display_packets", 50)
    theme = st.session_state.get('theme', 'dark')
    
    # Controls bar
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.session_state.capture_engine.is_active():
            if st.button("🛑 Stop Sniffing", use_container_width=True):
                st.session_state.capture_engine.stop()
                st.rerun()
        else:
            if st.button("▶️ Start Sniffing", type="primary", use_container_width=True):
                iface = st.session_state.get('iface_input', config.get("capture.default_interface"))
                st.session_state.capture_engine.interface = iface
                st.session_state.capture_engine.bpf_filter = st.session_state.get('bpf_input', "")
                st.session_state.capture_engine.start()
                st.rerun()
                
    with col2:
        default_iface = getattr(st.session_state.capture_engine, 'interface', "eth0")
        if hasattr(default_iface, 'name'):
            default_iface = default_iface.name
        st.text_input("Interface", value=default_iface, key="iface_input")
    with col3:
        st.text_input("BPF Filter (e.g. 'tcp port 80')", value="", key="bpf_input")
    
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    
    # Fetch data
    recent_packets = st.session_state.db.get_recent_packets(limit=display_limit)
    active_alerts = st.session_state.alert_manager.get_active_alerts()
    unique_ips = len(set(p['src_ip'] for p in recent_packets)) if recent_packets else 0
    protocols_seen = len(set(p['protocol'] for p in recent_packets)) if recent_packets else 0
    
    # Metric cards
    render_metric_cards(len(recent_packets), len(active_alerts), unique_ips, protocols_seen)
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    
    # Tabbed content
    tab_overview, tab_packets, tab_threats = st.tabs(["📊 Overview", "📋 Packets", "🚨 Threats"])
    
    with tab_overview:
        # Row 1: Timeline + Protocol
        col_timeline, col_proto = st.columns([2, 1])
        with col_timeline:
            st.markdown('<div class="ct-section-title">Traffic Timeline</div>', unsafe_allow_html=True)
            render_timeline_chart(recent_packets, theme)
        with col_proto:
            st.markdown('<div class="ct-section-title">Protocol Distribution</div>', unsafe_allow_html=True)
            render_protocol_chart(recent_packets, theme)
        
        # Row 2: GeoIP + Top Talkers
        col_map, col_talkers = st.columns([2, 1])
        with col_map:
            st.markdown('<div class="ct-section-title">GeoIP Map</div>', unsafe_allow_html=True)
            render_geo_map(recent_packets)
        with col_talkers:
            st.markdown('<div class="ct-section-title">Top Talkers</div>', unsafe_allow_html=True)
            render_top_talkers(recent_packets, theme)
    
    with tab_packets:
        st.markdown('<div class="ct-section-title">Captured Packets</div>', unsafe_allow_html=True)
        render_packet_table(recent_packets)
    
    with tab_threats:
        col_sev, col_alerts = st.columns([1, 2])
        with col_sev:
            st.markdown('<div class="ct-section-title">Severity Breakdown</div>', unsafe_allow_html=True)
            render_severity_chart(active_alerts, theme)
        with col_alerts:
            st.markdown('<div class="ct-section-title">Active Alerts</div>', unsafe_allow_html=True)
            render_alert_panel(active_alerts)
    
    # Auto-refresh while sniffing
    if st.session_state.capture_engine.is_active():
        try:
            st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")
        except Exception:
            pass
