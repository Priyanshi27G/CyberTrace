import streamlit as st
import os
import tempfile
from dashboard.components.metric_cards import render_metric_cards
from dashboard.components.geo_map import render_geo_map
from dashboard.components.timeline_chart import render_timeline_chart
from dashboard.components.protocol_chart import render_protocol_chart
from dashboard.components.packet_table import render_packet_table
from dashboard.components.alert_panel import render_alert_panel
from dashboard.components.top_talkers_chart import render_top_talkers
from dashboard.components.severity_chart import render_severity_chart
from src.capture.pcap_reader import PCAPReader
from src.detectors.dos_detector import DoSDetector
from src.detectors.port_scan_detector import PortScanDetector
from src.detectors.dns_anomaly_detector import DNSAnomalyDetector
from src.models.alert import Alert

def _run_detectors(packets_data):
    """Run threat detectors on parsed packets and return alerts."""
    from src.models.packet import PacketData
    
    detectors = [DoSDetector(), PortScanDetector(), DNSAnomalyDetector()]
    alerts = []
    
    for p in packets_data:
        pkt = PacketData(
            timestamp=p['timestamp'], src_ip=p['src_ip'], dst_ip=p['dst_ip'],
            protocol=p['protocol'], length=p['length'],
            src_port=p.get('src_port'), dst_port=p.get('dst_port'),
            flags=p.get('flags'), summary=p.get('summary', '')
        )
        for det in detectors:
            alert = det.detect(pkt)
            if alert:
                alerts.append(alert)
    
    return alerts

def render_pcap_forensics():
    st.markdown('<div class="ct-section-title">PCAP Forensics</div>', unsafe_allow_html=True)
    theme = st.session_state.get('theme', 'dark')
    
    uploaded_file = st.file_uploader("Upload a PCAP file for analysis", type=["pcap", "pcapng"])
    
    if uploaded_file is not None:
        with st.spinner("Parsing PCAP file..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            try:
                reader = PCAPReader(tmp_path)
                reader.start()
                packets = reader.get_packets(10000)
                reader.stop()
                
                if not packets:
                    st.warning("No packets found in file.")
                    return
                    
                packets_data = [
                    {
                        "timestamp": p.timestamp, "src_ip": p.src_ip, "dst_ip": p.dst_ip,
                        "protocol": p.protocol, "length": p.length,
                        "src_port": p.src_port, "dst_port": p.dst_port,
                        "flags": p.flags, "summary": p.summary
                    } for p in packets
                ]
                
                # Run threat detection on PCAP data
                pcap_alerts = _run_detectors(packets_data)
                
                st.success(f"Loaded {len(packets)} packets — {len(pcap_alerts)} threats detected")
                
                # Summary metrics
                unique_ips = len(set(p['src_ip'] for p in packets_data))
                protocols = len(set(p['protocol'] for p in packets_data))
                render_metric_cards(len(packets_data), len(pcap_alerts), unique_ips, protocols)
                
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                
                # Tabbed layout
                tab_analysis, tab_packets, tab_threats = st.tabs(["📊 Analysis", "📋 Packets", "🚨 Threats"])
                
                with tab_analysis:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown('<div class="ct-section-title">Traffic Timeline</div>', unsafe_allow_html=True)
                        render_timeline_chart(packets_data, theme)
                    with col2:
                        st.markdown('<div class="ct-section-title">Protocol Breakdown</div>', unsafe_allow_html=True)
                        render_protocol_chart(packets_data, theme)
                    
                    col_map, col_talkers = st.columns([2, 1])
                    with col_map:
                        st.markdown('<div class="ct-section-title">GeoIP Map (Source IPs)</div>', unsafe_allow_html=True)
                        render_geo_map(packets_data)
                    with col_talkers:
                        st.markdown('<div class="ct-section-title">Top Talkers</div>', unsafe_allow_html=True)
                        render_top_talkers(packets_data, theme)
                
                with tab_packets:
                    st.markdown('<div class="ct-section-title">Packet Data</div>', unsafe_allow_html=True)
                    render_packet_table(packets_data)
                
                with tab_threats:
                    if pcap_alerts:
                        col_sev, col_alerts = st.columns([1, 2])
                        with col_sev:
                            st.markdown('<div class="ct-section-title">Severity Breakdown</div>', unsafe_allow_html=True)
                            render_severity_chart(pcap_alerts, theme)
                        with col_alerts:
                            st.markdown('<div class="ct-section-title">Detected Threats</div>', unsafe_allow_html=True)
                            render_alert_panel(pcap_alerts)
                    else:
                        st.success("No threats detected in this PCAP file.")
                
            except Exception as e:
                st.error(f"Error processing PCAP: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    else:
        st.markdown("""
        <div class="ct-card" style="text-align:center; padding:40px;">
            <div style="font-size:3rem; margin-bottom:10px;">📂</div>
            <div style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">Upload a PCAP File</div>
            <div style="color:var(--text-secondary); font-size:0.9rem;">
                Drag and drop a .pcap or .pcapng file above to begin forensic analysis.<br/>
                The tool will analyze traffic patterns, detect threats, and map IP locations.
            </div>
        </div>
        """, unsafe_allow_html=True)
