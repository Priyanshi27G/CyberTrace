import streamlit as st
from dashboard.components.metric_cards import render_metric_cards
from dashboard.components.protocol_chart import render_protocol_chart
from dashboard.components.packet_table import render_packet_table
from dashboard.components.alert_panel import render_alert_panel
from src.config.config_loader import ConfigLoader
from st_autorefresh import st_autorefresh

def render_live_monitor():
    st.header("Live Network Monitor")
    
    config = ConfigLoader()
    refresh_rate = config.get("dashboard.refresh_interval", 2)
    display_limit = config.get("dashboard.max_display_packets", 50)
    
    # Controls
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.session_state.capture_engine.is_active():
            if st.button("🛑 Stop Sniffing", use_container_width=True):
                st.session_state.capture_engine.stop()
                st.rerun()
        else:
            if st.button("▶️ Start Sniffing", type="primary", use_container_width=True):
                # Update config with UI values
                st.session_state.capture_engine.interface = st.session_state.get('iface_input', config.get("capture.default_interface"))
                st.session_state.capture_engine.bpf_filter = st.session_state.get('bpf_input', "")
                st.session_state.capture_engine.start()
                st.rerun()
                
    with col2:
        st.text_input("Interface", value=config.get("capture.default_interface", "eth0"), key="iface_input")
    with col3:
        st.text_input("BPF Filter (e.g. 'tcp port 80')", value="", key="bpf_input")
        
    st.divider()
    
    # Fetch data
    recent_packets = st.session_state.db.get_recent_packets(limit=display_limit)
    active_alerts = st.session_state.alert_manager.get_active_alerts()
    unique_ips = len(set(p['src_ip'] for p in recent_packets)) if recent_packets else 0
    protocols_seen = len(set(p['protocol'] for p in recent_packets)) if recent_packets else 0
    
    # Render Metrics
    render_metric_cards(len(recent_packets), len(active_alerts), unique_ips, protocols_seen)
    
    # Layout
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("Recent Packets")
        render_packet_table(recent_packets)
        
    with col_side:
        st.subheader("Protocol Distribution")
        render_protocol_chart(recent_packets)
        
        st.subheader("Threat Alerts")
        render_alert_panel(active_alerts)
        
    # Auto-refresh if sniffing
    if st.session_state.capture_engine.is_active():
        try:
            st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")
        except NameError:
            st.warning("Install streamlit-autorefresh for live updates")
