import streamlit as st

def render_sidebar() -> str:
    with st.sidebar:
        st.title("🔍 CyberTrace")
        st.markdown("Network Traffic & Threat Monitor")
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Select View",
            options=["Live Monitor", "PCAP Forensics", "Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick Stats
        st.subheader("Quick Stats")
        if 'db' in st.session_state:
            alerts = st.session_state.db.get_active_alerts()
            st.metric("Active Alerts", len(alerts))
            
            # Count packets roughly by checking last id
            conn = st.session_state.db._get_conn()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT MAX(id) FROM packets")
                count = cursor.fetchone()[0] or 0
                st.metric("Packets Captured", count)
            except Exception:
                pass
                
        return page
