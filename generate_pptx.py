import sys
from pptx import Presentation

def update_presentation(input_file, output_file):
    prs = Presentation(input_file)

    # Slide 1: Title
    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if not shape.has_text_frame: continue
        text = shape.text
        if "<<Title>>" in text:
            shape.text_frame.text = text.replace("<<Title>>", "CyberTrace:\nReal-Time Network Security Monitoring & Anomaly Detection")
        elif "<student Name><Enrollment No>" in text:
            shape.text_frame.text = text.replace("<student Name><Enrollment No>", "Priyanshi Gupta\n[Your Enrollment No]")
        elif "(All Team Members Name)" in text:
            shape.text_frame.text = text.replace("(All Team Members Name)", "[Team Member Names, if any]")

    # Slide 3: Proposed Area and Topic
    slide3 = prs.slides[2]
    for shape in slide3.shapes:
        if not shape.has_text_frame: continue
        if "Description of Proposed Area" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "Area: Cybersecurity & Network Traffic Analysis\n\nTopic: CyberTrace - A system to monitor network traffic in real-time, detect potential anomalies, and present actionable insights via an intuitive dashboard.\n\nWe chose this because network threats are increasing rapidly, and detecting them with a clear, decoupled web architecture helps in quick response."

    # Slide 4: Introduction
    slide4 = prs.slides[3]
    for shape in slide4.shapes:
        if not shape.has_text_frame: continue
        if "Brief Introduction" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "CyberTrace bridges the gap between raw network packet data and readable security intelligence.\n\nIt is designed to capture packets (live or via PCAP files), analyze them for suspicious behavior, and display metrics, protocol distributions, and threat alerts in a modern, easy-to-understand web interface."

    # Slide 5: Objectives
    slide5 = prs.slides[4]
    for shape in slide5.shapes:
        if not shape.has_text_frame: continue
        if "This section provides a clear picture" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "1. To capture and parse network traffic efficiently.\n2. To detect basic network anomalies (e.g., DoS, Port Scans) and generate alerts.\n3. To provide a user-friendly, responsive dashboard for data visualization.\n4. To support post-incident forensics via PCAP file uploads."

    # Slide 6: Proposed Methodology
    slide6 = prs.slides[5]
    for shape in slide6.shapes:
        if not shape.has_text_frame: continue
        if "Proposed Algorithm/Method" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "1. Data Capture Layer: Using Python packet sniffing (e.g., Scapy) to read network interfaces or historical PCAP files.\n2. Detection Engine Layer: Applying rule-based and basic ML threshold analysis to identify suspicious patterns.\n3. Backend API Layer: A decoupled FastAPI server to process data and serve it efficiently.\n4. Frontend UI Layer: A dynamic React-based dashboard for real-time visualization and alerting."

    # Slide 7: Technical Details
    slide7 = prs.slides[6]
    for shape in slide7.shapes:
        if not shape.has_text_frame: continue
        if "Hardware and software Requirement" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "Hardware Requirements:\n- Standard PC/Laptop (Minimum 4GB RAM, Multi-core Processor)\n- Network Interface Card (NIC)\n\nSoftware Requirements:\n- Backend: Python (FastAPI, Scapy)\n- Frontend: React JS, Vite, TailwindCSS\n- OS: Linux/Windows/macOS"

    # Slide 8: Expected Outcome
    slide8 = prs.slides[7]
    for shape in slide8.shapes:
        if not shape.has_text_frame: continue
        if "Summary of the project" in shape.text:
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "- A functional prototype capable of live network monitoring and alert generation.\n- A modern, decoupled web architecture demonstrating full-stack security application development.\n- Increased visibility into network traffic patterns to aid in basic threat hunting."

    # Slide 9: References
    slide9 = prs.slides[8]
    for shape in slide9.shapes:
        if not shape.has_text_frame: continue
        # Find the empty text box or the one under References
        if not shape.text.strip() or "References" not in shape.text:
            pass # Keep looking or just add text if it's the main body shape
            
        # The title shape usually says "References", the body shape is usually empty or has a newline.
        # Let's just find the first shape that is not the title.
        if shape.text != "References":
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            p.text = "[1] RFC 793 - Transmission Control Protocol (TCP)\n[2] Scapy Documentation for Packet Manipulation\n[3] React and FastAPI Official Documentation\n[4] IEEE papers on basic network anomaly detection."

    prs.save(output_file)
    print(f"Presentation saved successfully to {output_file}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "format.pptx"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "CyberTrace_Viva_Presentation.pptx"
    update_presentation(input_file, output_file)
