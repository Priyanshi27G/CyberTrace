"""
CyberTrace Viva PPT — rebuilt from secondppt.pptx visual style.
Tone: "proposed / future system" — NOT "we built this"
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

# ── Palette (from secondppt exactly) ─────────────────────────────────
DARK_RED   = RGBColor(0xB9, 0x1C, 0x1C)   # B91C1C – headings
ORANGE     = RGBColor(0xEA, 0x58, 0x0C)   # EA580C – section labels / accents
CARD_A     = RGBColor(0xFD, 0xF3, 0xDC)   # FDF3DC – warm cream card
CARD_B     = RGBColor(0xFF, 0xF7, 0xED)   # FFF7ED – lighter cream card
BLACK      = RGBColor(0x1C, 0x19, 0x17)   # 1C1917 – body text
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

# slide dimensions
W = Inches(13.33)
H = Inches(7.50)

# ── Helpers ───────────────────────────────────────────────────────────
def set_bg(slide, rgb):
    fill = slide.background.fill; fill.solid(); fill.fore_color.rgb = rgb

def rrect(slide, l, t, w, h, fill=None, radius=Inches(0.12), line_rgb=None, line_pt=0):
    """Rounded rectangle shape."""
    sp = slide.shapes.add_shape(5, l, t, w, h)   # 5 = ROUNDED_RECTANGLE
    sp.adjustments[0] = 0.05          # corner rounding
    if fill:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    else:
        sp.fill.background()
    if line_rgb:
        sp.line.color.rgb = line_rgb; sp.line.width = Pt(line_pt)
    else:
        sp.line.fill.background(); sp.line.width = Pt(0)
    return sp

def rect(slide, l, t, w, h, fill=None, line_rgb=None, line_pt=0):
    sp = slide.shapes.add_shape(1, l, t, w, h)
    if fill:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    else:
        sp.fill.background()
    if line_rgb:
        sp.line.color.rgb = line_rgb; sp.line.width = Pt(line_pt)
    else:
        sp.line.fill.background(); sp.line.width = Pt(0)
    return sp

def tb(slide, l, t, w, h, text, size, bold=False, color=None,
       align=PP_ALIGN.LEFT, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run()
    r.text = text; r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    if color: r.font.color.rgb = color
    return box

def clear(slide):
    tree = slide.shapes._spTree
    for sp in list(tree):
        if sp.tag.split('}')[-1] in ('sp','pic','cxnSp','graphicFrame','grpSp'):
            tree.remove(sp)

def content_header(slide, section_no, section_label, title):
    """Matches secondppt header style exactly."""
    tb(slide, Inches(0.67), Inches(0.50), Inches(12.67), Inches(0.22),
       f"Section {section_no}  •  {section_label}", 11, bold=True, color=ORANGE)
    tb(slide, Inches(0.67), Inches(0.72), Inches(12.67), Inches(0.56),
       title, 27, bold=True, color=DARK_RED)
    rect(slide, Inches(0.67), Inches(1.28), Inches(12.0), Inches(0.03), fill=ORANGE)

# ── BUILD ─────────────────────────────────────────────────────────────
def build(template, output):
    prs = Presentation(template)
    sls  = prs.slides

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 1 – Title / Cover
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[0]; clear(sl); set_bg(sl, WHITE)

    # Top header band
    rect(sl, 0, 0, W, Inches(1.52), fill=DARK_RED)
    tb(sl, Inches(0.55), Inches(0.12), Inches(12.23), Inches(0.62),
       "Indore Institute of Science & Technology",
       22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(sl, Inches(0.55), Inches(0.74), Inches(12.23), Inches(0.36),
       "Department of Information Technology",
       14, color=CARD_A, align=PP_ALIGN.CENTER)

    # "A Minor Project" label
    tb(sl, Inches(1.0), Inches(1.7), Inches(11.3), Inches(0.4),
       "A Minor Project Presentation on",
       13, color=ORANGE, align=PP_ALIGN.CENTER)

    # Project title card (rounded)
    rrect(sl, Inches(1.5), Inches(2.2), Inches(10.35), Inches(1.75), fill=CARD_A)
    tb(sl, Inches(1.65), Inches(2.32), Inches(10.05), Inches(0.65),
       "CYBERTRACE", 34, bold=True, color=DARK_RED, align=PP_ALIGN.CENTER)
    tb(sl, Inches(1.65), Inches(3.0), Inches(10.05), Inches(0.82),
       "Real-Time Network Security Monitoring & Anomaly Detection System",
       16, color=BLACK, align=PP_ALIGN.CENTER)

    # Orange thin divider
    rect(sl, Inches(1.5), Inches(4.12), Inches(10.35), Inches(0.03), fill=ORANGE)

    # Guided by
    tb(sl, Inches(1.1), Inches(4.28), Inches(4.6), Inches(0.38),
       "Project Guide", 13, bold=True, color=ORANGE)
    tb(sl, Inches(1.1), Inches(4.68), Inches(4.6), Inches(0.6),
       "Ms. Rupal Yadav\nDepartment of Information Technology", 12, color=BLACK)

    # Presented by (3 students)
    tb(sl, Inches(7.2), Inches(4.28), Inches(5.5), Inches(0.38),
       "Presented By", 13, bold=True, color=ORANGE)
    tb(sl, Inches(7.2), Inches(4.68), Inches(5.5), Inches(1.1),
       "Priyanshi Gupta        0818IT241053\nPalak Yadav              0818IT241047\nVishwajeet Singh Tomar  0818IT241075",
       12, color=BLACK)

    # Year
    tb(sl, Inches(3.5), Inches(5.9), Inches(6.35), Inches(0.4),
       "Academic Year: 2024 – 2025", 12, color=BLACK, align=PP_ALIGN.CENTER)

    # Footer line
    rect(sl, 0, H - Inches(0.35), W, Inches(0.35), fill=CARD_A)
    tb(sl, Inches(0.5), H - Inches(0.32), Inches(12.3), Inches(0.28),
       "Indore Institute of Science & Technology  |  Minor Project – 2024-25",
       10, color=ORANGE, align=PP_ALIGN.CENTER)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 2 – Outline
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[1]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "00", "Table of Contents", "Outline")

    topics = [
        ("01", "Proposed Area and Topic", "Domain focus and project title."),
        ("02", "Introduction",            "Overview of the CyberTrace platform."),
        ("03", "Objectives",              "Five primary goals of the project."),
        ("04", "Proposed Methodology",    "System architecture and data flow."),
        ("05", "Technical Details",       "Minimum hardware and software stack."),
        ("06", "Expected Outcome",        "Project deliverables and impact."),
        ("07", "References",              "Standard papers and documentation."),
    ]
    cols_x = [Inches(1.34), Inches(7.55)]
    base_y = Inches(1.55)
    gap    = Inches(0.76)

    for idx, (num, title, desc) in enumerate(topics):
        cx = cols_x[idx % 2]
        cy = base_y + (idx // 2) * gap
        # bullet dot
        tb(sl, cx, cy + Inches(0.06), Inches(0.08), Inches(0.28),
           "•", 18, color=BLACK)
        tb(sl, cx + Inches(0.09), cy, Inches(4.67), Inches(0.56),
           f"{num}. {title}: ", 18, bold=True, color=BLACK)
        # inline desc (second run not easily done in a textbox, so separate)
        tb(sl, cx + Inches(0.09) + Inches(len(f'{num}. {title}: ') * 0.11),
           cy, Inches(4.67 - len(f'{num}. {title}: ') * 0.11), Inches(0.56),
           desc, 18, color=BLACK)

    # Rebuild with clean inline style
    # clear bullets and redo properly
    # Actually let's keep it clean: title bold, desc on same line, separate textbox
    for idx, (num, title, desc) in enumerate(topics):
        cx = cols_x[idx % 2]
        cy = base_y + (idx // 2) * gap
        # We need a multi-run paragraph. Use a single textbox with two runs.
        box = slide.shapes.add_textbox(cx + Inches(0.09), cy, Inches(4.67), Inches(0.56)) \
            if False else sl.shapes.add_textbox(cx + Inches(0.09), cy, Inches(4.67), Inches(0.56))
        tf = box.text_frame; tf.word_wrap = True
        p  = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = f"{num}. {title}: "; r1.font.size = Pt(18); r1.font.bold = True; r1.font.color.rgb = BLACK
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(18); r2.font.bold = False; r2.font.color.rgb = BLACK

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 3 – Proposed Area & Topic
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[2]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "01", "Font Style: Times New Roman", "Proposed Area and Topic")

    # Left rounded card – Area
    rrect(sl, Inches(0.67), Inches(1.55), Inches(5.79), Inches(3.62), fill=CARD_A)
    tb(sl, Inches(0.97), Inches(1.85), Inches(5.3), Inches(0.36),
       "Proposed Area & Motivation", 18, bold=True, color=DARK_RED)
    bullets_area = [
        ("Cybersecurity Domain:", "Network traffic inspection and analysis."),
        ("Intrusion Detection:", "Automated, rule-based threat identification."),
        ("Packet Monitoring:", "Real-time and historical stream analysis."),
        ("Cost Efficiency:", "Open-source alternative to costly enterprise tools."),
    ]
    for i, (bold_text, rest) in enumerate(bullets_area):
        by = Inches(2.32) + i * Inches(0.54)
        tb(sl, Inches(1.15), by - Inches(0.02), Inches(0.07), Inches(0.28),
           "•", 15, color=BLACK)
        box = sl.shapes.add_textbox(Inches(1.22), by, Inches(5.11), Inches(0.5))
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = bold_text + " "; r1.font.size = Pt(15); r1.font.bold = True; r1.font.color.rgb = BLACK
        r2 = p.add_run(); r2.text = rest; r2.font.size = Pt(15); r2.font.bold = False; r2.font.color.rgb = BLACK

    # Left bottom card – Topic
    rrect(sl, Inches(0.67), Inches(5.32), Inches(5.79), Inches(1.68), fill=CARD_B)
    tb(sl, Inches(0.97), Inches(5.55), Inches(5.3), Inches(0.32),
       "Proposed Project Topic", 16, bold=True, color=ORANGE)
    tb(sl, Inches(0.97), Inches(5.9), Inches(5.2), Inches(0.85),
       "CyberTrace: Real-Time Network Security Monitoring & Anomaly Detection System using Python, FastAPI, and React.", 15, bold=True, color=BLACK)

    # Right — image placeholder with context text
    rrect(sl, Inches(6.70), Inches(1.55), Inches(6.0), Inches(5.45), fill=CARD_B)
    tb(sl, Inches(6.95), Inches(1.75), Inches(5.55), Inches(0.38),
       "Why This Project?", 16, bold=True, color=DARK_RED)
    whys = [
        "Global cybercrime damage is projected to reach $10.5 trillion annually by 2025.",
        "Most existing IDS tools are expensive and require deep expertise to operate.",
        "Institutions and small teams lack accessible, real-time threat visibility tools.",
        "CyberTrace will provide a lightweight, open-source dashboard that any IT team can deploy.",
        "It will bridge the gap between raw packet data and actionable security insights.",
    ]
    for i, w in enumerate(whys):
        tb(sl, Inches(6.95), Inches(2.28) + i * Inches(0.82), Inches(5.55), Inches(0.72),
           f"→  {w}", 13, color=BLACK)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 4 – Introduction
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[3]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "02", "Brief Introduction of Project", "Introduction")

    # Quote banner
    rrect(sl, Inches(0.67), Inches(1.55), Inches(12.0), Inches(1.02), fill=CARD_A)
    tb(sl, Inches(0.0), Inches(1.7), W, Inches(0.72),
       ' "CyberTrace will bridge raw network data and actionable security intelligence — in real time." ',
       19, bold=True, color=DARK_RED, align=PP_ALIGN.CENTER, italic=True)

    tb(sl, Inches(0.67), Inches(2.75), Inches(12.0), Inches(0.55),
       "The proposed system aims to monitor network activity continuously, identify threats automatically, "
       "and present findings through an intuitive web-based dashboard — without requiring expensive enterprise solutions.",
       14, color=BLACK)

    # Three cards
    card_data = [
        ("What It Will Do",   DARK_RED, CARD_A,
         "Capture and parse network packets (live or from PCAP files) and run them through multiple anomaly detection engines to flag threats in real time."),
        ("How It Will Work",  ORANGE,   CARD_B,
         "A Scapy-based capture layer will feed a FastAPI backend that processes packets, stores alerts, and serves data via REST and WebSocket to a React dashboard."),
        ("Why It Matters",    DARK_RED, CARD_A,
         "Early automated threat detection reduces incident response time. The system will be deployable by small teams without enterprise-level licensing or infrastructure costs."),
    ]
    cw = Inches(3.81)
    for (title, tc, bg, body), cx in zip(card_data, [Inches(0.67), Inches(4.76), Inches(8.86)]):
        rrect(sl, cx, Inches(3.48), cw, Inches(3.28), fill=bg)
        tb(sl, cx + Inches(0.29), Inches(3.72), cw - Inches(0.38), Inches(0.38),
           title, 18, bold=True, color=tc)
        tb(sl, cx + Inches(0.18), Inches(4.14), cw - Inches(0.3), Inches(2.42),
           body, 14, color=BLACK)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 5 – Objectives
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[4]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "03", "Goals of the Project", "Objectives")

    objectives = [
        ("01", "Packet Capture",    CARD_A,
         "Develop a module to capture live traffic from a network interface and parse recorded PCAP files using the Scapy library."),
        ("02", "Anomaly Detection", CARD_B,
         "Implement rule-based and ML-threshold detectors for DoS attacks, Port Scans, and DNS anomalies to generate real-time alerts."),
        ("03", "Web Dashboard",     CARD_A,
         "Design a responsive, browser-based UI using React JS to display live packet metrics, protocol charts, and active threat alerts."),
        ("04", "PCAP Forensics",    CARD_B,
         "Build an upload module allowing investigators to submit stored .pcap files for offline threat analysis and report generation."),
        ("05", "Decoupled Design",  CARD_A,
         "Architect the system as a modular FastAPI backend paired with a React frontend, enabling independent scaling of each layer."),
    ]
    oh = Inches(0.84)
    for i, (num, title, bg, desc) in enumerate(objectives):
        y = Inches(1.52) + i * (oh + Inches(0.04))
        rrect(sl, Inches(0.67), y, Inches(12.0), oh, fill=bg)
        tb(sl, Inches(0.82), y + Inches(0.18), Inches(0.55), Inches(0.5),
           num, 22, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
        box = sl.shapes.add_textbox(Inches(1.5), y + Inches(0.16), Inches(10.98), Inches(0.55))
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = title + ":  "; r1.font.size = Pt(18); r1.font.bold = True; r1.font.color.rgb = BLACK
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(14); r2.font.bold = False; r2.font.color.rgb = BLACK

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 6 – Methodology: Architecture
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[5]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "04", "Proposed Algorithm / Method", "Proposed Methodology: Architecture")

    layers = [
        ("LAYER 1", "Data Capture Layer",
         "The system will use Scapy to sniff live packets from a NIC or read uploaded PCAP files through a PCAPReader module.",
         CARD_A, DARK_RED),
        ("LAYER 2", "Detection Engine",
         "Each parsed packet will pass through four detector modules: DoSDetector, PortScanDetector, DNSAnomalyDetector, and MLAnomalyDetector.",
         CARD_B, ORANGE),
        ("LAYER 3", "Backend API",
         "FastAPI will expose REST endpoints (/api/metrics, /api/alerts, /api/upload_pcap) and a WebSocket channel for live streaming.",
         CARD_A, DARK_RED),
        ("LAYER 4", "Frontend UI",
         "A React + Vite application will render an interactive dashboard featuring live charts, an alert panel, and a PCAP upload interface.",
         CARD_B, ORANGE),
    ]
    cw = Inches(2.59)
    for i, (lbl, title, desc, bg, tc) in enumerate(layers):
        cx = Inches(0.67) + i * (cw + Inches(0.47))
        rrect(sl, cx, Inches(1.52), cw, Inches(5.6), fill=bg)
        tb(sl, cx + Inches(0.18), Inches(1.72), cw - Inches(0.24), Inches(0.38),
           lbl, 14, bold=True, color=tc, align=PP_ALIGN.CENTER)
        tb(sl, cx + Inches(0.18), Inches(2.16), cw - Inches(0.24), Inches(0.46),
           title, 16, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        # Arrow between layers
        if i < 3:
            tb(sl, cx + cw + Inches(0.08), Inches(4.0), Inches(0.38), Inches(0.38),
               "→", 22, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
        tb(sl, cx + Inches(0.15), Inches(2.75), cw - Inches(0.24), Inches(4.1),
           desc, 14, color=BLACK)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 7 – Methodology: Flow Chart (text-based)
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[6]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "04", "Process of the Whole Project", "Proposed Methodology: Flow Chart")

    steps = [
        ("START",            "System initialises and selects capture source (Live NIC or PCAP file).",             DARK_RED),
        ("CAPTURE",          "Scapy captures or reads packets and sends them to the Packet Parser.",               ORANGE),
        ("PARSE",            "Parser extracts: Source/Dest IP, Port, Protocol, Payload size, Timestamp.",         DARK_RED),
        ("DETECT",           "Four engines run in parallel: DoS, PortScan, DNSAnomaly, MLThreshold.",             ORANGE),
        ("ALERT / STORE",    "Flagged packets generate alerts stored in SQLite via SQLAlchemy ORM.",               DARK_RED),
        ("SERVE",            "FastAPI serves metrics and alerts via REST + WebSocket to the React frontend.",      ORANGE),
        ("DASHBOARD",        "React dashboard renders live charts, an alert feed, and forensics upload UI.",       DARK_RED),
    ]
    bw = Inches(1.55); bh = Inches(0.74); gap_x = Inches(0.22)
    base_x = Inches(0.42); base_y = Inches(1.52)

    for i, (label, detail, tc) in enumerate(steps):
        cx = base_x + i * (bw + gap_x)
        rrect(sl, cx, base_y, bw, bh, fill=CARD_A if i % 2 == 0 else CARD_B)
        tb(sl, cx + Inches(0.08), base_y + Inches(0.08), bw - Inches(0.14), Inches(0.38),
           label, 12, bold=True, color=tc, align=PP_ALIGN.CENTER)
        if i < len(steps) - 1:
            tb(sl, cx + bw, base_y + Inches(0.22), gap_x, Inches(0.32),
               "→", 16, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

    # Detail boxes below
    detail_y = Inches(2.52)
    for i, (label, detail, tc) in enumerate(steps):
        cx = base_x + i * (bw + gap_x)
        rrect(sl, cx, detail_y, bw, Inches(4.48), fill=CARD_B if i % 2 == 0 else CARD_A)
        tb(sl, cx + Inches(0.1), detail_y + Inches(0.12), bw - Inches(0.18), Inches(4.2),
           detail, 12, color=BLACK)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 8 – Technical Details
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[7]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "05", "Hardware and Software Requirement (MIN)", "Technical Details")

    # Hardware card
    rrect(sl, Inches(0.67), Inches(1.52), Inches(5.79), Inches(5.45), fill=CARD_A)
    tb(sl, Inches(0.97), Inches(1.78), Inches(5.3), Inches(0.38),
       "Hardware Requirements (MIN)", 18, bold=True, color=DARK_RED)
    hw = [
        ("System Type:", "Standard PC or Laptop."),
        ("Memory (RAM):", "Minimum 4 GB (8 GB Recommended)."),
        ("Processor:", "Intel Core i3+ or AMD Ryzen 3+."),
        ("Network Card:", "Standard NIC for live packet capture."),
        ("Disk Space:", "Minimum 500 MB free storage."),
    ]
    for i, (key, val) in enumerate(hw):
        by = Inches(2.28) + i * Inches(0.72)
        tb(sl, Inches(0.85), by - Inches(0.02), Inches(0.07), Inches(0.28), "•", 15, color=BLACK)
        box = sl.shapes.add_textbox(Inches(0.97), by, Inches(5.25), Inches(0.58))
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = key + " "; r1.font.size = Pt(15); r1.font.bold = True; r1.font.color.rgb = BLACK
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(15); r2.font.bold = False; r2.font.color.rgb = BLACK

    # Software card
    rrect(sl, Inches(6.88), Inches(1.52), Inches(5.79), Inches(5.45), fill=CARD_B)
    tb(sl, Inches(7.18), Inches(1.78), Inches(5.3), Inches(0.38),
       "Software Requirements & Tech Stack", 18, bold=True, color=DARK_RED)
    sw = [
        ("Languages:", "Python 3.x and JavaScript (ES2022)."),
        ("Packet Capture:", "Scapy – sniffing and PCAP parsing."),
        ("Backend & DB:", "FastAPI, Uvicorn, SQLite, SQLAlchemy."),
        ("Frontend UI:", "React JS, Vite, TailwindCSS, Recharts."),
        ("OS Support:", "Linux (Recommended) and Windows."),
    ]
    for i, (key, val) in enumerate(sw):
        by = Inches(2.28) + i * Inches(0.72)
        tb(sl, Inches(7.05), by - Inches(0.02), Inches(0.07), Inches(0.28), "•", 15, color=BLACK)
        box = sl.shapes.add_textbox(Inches(7.18), by, Inches(5.28), Inches(0.58))
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run(); r1.text = key + " "; r1.font.size = Pt(15); r1.font.bold = True; r1.font.color.rgb = BLACK
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(15); r2.font.bold = False; r2.font.color.rgb = BLACK

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 9 – Expected Outcome
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[8]; clear(sl); set_bg(sl, WHITE)
    content_header(sl, "06", "Summary of the Project", "Expected Outcome")

    outcomes = [
        ("1. Functional Prototype",
         CARD_A, DARK_RED,
         "A working prototype capable of capturing live packets or reading PCAP files, detecting anomalies, and generating real-time security alerts through automated rule engines.",
         CARD_B, ORANGE,
         "2. Interactive Web Dashboard",
         "A browser-based React dashboard displaying live traffic metrics, protocol distribution charts, and a threat alert feed — accessible from any device on the network."),
        ("3. PCAP Forensics Module",
         CARD_A, DARK_RED,
         "A dedicated forensics page allowing investigators to upload recorded .pcap files for offline analysis and downloadable incident reports for post-event investigation.",
         CARD_B, ORANGE,
         "4. Scalable & Decoupled Architecture",
         "A cleanly separated FastAPI backend and React frontend ensuring each layer can be independently maintained, scaled, or upgraded without disrupting the other."),
    ]

    for row_idx, (t1, bg1, tc1, d1, bg2, tc2, t2, d2) in enumerate(outcomes):
        base_y2 = Inches(1.52) + row_idx * Inches(2.82)
        for j, (t, bg, tc, d) in enumerate([(t1,bg1,tc1,d1),(t2,bg2,tc2,d2)]):
            cx = Inches(0.67) if j == 0 else Inches(6.79)
            rrect(sl, cx, base_y2, Inches(5.88), Inches(2.55), fill=bg)
            tb(sl, cx + Inches(0.24), base_y2 + Inches(0.2), Inches(5.35), Inches(0.42),
               t, 17, bold=True, color=tc)
            tb(sl, cx + Inches(0.24), base_y2 + Inches(0.7), Inches(5.35), Inches(1.7),
               d, 13, color=BLACK)

    # ═══════════════════════════════════════════════════════════════════
    # SLIDE 10 – References + Thank You
    # ═══════════════════════════════════════════════════════════════════
    sl = sls[9]; clear(sl); set_bg(sl, WHITE)

    tb(sl, Inches(0.67), Inches(0.35), Inches(12.67), Inches(0.22),
       "Section 07  •  Citations & Documentation", 11, bold=True, color=ORANGE)
    tb(sl, Inches(0.67), Inches(0.57), Inches(12.67), Inches(0.55),
       "References", 27, bold=True, color=DARK_RED)
    rect(sl, Inches(0.67), Inches(1.1), Inches(12.0), Inches(0.03), fill=ORANGE)

    refs = [
        "[1] RFC 793: Transmission Control Protocol (TCP), IETF, 1981.",
        "[2] Scapy Documentation: Packet Manipulation Library — https://scapy.net",
        "[3] FastAPI Documentation: High Performance APIs with Python — https://fastapi.tiangolo.com",
        "[4] React JS Documentation: JavaScript Library for Building UIs — https://react.dev",
        '[5] V. Chandola et al.: "Anomaly Detection: A Survey", ACM Computing Surveys, 2009.',
        "[6] UI Component Library: TailwindCSS & DaisyUI — https://daisyui.com",
    ]
    rrect(sl, Inches(0.67), Inches(1.25), Inches(12.0), Inches(3.85), fill=CARD_A)
    for i, ref in enumerate(refs):
        tb(sl, Inches(0.95), Inches(1.45) + i * Inches(0.56), Inches(11.5), Inches(0.5),
           ref, 14, color=BLACK)

    tb(sl, 0, Inches(5.4), W, Inches(0.65),
       "Thank You!", 40, bold=True, color=DARK_RED, align=PP_ALIGN.CENTER)
    tb(sl, 0, Inches(6.1), W, Inches(0.38),
       "We look forward to your guidance and feedback.", 15, color=BLACK,
       align=PP_ALIGN.CENTER, italic=True)

    prs.save(output)
    print(f"✅  Saved → {output}")


if __name__ == "__main__":
    build(
        "/home/pinkparrot/Priyanshi Gupta/secondppt.pptx",
        "/home/pinkparrot/Priyanshi Gupta/CyberTrace/ct_viva.pptx"
    )
