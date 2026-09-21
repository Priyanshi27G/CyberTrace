import streamlit as st
import os
import tempfile
from dashboard.components.geo_map import render_geo_map
from dashboard.components.timeline_chart import render_timeline_chart
from dashboard.components.protocol_chart import render_protocol_chart
from dashboard.components.packet_table import render_packet_table
from src.capture.pcap_reader import PCAPReader

def render_pcap_forensics():
    st.header("PCAP Forensics")
    
    uploaded_file = st.file_uploader("Upload a PCAP file for analysis", type=["pcap", "pcapng"])
    
    if uploaded_file is not None:
        with st.spinner("Parsing PCAP file..."):
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            try:
                reader = PCAPReader(tmp_path)
                reader.start()
                packets = reader.get_packets(10000) # Read up to 10k packets for demo
                reader.stop()
                
                if not packets:
                    st.warning("No packets found in file.")
                    return
                    
                # Convert to dict format expected by components
                packets_data = [
                    {
                        "timestamp": p.timestamp,
                        "src_ip": p.src_ip,
                        "dst_ip": p.dst_ip,
                        "protocol": p.protocol,
                        "length": p.length,
                        "src_port": p.src_port,
                        "dst_port": p.dst_port,
                        "flags": p.flags,
                        "summary": p.summary
                    } for p in packets
                ]
                
                st.success(f"Successfully loaded {len(packets)} packets!")
                
                # Layout
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.subheader("Traffic Timeline")
                    render_timeline_chart(packets_data)
                with col2:
                    st.subheader("Protocol Breakdown")
                    render_protocol_chart(packets_data)
                    
                st.divider()
                st.subheader("GeoIP Map (Source IPs)")
                render_geo_map(packets_data)
                
                st.divider()
                st.subheader("Packet Data")
                render_packet_table(packets_data)
                
            except Exception as e:
                st.error(f"Error processing PCAP: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    else:
        st.info("Please upload a .pcap file to begin forensics analysis.")
