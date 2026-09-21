import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

def render_timeline_chart(packets_data: List[Dict[str, Any]]):
    if not packets_data:
        st.info("No data for timeline")
        return
        
    df = pd.DataFrame(packets_data)
    
    # Convert timestamp to datetime and bin by second
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['second'] = df['datetime'].dt.floor('S')
    
    # Count packets per second
    timeline_df = df.groupby('second').size().reset_index(name='Packets')
    
    fig = px.line(
        timeline_df, 
        x='second', 
        y='Packets',
        color_discrete_sequence=["#4FC3F7"]
    )
    
    fig.update_layout(
        margin=dict(t=10, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'),
        xaxis_title="Time",
        yaxis_title="Packets/sec"
    )
    
    st.plotly_chart(fig, use_container_width=True)
