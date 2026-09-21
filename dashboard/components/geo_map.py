import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any
from src.enrichment.geo_resolver import GeoResolver
import collections

@st.cache_resource
def get_geo_resolver():
    return GeoResolver()

def render_geo_map(packets_data: List[Dict[str, Any]]):
    if not packets_data:
        st.info("No data for map")
        return
        
    resolver = get_geo_resolver()
    
    # Extract IPs and get counts
    ips = [p['src_ip'] for p in packets_data]
    ip_counts = collections.Counter(ips)
    
    # Resolve locations
    unique_ips = list(ip_counts.keys())
    locations = resolver.resolve_batch(unique_ips)
    
    # Prepare map data
    map_data = []
    for ip, loc in locations.items():
        if loc['status'] == 'success':
            map_data.append({
                'IP': ip,
                'Country': loc['country'],
                'City': loc['city'],
                'lat': loc['lat'],
                'lon': loc['lon'],
                'Packets': ip_counts[ip]
            })
            
    if not map_data:
        st.warning("Could not map any IP addresses (might be local network only).")
        return
        
    df = pd.DataFrame(map_data)
    
    fig = px.scatter_mapbox(
        df, 
        lat="lat", 
        lon="lon", 
        hover_name="IP", 
        hover_data=["Country", "City", "Packets"],
        color_discrete_sequence=["#4FC3F7"],
        zoom=1,
        size="Packets",
        mapbox_style="carto-darkmatter"
    )
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
