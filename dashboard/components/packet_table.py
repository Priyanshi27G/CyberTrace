import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from src.utils.helpers import format_timestamp, format_bytes

def render_packet_table(packets_data: List[Dict[str, Any]]):
    if not packets_data:
        st.info("No packets captured yet. Start the sniffer or upload a PCAP file.")
        return
        
    df = pd.DataFrame(packets_data)
    
    # Format columns
    df['Time'] = df['timestamp'].apply(format_timestamp)
    df['Size'] = df['length'].apply(format_bytes)
    
    # Select and rename columns for display
    display_df = df[['Time', 'src_ip', 'dst_ip', 'protocol', 'Size', 'summary']]
    display_df.columns = ['Time', 'Source IP', 'Dest IP', 'Protocol', 'Size', 'Summary']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
