import streamlit as st

def render_metric_cards(packets_count: int, alert_count: int, unique_ips: int, protocols_count: int):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Recent Packets", packets_count)
    with col2:
        st.metric("Active Threats", alert_count, delta_color="inverse")
    with col3:
        st.metric("Unique Source IPs", unique_ips)
    with col4:
        st.metric("Protocols Seen", protocols_count)
