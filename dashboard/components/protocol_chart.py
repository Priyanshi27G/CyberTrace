import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_protocol_chart(packets_data: List[Dict[str, Any]], theme: str = 'dark'):
    if not packets_data:
        st.info("No data for chart")
        return
        
    df = pd.DataFrame(packets_data)
    proto_counts = df['protocol'].value_counts().reset_index()
    proto_counts.columns = ['Protocol', 'Count']
    
    # Use warm colors instead of default
    colors = ['#10B981', '#F59E0B', '#06B6D4', '#EF4444', '#8B5CF6', '#EC4899', '#F97316']
    
    fig = px.pie(
        proto_counts, values='Count', names='Protocol',
        hole=0.45, color_discrete_sequence=colors
    )
    
    template = 'plotly_dark' if theme == 'dark' else 'plotly_white'
    fig.update_layout(
        template=template,
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        showlegend=True,
        legend=dict(font=dict(size=11))
    )
    
    st.plotly_chart(fig)
