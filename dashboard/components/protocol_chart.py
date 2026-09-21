import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_protocol_chart(packets_data: List[Dict[str, Any]]):
    if not packets_data:
        st.info("No data for chart")
        return
        
    df = pd.DataFrame(packets_data)
    proto_counts = df['protocol'].value_counts().reset_index()
    proto_counts.columns = ['Protocol', 'Count']
    
    fig = px.pie(
        proto_counts, 
        values='Count', 
        names='Protocol',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0')
    )
    
    st.plotly_chart(fig, use_container_width=True)
