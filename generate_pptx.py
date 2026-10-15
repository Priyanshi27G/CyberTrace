from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt
import copy
from lxml import etree

# -----------------------------------------------------------------------
# CONSTANTS (matching the institute template exactly)
# -----------------------------------------------------------------------
DARK_RED   = RGBColor(0xC0, 0x00, 0x00)   # Institute heading colour
DARK_BLUE  = RGBColor(0x00, 0x20, 0x60)   # Sub-heading colour
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
CYBER_BLUE = RGBColor(0x00, 0x70, 0xC0)   # accent for cyber theme
DARK_BG    = RGBColor(0x1F, 0x35, 0x64)   # slide content-area bg
ACCENT     = RGBColor(0x00, 0xB0, 0xF0)   # light cyan accent

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# -----------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------
def set_bg_color(slide, rgb: RGBColor):
    """Solid background colour for a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = rgb

def add_rect(slide, left, top, width, height, fill_rgb=None, line_rgb=None, line_width_pt=1):
    from pptx.util import Pt
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.line.width = Pt(line_width_pt) if line_rgb else Pt(0)
    if line_rgb:
        shape.line.color.rgb = line_rgb
    else:
        shape.line.fill.background()
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    return shape

def add_textbox(slide, left, top, width, height, text, font_size, bold=False,
                color=None, align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return txBox

def add_bullet_box(slide, left, top, width, height, bullets, font_size=16,
                   color=None, indent_pt=14):
    """Add a textbox with multiple bullet-point paragraphs."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for bullet in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = bullet
        p.alignment = PP_ALIGN.LEFT
        # indent
        from pptx.oxml.ns import qn
        pPr = p._p.get_or_add_pPr()
        pPr.set('indent', str(int(-Pt(indent_pt))))
        pPr.set('marL', str(int(Pt(indent_pt * 2))))
        p.space_before = Pt(4)
        if p.runs:
            p.runs[0].font.size = Pt(font_size)
            p.runs[0].font.bold = False
            if color:
                p.runs[0].font.color.rgb = color

def add_divider(slide, left, top, width, color=DARK_RED, thickness_pt=2.5):
    shape = slide.shapes.add_shape(1, left, top, width, Pt(thickness_pt))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    return shape

