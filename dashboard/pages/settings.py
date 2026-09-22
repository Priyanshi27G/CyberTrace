import streamlit as st
from src.config.config_loader import ConfigLoader

def render_settings():
    st.header("Settings & Configuration")
    config = ConfigLoader()
    
    st.subheader("Detection Thresholds")
    st.info("Note: Modifying thresholds here currently requires an app restart to take full effect in this demo version.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**DoS Detection**")
        st.slider("ICMP Flood Max Packets", 10, 1000, config.get_threshold("dos.icmp_flood.max_packets", 50))
        st.slider("SYN Flood Max Packets", 10, 1000, config.get_threshold("dos.syn_flood.max_packets", 100))
        
        st.markdown("**Port Scan Detection**")
        st.slider("Min Unique Ports", 5, 100, config.get_threshold("port_scan.min_ports", 10))
        
    with col2:
        st.markdown("**DNS Anomaly**")
        st.slider("Entropy Threshold", 2.0, 5.0, float(config.get_threshold("dns_anomaly.entropy_threshold", 3.5)), 0.1)
        
        st.markdown("**ML Anomaly (Isolation Forest)**")
        st.slider("Contamination Rate", 0.01, 0.20, float(config.get_threshold("ml_anomaly.contamination", 0.05)), 0.01)
        
    st.divider()
    
    st.subheader("Database Stats")
    conn = st.session_state.db._get_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM packets")
        pkt_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alerts")
        alert_count = cursor.fetchone()[0]
        
        st.write(f"**Total Packets Stored:** {pkt_count}")
        st.write(f"**Total Alerts Generated:** {alert_count}")
        
        if st.button("Clear Database"):
            cursor.execute("DELETE FROM packets")
            cursor.execute("DELETE FROM alerts")
            conn.commit()
            st.success("Database cleared successfully!")
            st.rerun()
    except Exception as e:
        st.error(f"Could not load database stats: {e}")
        
    st.divider()
    st.markdown("### About CyberTrace")
    st.markdown("""
    **Version:** 1.0.3  
    
    A network traffic analysis and threat detection tool.
    """)
