import streamlit as st
import sys
import platform
from src.config.config_loader import ConfigLoader

def render_settings():
    st.markdown('<div class="ct-section-title">Settings & Configuration</div>', unsafe_allow_html=True)
    config = ConfigLoader()
    
    tab_detection, tab_database, tab_about = st.tabs(["🎯 Detection Config", "💾 Database", "ℹ️ About"])
    
    with tab_detection:
        st.info("Modifying thresholds requires an app restart to take effect.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="ct-card"><div class="ct-section-title">DoS Detection</div>""", unsafe_allow_html=True)
            st.slider("ICMP Flood Max Packets", 10, 1000, config.get_threshold("dos.icmp_flood.max_packets", 50))
            st.slider("SYN Flood Max Packets", 10, 1000, config.get_threshold("dos.syn_flood.max_packets", 100))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""<div class="ct-card" style="margin-top:12px;"><div class="ct-section-title">Port Scan Detection</div>""", unsafe_allow_html=True)
            st.slider("Min Unique Ports", 5, 100, config.get_threshold("port_scan.min_ports", 10))
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("""<div class="ct-card"><div class="ct-section-title">DNS Anomaly</div>""", unsafe_allow_html=True)
            st.slider("Entropy Threshold", 2.0, 5.0, float(config.get_threshold("dns_anomaly.entropy_threshold", 3.5)), 0.1)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""<div class="ct-card" style="margin-top:12px;"><div class="ct-section-title">ML Anomaly (Isolation Forest)</div>""", unsafe_allow_html=True)
            st.slider("Contamination Rate", 0.01, 0.20, float(config.get_threshold("ml_anomaly.contamination", 0.05)), 0.01)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab_database:
        conn = st.session_state.db._get_conn()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM packets")
            pkt_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM alerts")
            alert_count = cursor.fetchone()[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="ct-metric" style="border-top: 3px solid #10B981;">
                    <div class="ct-metric-value">{pkt_count:,}</div>
                    <div class="ct-metric-label">Total Packets Stored</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="ct-metric" style="border-top: 3px solid #F59E0B;">
                    <div class="ct-metric-value">{alert_count:,}</div>
                    <div class="ct-metric-label">Total Alerts Generated</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            
            if st.button("🗑️ Clear Database", use_container_width=True):
                cursor.execute("DELETE FROM packets")
                cursor.execute("DELETE FROM alerts")
                conn.commit()
                st.success("Database cleared!")
                st.rerun()
        except Exception as e:
            st.error(f"Could not load database stats: {e}")
    
    with tab_about:
        st.markdown(f"""
        <div class="ct-card">
            <div class="ct-section-title">CyberTrace</div>
            <table style="width:100%; border-collapse:collapse;">
                <tr><td style="padding:8px 0; color:var(--text-secondary);">Version</td><td style="padding:8px 0; font-weight:600;">2.0.0</td></tr>
                <tr><td style="padding:8px 0; color:var(--text-secondary);">Python</td><td style="padding:8px 0;">{sys.version.split()[0]}</td></tr>
                <tr><td style="padding:8px 0; color:var(--text-secondary);">Platform</td><td style="padding:8px 0;">{platform.system()} {platform.release()}</td></tr>
                <tr><td style="padding:8px 0; color:var(--text-secondary);">Description</td><td style="padding:8px 0;">Network traffic analysis and threat detection tool</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