def slide_header(slide, title_text, subtitle=None):
    """Standard content slide header: dark banner + title."""
    # Top dark banner
    add_rect(slide, 0, 0, SLIDE_W, Inches(1.4), fill_rgb=DARK_BG)
    # Accent left bar
    add_rect(slide, 0, 0, Inches(0.12), Inches(1.4), fill_rgb=DARK_RED)
    # Slide title
    add_textbox(slide, Inches(0.3), Inches(0.2), Inches(12.5), Inches(1.0),
                title_text, font_size=30, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_textbox(slide, Inches(0.3), Inches(0.82), Inches(12.5), Inches(0.5),
                    subtitle, font_size=13, bold=False, color=ACCENT, align=PP_ALIGN.LEFT)

def footer_bar(slide):
    """Bottom thin accent bar for all slides."""
    add_rect(slide, 0, SLIDE_H - Inches(0.12), SLIDE_W, Inches(0.12), fill_rgb=DARK_RED)

# -----------------------------------------------------------------------
# BUILD PRESENTATION
# -----------------------------------------------------------------------
def build_ppt(template_path, output_path):
    prs = Presentation(template_path)

    # We'll rebuild only slides we care about (1-9) in-place.
    # Since python-pptx can't delete/reorder easily while preserving template,
    # we clear existing shapes and redraw each slide.

    def clear_slide(slide):
        sp_tree = slide.shapes._spTree
        # Remove all but background / slide-xml wrappers
        for sp in list(sp_tree):
            tag = sp.tag.split('}')[-1]
            if tag in ('sp', 'pic', 'cxnSp', 'graphicFrame', 'grpSp'):
                sp_tree.remove(sp)

    slides = prs.slides

    # ==========================================================
    # SLIDE 1: Title Slide
    # ==========================================================
    sl = slides[0]
    clear_slide(sl)
    set_bg_color(sl, RGBColor(0xFF, 0xFF, 0xFF))

    # Top dark header strip
    add_rect(sl, 0, 0, SLIDE_W, Inches(1.1), fill_rgb=DARK_BG)
    add_rect(sl, 0, 0, Inches(0.18), Inches(1.1), fill_rgb=DARK_RED)
    # Institute name
    add_textbox(sl, Inches(0.35), Inches(0.12), Inches(12.6), Inches(0.5),
                "Indore Institute of Science & Technology",
                font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(sl, Inches(0.35), Inches(0.62), Inches(12.6), Inches(0.35),
                "Department of Information Technology",
                font_size=16, bold=False, color=ACCENT, align=PP_ALIGN.CENTER)

    # Middle section
    add_textbox(sl, Inches(1), Inches(1.3), Inches(11.3), Inches(0.45),
                "A Minor Project Presentation on",
                font_size=15, bold=False, color=DARK_BLUE, align=PP_ALIGN.CENTER)

    # Big project title box  (dark bg, white text) – centred
    title_box = add_rect(sl, Inches(1.5), Inches(2.0), Inches(10.3), Inches(1.6),
                         fill_rgb=DARK_BG)
    # accent lines beside title box
    add_rect(sl, Inches(1.5), Inches(2.0), Inches(0.08), Inches(1.6), fill_rgb=DARK_RED)
    add_rect(sl, Inches(11.72), Inches(2.0), Inches(0.08), Inches(1.6), fill_rgb=DARK_RED)
    add_textbox(sl, Inches(1.7), Inches(2.1), Inches(10.0), Inches(0.55),
                "CYBERTRACE",
                font_size=34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(sl, Inches(1.7), Inches(2.65), Inches(10.0), Inches(0.75),
                "Real-Time Network Security Monitoring\n& Anomaly Detection System",
                font_size=18, bold=False, color=ACCENT, align=PP_ALIGN.CENTER)

    # Horizontal divider
    add_divider(sl, Inches(1.3), Inches(3.85), Inches(10.7), color=DARK_RED, thickness_pt=1.5)

    # Guided by / Presented by
    add_textbox(sl, Inches(1.0), Inches(4.05), Inches(4.5), Inches(0.45),
                "Guided By:", font_size=14, bold=True, color=DARK_BLUE)
    add_textbox(sl, Inches(1.0), Inches(4.5), Inches(4.5), Inches(0.75),
                "[Professor Name]\nDepartment of IT", font_size=13, bold=False, color=RGBColor(0x33,0x33,0x33))

    add_textbox(sl, Inches(7.5), Inches(4.05), Inches(4.5), Inches(0.45),
                "Presented By:", font_size=14, bold=True, color=DARK_BLUE, align=PP_ALIGN.LEFT)
    add_textbox(sl, Inches(7.5), Inches(4.5), Inches(4.5), Inches(0.75),
                "Priyanshi Gupta  [Enrollment No.]\n[Team Member Names]",
                font_size=13, bold=False, color=RGBColor(0x33,0x33,0x33))

    # Session / Year
    add_textbox(sl, Inches(3.5), Inches(5.5), Inches(6.0), Inches(0.45),
                "Academic Year: 2024 – 2025",
                font_size=13, bold=False, color=DARK_BLUE, align=PP_ALIGN.CENTER)

    footer_bar(sl)

    # ==========================================================
    # SLIDE 2: Outline / Table of Contents
    # ==========================================================
    sl = slides[1]
    clear_slide(sl)
    set_bg_color(sl, LIGHT_GRAY)
    slide_header(sl, "Outline", "Topics Covered in This Presentation")
    footer_bar(sl)

    topics = [
        ("01", "Proposed Area & Topic"),
        ("02", "Introduction"),
        ("03", "Objectives"),
        ("04", "Proposed Methodology"),
        ("05", "Technical Details"),
        ("06", "Expected Outcome"),
        ("07", "References"),
    ]
    cols = 2
    box_w = Inches(5.5)
    box_h = Inches(0.62)
    start_x = [Inches(0.7), Inches(7.0)]
    start_y = Inches(1.65)
    gap_y = Inches(0.72)

    for idx, (num, name) in enumerate(topics):
        col = idx % cols
        row = idx // cols
        x = start_x[col]
        y = start_y + row * gap_y

        add_rect(sl, x, y, box_w, box_h, fill_rgb=DARK_BG)
        add_rect(sl, x, y, Inches(0.55), box_h, fill_rgb=DARK_RED)
        add_textbox(sl, x + Inches(0.05), y + Inches(0.06), Inches(0.5), Inches(0.5),
                    num, font_size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, x + Inches(0.65), y + Inches(0.1), Inches(4.7), Inches(0.45),
                    name, font_size=17, bold=True, color=WHITE)

    # ==========================================================
    # SLIDE 3: Proposed Area and Topic
    # ==========================================================
    sl = slides[2]
    clear_slide(sl)
    set_bg_color(sl, RGBColor(0xFF, 0xFF, 0xFF))
    slide_header(sl, "Proposed Area & Topic", "Problem Domain  |  Research Focus  |  Motivation")
    footer_bar(sl)

    # Left column: Area card
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(5.8), Inches(5.6), fill_rgb=LIGHT_GRAY)
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(5.8), Inches(0.5), fill_rgb=DARK_RED)
    add_textbox(sl, Inches(0.6), Inches(1.6), Inches(5.5), Inches(0.4),
                "AREA", font_size=14, bold=True, color=WHITE)
    area_pts = [
        "• Cybersecurity & Network Traffic Analysis",
        "• Intrusion Detection Systems (IDS)",
        "• Real-time Packet Monitoring",
    ]
    y_off = Inches(2.18)
    for pt in area_pts:
        add_textbox(sl, Inches(0.65), y_off, Inches(5.5), Inches(0.6),
                    pt, font_size=15, color=RGBColor(0x20,0x20,0x20))
        y_off += Inches(0.62)

    add_textbox(sl, Inches(0.6), Inches(4.0), Inches(5.5), Inches(0.4),
                "MOTIVATION", font_size=13, bold=True, color=DARK_RED)
    add_textbox(sl, Inches(0.6), Inches(4.4), Inches(5.5), Inches(1.6),
                "Cyber attacks are rising exponentially. Traditional monitoring tools are complex and siloed. CyberTrace aims to bring clarity and simplicity to network threat detection using open-source technology.",
                font_size=14, color=RGBColor(0x33,0x33,0x33))

    # Right column: Topic box
    add_rect(sl, Inches(6.6), Inches(1.55), Inches(6.2), Inches(5.6), fill_rgb=DARK_BG)
    add_rect(sl, Inches(6.6), Inches(1.55), Inches(6.2), Inches(0.5), fill_rgb=CYBER_BLUE)
    add_textbox(sl, Inches(6.7), Inches(1.6), Inches(6.0), Inches(0.4),
                "TOPIC", font_size=14, bold=True, color=WHITE)
    add_textbox(sl, Inches(6.7), Inches(2.18), Inches(5.8), Inches(0.5),
                "CyberTrace", font_size=24, bold=True, color=ACCENT)
    add_textbox(sl, Inches(6.7), Inches(2.78), Inches(5.8), Inches(0.7),
                "Real-Time Network Security Monitoring\n& Anomaly Detection System",
                font_size=15, bold=False, color=WHITE)
    add_divider(sl, Inches(6.7), Inches(3.6), Inches(5.5), color=DARK_RED, thickness_pt=1.5)
    add_textbox(sl, Inches(6.7), Inches(3.75), Inches(5.8), Inches(3.1),
                "The project captures live or recorded network packets, passes them through anomaly detection engines (rule-based + ML thresholding), and displays real-time metrics on a modern web dashboard built with React + FastAPI.",
                font_size=14, color=WHITE)

    # ==========================================================
    # SLIDE 4: Introduction
    # ==========================================================
    sl = slides[3]
    clear_slide(sl)
    set_bg_color(sl, LIGHT_GRAY)
    slide_header(sl, "Introduction", "What is CyberTrace?  |  Why does it matter?")
    footer_bar(sl)

    # Top quote box
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(12.3), Inches(0.85), fill_rgb=DARK_BG)
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(0.1), Inches(0.85), fill_rgb=ACCENT)
    add_textbox(sl, Inches(0.75), Inches(1.68), Inches(11.8), Inches(0.6),
                "\"CyberTrace bridges raw network data and actionable security intelligence — in real time.\"",
                font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, italic=True)

    # Three info cards
    cards = [
        ("What It Does", "Captures & parses live or PCAP-based network packets and runs them through multiple detection algorithms to flag threats automatically."),
        ("How It Works", "A decoupled architecture: Scapy handles capture, FastAPI serves a RESTful API, and React renders beautiful, real-time dashboards."),
        ("Why It Matters", "Early threat detection reduces incident response time. CyberTrace makes that accessible to students and small teams without enterprise cost."),
    ]
    card_w = Inches(3.9)
    card_x_list = [Inches(0.5), Inches(4.7), Inches(8.9)]
    for (title, body), cx in zip(cards, card_x_list):
        add_rect(sl, cx, Inches(2.6), card_w, Inches(4.4), fill_rgb=RGBColor(0xFF,0xFF,0xFF))
        add_rect(sl, cx, Inches(2.6), card_w, Inches(0.55), fill_rgb=DARK_RED)
        add_textbox(sl, cx+Inches(0.1), Inches(2.65), card_w-Inches(0.2), Inches(0.45),
                    title, font_size=14, bold=True, color=WHITE)
        add_textbox(sl, cx+Inches(0.15), Inches(3.28), card_w-Inches(0.3), Inches(3.6),
                    body, font_size=13, color=RGBColor(0x33,0x33,0x33))

    # ==========================================================
    # SLIDE 5: Objectives
    # ==========================================================
    sl = slides[4]
    clear_slide(sl)
    set_bg_color(sl, RGBColor(0xFF,0xFF,0xFF))
    slide_header(sl, "Objectives", "Clear Goals for the CyberTrace Project")
    footer_bar(sl)

    objectives = [
        ("01", "Packet Capture", "Efficiently capture and parse live or file-based network traffic using Scapy."),
        ("02", "Anomaly Detection", "Detect threats like DoS attacks, Port Scans, and DNS anomalies in real time."),
        ("03", "Web Dashboard", "Provide an intuitive, responsive UI to visualize traffic metrics and alerts."),
        ("04", "PCAP Forensics", "Allow post-incident analysis by uploading .pcap files for offline investigation."),
        ("05", "Decoupled Design", "Implement a modern, scalable architecture (FastAPI backend + React frontend)."),
    ]

    obj_w = Inches(12.0)
    obj_h = Inches(0.75)
    for i, (num, title, desc) in enumerate(objectives):
        y = Inches(1.55) + i * (obj_h + Inches(0.1))
        bg = DARK_BG if i % 2 == 0 else RGBColor(0xE8, 0xEF, 0xF8)
        txt_col = WHITE if i % 2 == 0 else RGBColor(0x1F,0x35,0x64)
        desc_col = ACCENT if i % 2 == 0 else RGBColor(0x00,0x70,0xC0)
        add_rect(sl, Inches(0.65), y, obj_w, obj_h, fill_rgb=bg)
        add_rect(sl, Inches(0.65), y, Inches(0.6), obj_h, fill_rgb=DARK_RED)
        add_textbox(sl, Inches(0.67), y+Inches(0.12), Inches(0.58), Inches(0.5),
                    num, font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, Inches(1.4), y+Inches(0.08), Inches(2.8), Inches(0.4),
                    title, font_size=15, bold=True, color=txt_col)
        add_textbox(sl, Inches(4.3), y+Inches(0.08), Inches(8.0), Inches(0.5),
                    desc, font_size=13, color=desc_col)

    # ==========================================================
    # SLIDE 6: Proposed Methodology
    # ==========================================================
    sl = slides[5]
    clear_slide(sl)
    set_bg_color(sl, LIGHT_GRAY)
    slide_header(sl, "Proposed Methodology", "System Architecture  |  Data Flow  |  Algorithm")
    footer_bar(sl)

    layers = [
        ("Layer 1", "Data Capture", "Scapy sniffs packets from network interface OR reads .pcap files via PCAPReader class.", DARK_RED),
        ("Layer 2", "Detection Engine", "Each packet is passed through DoSDetector, PortScanDetector, DNSAnomalyDetector, and MLAnomalyDetector.", CYBER_BLUE),
        ("Layer 3", "Backend API", "FastAPI exposes /api/metrics, /api/alerts, and /api/upload_pcap endpoints. WebSocket for live streaming.", DARK_BLUE),
        ("Layer 4", "Frontend UI", "React + Vite renders dashboards with charts, alert panels, and a PCAP Forensics upload page.", RGBColor(0x00,0x80,0x00)),
    ]

    arrow_x = Inches(6.45)
    for i, (num, title, desc, col) in enumerate(layers):
        y = Inches(1.55) + i * Inches(1.25)
        add_rect(sl, Inches(0.5), y, Inches(5.7), Inches(1.05), fill_rgb=RGBColor(0xFF,0xFF,0xFF))
        add_rect(sl, Inches(0.5), y, Inches(1.1), Inches(1.05), fill_rgb=col)
        add_textbox(sl, Inches(0.52), y+Inches(0.05), Inches(1.06), Inches(0.45),
                    num, font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.52), y+Inches(0.5), Inches(1.06), Inches(0.45),
                    title, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, Inches(1.72), y+Inches(0.1), Inches(4.3), Inches(0.88),
                    desc, font_size=12, color=RGBColor(0x22,0x22,0x22))
        # Arrow right (except last)
        if i < len(layers)-1:
            add_textbox(sl, Inches(6.0), y+Inches(0.55), Inches(0.8), Inches(0.4),
                        "▼", font_size=18, bold=True, color=DARK_RED, align=PP_ALIGN.CENTER)

    # Right side: flow summary box
    add_rect(sl, Inches(6.7), Inches(1.55), Inches(5.9), Inches(5.1), fill_rgb=DARK_BG)
    add_rect(sl, Inches(6.7), Inches(1.55), Inches(5.9), Inches(0.5), fill_rgb=DARK_RED)
    add_textbox(sl, Inches(6.8), Inches(1.6), Inches(5.7), Inches(0.4),
                "Data Flow Summary", font_size=14, bold=True, color=WHITE)
    flow_text = (
        "Network Interface  ➜  Scapy Sniffer\n"
        "         ⬇\n"
        "Packet Parser (parse_packet)\n"
        "         ⬇\n"
        "Anomaly Detectors (4 Engines)\n"
        "         ⬇\n"
        "AlertManager  +  Database\n"
        "         ⬇\n"
        "FastAPI REST Endpoints\n"
        "         ⬇\n"
        "React Dashboard (Port 5173)"
    )
    add_textbox(sl, Inches(6.85), Inches(2.2), Inches(5.5), Inches(4.2),
                flow_text, font_size=13, bold=False, color=WHITE)

    # ==========================================================
    # SLIDE 7: Technical Details
    # ==========================================================
    sl = slides[6]
    clear_slide(sl)
    set_bg_color(sl, RGBColor(0xFF,0xFF,0xFF))
    slide_header(sl, "Technical Details", "Hardware & Software Requirements  |  Tech Stack")
    footer_bar(sl)

    # Hardware card
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(5.6), Inches(5.5), fill_rgb=LIGHT_GRAY)
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(5.6), Inches(0.55), fill_rgb=DARK_BLUE)
    add_textbox(sl, Inches(0.6), Inches(1.6), Inches(5.4), Inches(0.45),
                "⚙  Hardware Requirements", font_size=14, bold=True, color=WHITE)
    hw = [
        "• Standard PC / Laptop",
        "• Minimum 4 GB RAM (8 GB Recommended)",
        "• Multi-core Processor (Intel i3+ / AMD Ryzen 3+)",
        "• Network Interface Card (NIC) for live capture",
        "• 500 MB free disk space",
    ]
    for i, item in enumerate(hw):
        add_textbox(sl, Inches(0.65), Inches(2.25) + i*Inches(0.65), Inches(5.2), Inches(0.55),
                    item, font_size=13, color=RGBColor(0x22,0x22,0x22))

    # Software card
    add_rect(sl, Inches(6.6), Inches(1.55), Inches(6.2), Inches(5.5), fill_rgb=DARK_BG)
    add_rect(sl, Inches(6.6), Inches(1.55), Inches(6.2), Inches(0.55), fill_rgb=DARK_RED)
    add_textbox(sl, Inches(6.7), Inches(1.6), Inches(6.0), Inches(0.45),
                "💻  Tech Stack", font_size=14, bold=True, color=WHITE)
    sw = [
        ("Language", "Python 3.x  |  JavaScript (ES2022)"),
        ("Capture", "Scapy (Packet Sniffing & PCAP Parsing)"),
        ("Backend", "FastAPI + Uvicorn (REST API, WebSocket)"),
        ("Frontend", "React JS + Vite + TailwindCSS + DaisyUI"),
        ("Charts", "Recharts (Interactive Data Visualizations)"),
        ("Database", "SQLite (via SQLAlchemy ORM)"),
        ("OS Support", "Linux (Recommended)  |  Windows"),
    ]
    for i, (key, val) in enumerate(sw):
        y = Inches(2.22) + i*Inches(0.62)
        add_textbox(sl, Inches(6.7), y, Inches(2.0), Inches(0.5),
                    key + ":", font_size=12, bold=True, color=ACCENT)
        add_textbox(sl, Inches(8.85), y, Inches(3.8), Inches(0.5),
                    val, font_size=12, bold=False, color=WHITE)

    # ==========================================================
    # SLIDE 8: Expected Outcome
    # ==========================================================
    sl = slides[7]
    clear_slide(sl)
    set_bg_color(sl, LIGHT_GRAY)
    slide_header(sl, "Expected Outcome", "Deliverables  |  Results  |  Impact")
    footer_bar(sl)

    outcomes = [
        ("🛡", "Functional Prototype", "A working system capable of real-time packet sniffing, anomaly detection, and alert generation."),
        ("📊", "Modern Web Dashboard", "A premium React-based UI with live metrics, chart visualizations, and a threat alert panel."),
        ("🔍", "PCAP Forensics Module", "Post-incident analysis by uploading .pcap files to extract packets and generate threat reports."),
        ("🏗", "Scalable Architecture", "A fully decoupled FastAPI + React pattern that can be easily extended for production use."),
    ]
    card_w = Inches(5.7)
    positions = [
        (Inches(0.5), Inches(1.55)),
        (Inches(6.9), Inches(1.55)),
        (Inches(0.5), Inches(4.25)),
        (Inches(6.9), Inches(4.25)),
    ]
    for (icon, title, desc), (cx, cy) in zip(outcomes, positions):
        add_rect(sl, cx, cy, card_w, Inches(2.3), fill_rgb=RGBColor(0xFF,0xFF,0xFF))
        add_rect(sl, cx, cy, card_w, Inches(0.08), fill_rgb=DARK_RED)  # top border
        add_textbox(sl, cx+Inches(0.15), cy+Inches(0.15), Inches(0.6), Inches(0.5),
                    icon, font_size=24, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx+Inches(0.85), cy+Inches(0.18), Inches(4.6), Inches(0.45),
                    title, font_size=15, bold=True, color=DARK_BLUE)
        add_textbox(sl, cx+Inches(0.15), cy+Inches(0.75), Inches(5.4), Inches(1.4),
                    desc, font_size=13, color=RGBColor(0x33,0x33,0x33))

    # ==========================================================
    # SLIDE 9: References  (no overlap fix!)
    # ==========================================================
    sl = slides[8]
    clear_slide(sl)
    set_bg_color(sl, RGBColor(0xFF,0xFF,0xFF))
    slide_header(sl, "References", "")
    footer_bar(sl)

    refs = [
        "[1]  RFC 793 – Transmission Control Protocol (TCP). IETF, 1981.",
        "[2]  Scapy Documentation – Packet Manipulation Library. https://scapy.net",
        "[3]  FastAPI Official Documentation – High Performance APIs with Python. https://fastapi.tiangolo.com",
        "[4]  React JS Official Documentation – A JavaScript Library for Building UIs. https://react.dev",
        "[5]  V. Chandola, A. Banerjee, V. Kumar – \"Anomaly Detection: A Survey\". ACM Computing Surveys, 2009.",
        "[6]  TailwindCSS & DaisyUI Component Library – https://daisyui.com",
    ]
    add_rect(sl, Inches(0.5), Inches(1.55), Inches(12.3), Inches(5.5), fill_rgb=LIGHT_GRAY)
    for i, ref in enumerate(refs):
        y = Inches(1.75) + i * Inches(0.82)
        add_rect(sl, Inches(0.6), y, Inches(12.1), Inches(0.72), fill_rgb=RGBColor(0xFF,0xFF,0xFF))
        add_rect(sl, Inches(0.6), y, Inches(0.07), Inches(0.72), fill_rgb=DARK_RED)
        add_textbox(sl, Inches(0.8), y+Inches(0.1), Inches(11.8), Inches(0.52),
                    ref, font_size=13, color=RGBColor(0x22,0x22,0x22))

    # Save
    prs.save(output_path)
    print(f"✅ Saved: {output_path}")


if __name__ == "__main__":
    build_ppt(
        "/home/pinkparrot/Priyanshi Gupta/format.pptx",
        "/home/pinkparrot/Priyanshi Gupta/CyberTrace/CyberTrace_Viva_Presentation.pptx"
    )
