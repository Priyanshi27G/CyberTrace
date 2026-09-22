import streamlit as st
import plotly.graph_objects as go
from typing import List
from src.models.alert import Alert

def render_severity_chart(alerts: List[Alert], theme: str = 'dark'):
    if not alerts:
        st.info("No alerts to display")
        return
    
    severity_counts = {}
    for a in alerts:
        sev = a.severity.value.upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    labels = list(severity_counts.keys())
    values = list(severity_counts.values())
    
    colors_map = {
        'CRITICAL': '#EF4444', 'HIGH': '#F59E0B',
        'MEDIUM': '#FBBF24', 'LOW': '#06B6D4'
    }
    marker_colors = [colors_map.get(l, '#6B7280') for l in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.5,
        marker=dict(colors=marker_colors),
        textinfo='label+value', textposition='outside'
    )])
    
    template = 'plotly_dark' if theme == 'dark' else 'plotly_white'
    fig.update_layout(
        template=template,
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300, showlegend=False
    )
    
    st.plotly_chart(fig, key='severity_chart')
