import streamlit as st

def render_sidebar() -> str:
    with st.sidebar:
        # App branding
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 5px 0;">
            <span style="font-size:2rem;">🔍</span>
            <h2 style="margin:5px 0 0 0; font-weight:700; letter-spacing:-0.5px;">CyberTrace</h2>
            <p style="margin:0; font-size:0.8rem; color:var(--text-muted);">Network Traffic & Threat Monitor</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Theme toggle
        theme = st.toggle("☀️ Light Mode", value=False, key="theme_toggle")
        if theme:
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"
        
        st.divider()
        
        # Navigation
        page = st.radio(
            "Navigation",
            options=["📡 Live Monitor", "🔬 PCAP Forensics", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # System status
        is_sniffing = False
        if 'capture_engine' in st.session_state:
            is_sniffing = st.session_state.capture_engine.is_active()
        
        status_class = "ct-badge-active" if is_sniffing else "ct-badge-inactive"
        status_text = "Capturing" if is_sniffing else "Idle"
        
        st.markdown(f"""
        <div class="ct-card" style="padding:14px;">
            <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;">System Status</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.85rem;">Capture</span>
                <span class="ct-status-badge {status_class}">{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        if 'db' in st.session_state:
            try:
                conn = st.session_state.db._get_conn()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM alerts WHERE acknowledged = 0")
                alert_count = cursor.fetchone()[0]
                cursor.execute("SELECT MAX(id) FROM packets")
                pkt_count = cursor.fetchone()[0] or 0
                
                st.markdown(f"""
                <div class="ct-card" style="padding:14px; margin-top:10px;">
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;">Quick Stats</div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="font-size:0.85rem;">Packets</span>
                        <span style="font-weight:600; color:var(--accent-primary);">{pkt_count:,}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:0.85rem;">Alerts</span>
                        <span style="font-weight:600; color:{'var(--danger)' if alert_count > 0 else 'var(--accent-primary)'};">{alert_count}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception:
                pass
        
        # Clean page name (strip emoji)
        page_map = {
            "📡 Live Monitor": "Live Monitor",
            "🔬 PCAP Forensics": "PCAP Forensics",
            "⚙️ Settings": "Settings"
        }
        return page_map.get(page, "Live Monitor")
