import streamlit as st
from typing import List
from src.models.alert import Alert
from src.utils.helpers import format_timestamp

def render_alert_panel(alerts: List[Alert]):
    if not alerts:
        st.success("No active threats detected. Network is secure.")
        return
        
    st.error(f"{len(alerts)} Active Threats Detected!")
    
    for alert in alerts:
        severity_class = f"alert-{alert.severity.value.lower()}"
        
        # HTML/CSS driven alert card
        html = f"""
        <div class="alert-card {severity_class}">
            <div class="alert-title">[{alert.severity.value.upper()}] {alert.threat_type.name}</div>
            <div class="alert-desc">
                <b>Source IP:</b> {alert.source_ip} <br/>
                <b>Time:</b> {format_timestamp(alert.timestamp)} <br/>
                <b>Details:</b> {alert.description}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        if st.button(f"Acknowledge", key=f"ack_{alert.alert_id}"):
            st.session_state.alert_manager.acknowledge(alert.alert_id)
            st.rerun()
