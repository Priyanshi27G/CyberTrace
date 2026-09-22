import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_timeline_chart(packets_data: List[Dict[str, Any]], theme: str = 'dark'):
    if not packets_data:
        st.info("No data for timeline")
        return
        
    df = pd.DataFrame(packets_data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['second'] = df['datetime'].dt.floor('s')
    
    timeline_df = df.groupby('second').size().reset_index(name='Packets')
    
    fig = px.area(
        timeline_df, x='second', y='Packets',
        color_discrete_sequence=['#10B981']
    )
    
    template = 'plotly_dark' if theme == 'dark' else 'plotly_white'
    fig.update_layout(
        template=template,
        margin=dict(t=10, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Time", yaxis_title="Packets/sec",
        height=300
    )
    # Fill area with transparency
    fig.update_traces(fillcolor='rgba(16,185,129,0.15)', line_color='#10B981')
    
    st.plotly_chart(fig)
