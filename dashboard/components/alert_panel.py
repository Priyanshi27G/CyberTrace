import streamlit as st
from typing import List
from src.models.alert import Alert
from src.utils.helpers import format_timestamp

def render_alert_panel(alerts: List[Alert]):
    if not alerts:
        st.markdown("""
        <div class="ct-card" style="text-align:center; padding:30px;">
            <div style="font-size:2rem; margin-bottom:8px;">✅</div>
            <div style="color:var(--success); font-weight:600;">No Active Threats</div>
            <div style="color:var(--text-muted); font-size:0.85rem;">Network is secure</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for alert in alerts:
        sev = alert.severity.value.lower()
        sev_class = f"ct-alert-{sev}"
        sev_label = alert.severity.value.upper()
        
        # Severity color for the badge
        sev_colors = {
            'critical': '#EF4444', 'high': '#F59E0B',
            'medium': '#FBBF24', 'low': '#06B6D4'
        }
        badge_color = sev_colors.get(sev, '#6B7280')
        
        html = f"""
        <div class="ct-alert-card {sev_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="ct-alert-title">{alert.threat_type.name.replace('_', ' ')}</span>
                <span class="ct-status-badge" style="background:rgba({','.join(str(int(badge_color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15); color:{badge_color};">{sev_label}</span>
            </div>
            <div class="ct-alert-desc">
                <b>Source:</b> {alert.source_ip}<br/>
                <b>Time:</b> {format_timestamp(alert.timestamp)}<br/>
                {alert.description}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        # Only show acknowledge button for DB-stored alerts (not PCAP analysis)
        if alert.alert_id > 0:
            if st.button("Acknowledge", key=f"ack_{alert.alert_id}"):
                st.session_state.alert_manager.acknowledge(alert.alert_id)
                st.rerun()
