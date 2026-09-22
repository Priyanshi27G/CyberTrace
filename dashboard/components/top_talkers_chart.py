import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_top_talkers(packets_data: List[Dict[str, Any]], theme: str = 'dark'):
    if not packets_data:
        st.info("No data for top talkers")
        return
    
    df = pd.DataFrame(packets_data)
    top_ips = df['src_ip'].value_counts().head(10).reset_index()
    top_ips.columns = ['Source IP', 'Packets']
    top_ips = top_ips.iloc[::-1]
    
    fig = px.bar(
        top_ips, x='Packets', y='Source IP', orientation='h',
        color_discrete_sequence=['#10B981']
    )
    
    template = 'plotly_dark' if theme == 'dark' else 'plotly_white'
    fig.update_layout(
        template=template,
        margin=dict(t=10, b=10, l=0, r=10),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        xaxis_title='', yaxis_title=''
    )
    
    st.plotly_chart(fig, key='top_talkers')
