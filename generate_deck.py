import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="VISION_X_Evolution_Tracker_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    TEXT_LIGHT = RGBColor(203, 213, 225) # Slate 300
    
    ACCENT_SKY = RGBColor(56, 189, 248)    # Sky 400
    ACCENT_INDIGO = RGBColor(129, 140, 248)# Indigo 400
    COLOR_GREEN = RGBColor(52, 211, 153)   # Emerald 400
    COLOR_AMBER = RGBColor(251, 191, 36)   # Amber 400
    COLOR_RED = RGBColor(248, 113, 113)    # Red 400
    COLOR_PURPLE = RGBColor(192, 132, 252) # Purple 400

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="HACKATHON SHOWCASE | TEAM VISION X"):
        # Category / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_SKY

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title="", border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Accent decorative glow bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_SKY
    bar.line.fill.background()

    # Event badge
    badge = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.5), Inches(0.4))
    b_p = badge.text_frame.paragraphs[0]
    b_p.text = "COLLEGE HACKATHON 2026  •  AUTOMATED FACT-CHECKING & MISINFORMATION"
    b_p.font.size = Pt(13)
    b_p.font.bold = True
    b_p.font.color.rgb = ACCENT_INDIGO

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.5), Inches(1.3))
    tp = title_box.text_frame.paragraphs[0]
    tp.text = "EVOLUTION TRACKER 2.0"
    tp.font.size = Pt(46)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_WHITE

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.5), Inches(10.5), Inches(0.7))
    sp = sub_box.text_frame.paragraphs[0]
    sp.text = "Investigating How Information Changes, What Was Altered, and When it Became Misleading"
    sp.font.size = Pt(18)
    sp.font.color.rgb = TEXT_LIGHT

    # Tagline card
    tag_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(5.8), Inches(0.7))
    tag_card.fill.solid()
    tag_card.fill.fore_color.rgb = CARD_BG
    tag_card.line.color.rgb = ACCENT_SKY
    tag_p = tag_card.text_frame.paragraphs[0]
    tag_p.text = "OUR TAGLINE:  VERIFY BEFORE YOU SHARE"
    tag_p.font.size = Pt(14)
    tag_p.font.bold = True
    tag_p.font.color.rgb = COLOR_GREEN

    # Team & Credits box
    cred_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(10.5), Inches(0.8))
    cp = cred_box.text_frame.paragraphs[0]
    cp.text = "Developed by TEAM VISION X  |  Full-Stack & Applied AI Architecture"
    cp.font.size = Pt(14)
    cp.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 2: THE PROBLEM (WHY EXISTING TOOLS FAIL)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Core Problem: Beyond Static True/False", "THE MISINFORMATION PARADOX")

    # 3 Columns
    col_w = Inches(3.64)
    gap = Inches(0.39)
    top_pos = Inches(1.8)
    h_pos = Inches(4.9)

    # Card 1: Traditional Fact Checkers
    add_card(s2, Inches(0.8), top_pos, col_w, h_pos, "Traditional Fact-Checking")
    tb1 = s2.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.7), col_w - Inches(0.5), h_pos - Inches(0.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0
    bullets1 = [
        ("Binary Verdicts:", "Forces complex realities into oversimplified True or False verdicts."),
        ("Static Snapshot:", "Inspects claims in isolation without historical context or propagation trajectory."),
        ("Ignores Context:", "Fails to explain where and when a true fact transitioned into a misleading rumour."),
        ("Reactive, Not Diagnostic:", "Tells users what to think, but not how the claim mutated.")
    ]
    for b_title, b_desc in bullets1:
        p = tf1.add_paragraph() if tf1.paragraphs[0].text else tf1.paragraphs[0]
        p.space_after = Pt(14)
        run_t = p.add_run()
        run_t.text = f"• {b_title} "
        run_t.font.bold = True
        run_t.font.size = Pt(13)
        run_t.font.color.rgb = COLOR_RED
        run_d = p.add_run()
        run_d.text = b_desc
        run_d.font.size = Pt(12)
        run_d.font.color.rgb = TEXT_LIGHT

    # Card 2: The Real-World Reality
    add_card(s2, Inches(0.8) + col_w + gap, top_pos, col_w, h_pos, "How Misinformation Spreads")
    tb2 = s2.shapes.add_textbox(Inches(1.05) + col_w + gap, top_pos + Inches(0.7), col_w - Inches(0.5), h_pos - Inches(0.9))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    bullets2 = [
        ("Starts with Truth:", "Misinformation rarely starts 100% false; it originates from a real local event."),
        ("Dropped Caveats:", "Crucial conditions (e.g. 'only school #1' or 'in lab mice') are discarded."),
        ("Scope Inflation:", "Words like 'some' mutate into 'all', 'one school' becomes 'statewide shutdown'."),
        ("Viral Escalation:", "Sensationalised headlines trigger panic before fact-checkers even react.")
    ]
    for b_title, b_desc in bullets2:
        p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
        p.space_after = Pt(14)
        run_t = p.add_run()
        run_t.text = f"• {b_title} "
        run_t.font.bold = True
        run_t.font.size = Pt(13)
        run_t.font.color.rgb = COLOR_AMBER
        run_d = p.add_run()
        run_d.text = b_desc
        run_d.font.size = Pt(12)
        run_d.font.color.rgb = TEXT_LIGHT

    # Card 3: Evolution Tracker Paradigm
    add_card(s2, Inches(0.8) + (col_w + gap) * 2, top_pos, col_w, h_pos, "The Evolution Tracker Mission", ACCENT_SKY)
    tb3 = s2.shapes.add_textbox(Inches(1.05) + (col_w + gap) * 2, top_pos + Inches(0.7), col_w - Inches(0.5), h_pos - Inches(0.9))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
    bullets3 = [
        ("The Journey of Info:", "Investigates: 'How did a statement change, and when did it become misleading?'"),
        ("Genomic Fingerprinting:", "Extracts Rumour DNA to cluster related claims across differing wording."),
        ("Mutation Detection:", "Color-coded diff engine exposing added, removed, and inflated facts."),
        ("Verified Evidence:", "Multi-source web consensus with grounded Google Gemini interpretation.")
    ]
    for b_title, b_desc in bullets3:
        p = tf3.add_paragraph() if tf3.paragraphs[0].text else tf3.paragraphs[0]
        p.space_after = Pt(14)
        run_t = p.add_run()
        run_t.text = f"• {b_title} "
        run_t.font.bold = True
        run_t.font.size = Pt(13)
        run_t.font.color.rgb = COLOR_GREEN
        run_d = p.add_run()
        run_d.text = b_desc
        run_d.font.size = Pt(12)
        run_d.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 3: 4 SIGNATURE PILLARS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Four Signature Innovations of Evolution Tracker", "PRODUCT DIFFERENTIATION")

    grid_w = Inches(5.6)
    grid_h = Inches(2.35)
    row_gap = Inches(0.35)
    col_gap = Inches(0.5)

    pillars = [
        ("FEATURE A — RUMOUR DNA", "Genomic Fingerprinting of Claims", 
         "Extracts entities, quantities, dates, subject, assertion scope, and core factual properties. Forms visual claim families linking related statements even when exact wording changes.",
         ACCENT_SKY, Inches(0.8), Inches(1.8)),
        
        ("FEATURE B — MUTATION DETECTOR", "Granular Evolutionary Diff Engine", 
         "Compares two claim versions using color-coded text diffs. Detects added facts, removed conditions, altered dates, and scope inflation with clear non-accusatory explanations.",
         COLOR_AMBER, Inches(0.8) + grid_w + col_gap, Inches(1.8)),
        
        ("FEATURE C — RUMOUR JOURNEY MAP", "Interactive Contagion Timeline", 
         "Maps claim progression from origin to viral escalation. Visualizes mutation triggers, confidence degradation, and provenance tagging (observed vs user forwarded).",
         COLOR_PURPLE, Inches(0.8), Inches(1.8) + grid_h + row_gap),
        
        ("FEATURE D — EVIDENCE & VERDICT ENGINE", "Multi-Source Grounded Verification", 
         "Integrates live web search (Tavily) + Google Gemini AI with transparent rule-based fallback. Delivers 4 official verdict categories and calibrated 3-tier confidence.",
         COLOR_GREEN, Inches(0.8) + grid_w + col_gap, Inches(1.8) + grid_h + row_gap)
    ]

    for p_tag, p_head, p_body, p_color, p_x, p_y in pillars:
        add_card(s3, p_x, p_y, grid_w, grid_h, "", p_color)
        tb = s3.shapes.add_textbox(p_x + Inches(0.25), p_y + Inches(0.2), grid_w - Inches(0.5), grid_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = p_tag
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = p_color
        
        p2 = tf.add_paragraph()
        p2.text = p_head
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(6)
        
        p3 = tf.add_paragraph()
        p3.text = p_body
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 4: FEATURE A — RUMOUR DNA
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Feature A: Rumour DNA & Visual Claim Families", "CORE ARCHITECTURE")

    # Left card: DNA Dimensions
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "The Claim DNA Fingerprint")
    tb_dna = s4.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf_dna = tb_dna.text_frame
    tf_dna.word_wrap = True
    tf_dna.margin_left = tf_dna.margin_top = tf_dna.margin_right = tf_dna.margin_bottom = 0
    
    dna_dims = [
        ("Main Subject", "Identifies core topic (e.g. 'Oakridge High School', 'Curfew')."),
        ("Named Entities", "Extracts people, schools, government bodies, cities, nations."),
        ("Location & Geography", "Resolves geopolitical hierarchy from local campus to state/nation."),
        ("Dates & Time Horizons", "Captures explicit dates, relative deadlines, and durations."),
        ("Numbers & Statistics", "Tracks exact counts, monetary figures, and casualty numbers."),
        ("Scope of Statement", "Classifies reach: 'specific institution', 'district', or 'statewide'."),
        ("Factual Assertion", "Normalised canonical assertion for verifiable evidence comparison.")
    ]
    for d_name, d_desc in dna_dims:
        p = tf_dna.add_paragraph() if tf_dna.paragraphs[0].text else tf_dna.paragraphs[0]
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {d_name}: "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_SKY
        r2 = p.add_run()
        r2.text = d_desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # Right card: Visual Claim Family & Grouping
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Semantic Clustering & Family Graph")
    tb_fam = s4.shapes.add_textbox(Inches(7.05), Inches(2.5), Inches(5.2), Inches(4.0))
    tf_fam = tb_fam.text_frame
    tf_fam.word_wrap = True
    tf_fam.margin_left = tf_fam.margin_top = tf_fam.margin_right = tf_fam.margin_bottom = 0

    fam_points = [
        ("Multi-Layer Similarity Engine:", "Combines entity overlap, normalised tokens, and semantic embedding vectors."),
        ("Connects Related Rumours:", "Identifies claim variants even when vocabulary, phrasing, or languages differ completely."),
        ("Critical Safeguard (Anti-Assumption):", "The system NEVER assumes similar wording equals identical facts! It actively highlights divergence in numbers, dates, and scope."),
        ("Visual Claim Family Tree:", "Interactive network graph linking parent claims to mutated child versions, allowing users to see the entire cluster at a glance.")
    ]
    for f_head, f_body in fam_points:
        p = tf_fam.add_paragraph() if tf_fam.paragraphs[0].text else tf_fam.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"✔ {f_head}\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_GREEN
        r2 = p.add_run()
        r2.text = f_body
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 5: FEATURE B — MUTATION DETECTOR
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Feature B: Mutation Detector & Diff Engine", "GRANULAR EVOLUTION DETECTION")

    # Top description card
    top_c = add_card(s5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.1))
    top_tb = s5.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(11.2), Inches(0.8))
    top_tf = top_tb.text_frame
    top_tf.word_wrap = True
    top_tf.margin_left = top_tf.margin_top = top_tf.margin_right = top_tf.margin_bottom = 0
    top_p = top_tf.paragraphs[0]
    top_p.text = "How does information shift? The Mutation Detector compares sequential versions to isolate additions, deletions, and scope expansions. Explanations use neutral, objective language—recognizing legitimate corrections as well as malicious inflation."
    top_p.font.size = Pt(13)
    top_p.font.color.rgb = TEXT_LIGHT

    # 4 Color Coded Mutation Types
    box_w = Inches(2.7)
    box_gap = Inches(0.3)
    b_top = Inches(3.1)
    b_h = Inches(3.6)

    cards_data = [
        ("GREEN (+)", "Added Information", COLOR_GREEN, 
         "Identifies new factual assertions, secondary entities, or unverified claims appended to the original report."),
        
        ("RED (-)", "Removed Information", COLOR_RED, 
         "Detects missing caveats, dropped conditions, omitted dates, or deleted qualifying clauses (e.g. 'pending review')."),
        
        ("AMBER (!)", "Misleading Mutation", COLOR_AMBER, 
         "Flags scope inflation ('one school' -> 'all schools'), extreme quantifiers ('always', 'completely'), or shifted numbers."),
        
        ("BLUE (i)", "Contextual Mod", ACCENT_SKY, 
         "Recognizes grammar cleanups, updated timestamps, source attributions, or legitimate journalistic corrections.")
    ]

    for idx, (m_badge, m_title, m_col, m_body) in enumerate(cards_data):
        cx = Inches(0.8) + idx * (box_w + box_gap)
        add_card(s5, cx, b_top, box_w, b_h, "", m_col)
        
        tb = s5.shapes.add_textbox(cx + Inches(0.2), b_top + Inches(0.25), box_w - Inches(0.4), b_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = m_badge
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = m_col
        
        p2 = tf.add_paragraph()
        p2.text = m_title
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(10)
        
        p3 = tf.add_paragraph()
        p3.text = m_body
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 6: FEATURE C — RUMOUR JOURNEY MAP
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Feature C: Rumour Journey Map & Contagion Timeline", "TIMELINE INVESTIGATION")

    # Step-by-Step Flow Cards
    step_w = Inches(3.64)
    step_gap = Inches(0.39)
    step_top = Inches(1.8)
    step_h = Inches(4.1)

    steps = [
        ("STAGE 1: THE ORIGIN", "Local Factual Event", COLOR_GREEN,
         "“Oakridge High School closed for 2 days for pest fumigation.”",
         [
             ("Status:", "Verified / Factual"),
             ("Scope:", "Specific single campus"),
             ("Source:", "Direct school circular"),
             ("Confidence:", "High (95%)")
         ]),
        ("STAGE 2: THE MUTATION", "Scope & Duration Inflation", COLOR_AMBER,
         "“All schools in the district are closed for one month.”",
         [
             ("Status:", "Scope Altered (Amber)"),
             ("Scope:", "Entire district (Expanded)"),
             ("Mutation:", "Duration 2d -> 30d"),
             ("Condition:", "Fumigation reason stripped")
         ]),
        ("STAGE 3: VIRAL PANIC", "Statewide Emergency Hoax", COLOR_RED,
         "“Government declared statewide educational shutdown emergency!”",
         [
             ("Status:", "Contradicted / False"),
             ("Scope:", "Statewide emergency"),
             ("Severity:", "Panic inducing escalation"),
             ("Verdict:", "Likely False (Contradicted by Dept)")
         ])
    ]

    for idx, (s_tag, s_name, s_col, s_quote, s_meta) in enumerate(steps):
        sx = Inches(0.8) + idx * (step_w + step_gap)
        add_card(s6, sx, step_top, step_w, step_h, "", s_col)
        
        tb = s6.shapes.add_textbox(sx + Inches(0.25), step_top + Inches(0.2), step_w - Inches(0.5), step_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = s_tag
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = s_col
        
        p1 = tf.add_paragraph()
        p1.text = s_name
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(8)
        
        p_q = tf.add_paragraph()
        p_q.text = s_quote
        p_q.font.size = Pt(12)
        p_q.font.italic = True
        p_q.font.color.rgb = ACCENT_SKY
        p_q.space_after = Pt(12)
        
        for m_lbl, m_val in s_meta:
            pm = tf.add_paragraph()
            pm.space_after = Pt(4)
            r_l = pm.add_run()
            r_l.text = f"{m_lbl} "
            r_l.font.bold = True
            r_l.font.size = Pt(11)
            r_l.font.color.rgb = TEXT_MUTED
            r_v = pm.add_run()
            r_v.text = m_val
            r_v.font.size = Pt(11)
            r_v.font.color.rgb = TEXT_WHITE

    # Bottom Timeline Metadata Callout
    bot_c = add_card(s6, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.85), "", ACCENT_INDIGO)
    bot_tb = s6.shapes.add_textbox(Inches(1.05), Inches(6.25), Inches(11.2), Inches(0.6))
    bot_tf = bot_tb.text_frame
    bot_tf.word_wrap = True
    bot_tf.margin_left = bot_tf.margin_top = bot_tf.margin_right = bot_tf.margin_bottom = 0
    bot_p = bot_tf.paragraphs[0]
    bot_p.text = "PROVENANCE TAGGING: Every stage tracks timestamps, origin type (observed, forwarded, ai-inferred), and channel source—revealing exactly who introduced each distortion."
    bot_p.font.size = Pt(12)
    bot_p.font.bold = True
    bot_p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 7: GROUNDED EVIDENCE & AI INTERPRETATION
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Multi-Source Grounded Evidence & Gemini AI", "TRUTH VERIFICATION")

    # Left: Multi-source search & grounding
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "Live Evidence Retrieval")
    tb_ev = s7.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf_ev = tb_ev.text_frame
    tf_ev.word_wrap = True
    tf_ev.margin_left = tf_ev.margin_top = tf_ev.margin_right = tf_ev.margin_bottom = 0

    ev_bullets = [
        ("Tavily Live Web Search:", "Executes real-time searches querying accredited sources, wire services, and official portals."),
        ("Publisher Credibility Scoring:", "Dynamic 0–100 reliability weighting based on domain provenance (.gov, .edu, BBC, Reuters vs social forums)."),
        ("Strict Snippet Grounding:", "Evidence is explicitly labeled as 'Search Snippet'. System never pretends to have read paywalled full text."),
        ("Offline Fallback Corpus:", "Guarantees 100% demo functionality even without active internet or third-party search keys.")
    ]
    for e_h, e_b in ev_bullets:
        p = tf_ev.add_paragraph() if tf_ev.paragraphs[0].text else tf_ev.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"• {e_h}\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_SKY
        r2 = p.add_run()
        r2.text = e_b
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # Right: Google Gemini AI + Fallback
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Google Gemini 3.5 AI Integration", COLOR_PURPLE)
    tb_ai = s7.shapes.add_textbox(Inches(7.05), Inches(2.5), Inches(5.2), Inches(4.0))
    tf_ai = tb_ai.text_frame
    tf_ai.word_wrap = True
    tf_ai.margin_left = tf_ai.margin_top = tf_ai.margin_right = tf_ai.margin_bottom = 0

    ai_bullets = [
        ("Nuanced Semantic Parsing:", "Interprets complex scientific phrasing, qualifications, and domain terminology accurately."),
        ("Solves Heading/Inquiry Traps:", "Distinguishes between question titles ('Can the Sun rise in the west?') vs actual declarative facts."),
        ("Multi-Tier Model Resilience:", "Primary model `gemini-3.5-flash` with automatic fallback to `gemini-3.1-flash-lite` during quota/503 spikes."),
        ("Rule-Based Fallback Guarantee:", "If AI API times out (>12s) or key is absent, deterministic local NLP rules execute instantly without failing.")
    ]
    for a_h, a_b in ai_bullets:
        p = tf_ai.add_paragraph() if tf_ai.paragraphs[0].text else tf_ai.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"✔ {a_h}\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_PURPLE
        r2 = p.add_run()
        r2.text = a_b
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 8: CALIBRATED VERDICT & CONFIDENCE
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Calibrated Claim Verdict & Multi-Factor Confidence", "OBJECTIVE SCORING")

    # Left: 4 Verdict Categories
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "4 Official Verdict Categories")
    tb_v = s8.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    tf_v.margin_left = tf_v.margin_top = tf_v.margin_right = tf_v.margin_bottom = 0

    verdicts = [
        ("LIKELY TRUE", COLOR_GREEN, "Reliable, relevant evidence confirms core assertion with 0 unresolved contradictions."),
        ("LIKELY FALSE", COLOR_RED, "Reliable evidence refutes the assertion, identifies opposing facts, or debunks claim."),
        ("MIXED / PARTIALLY TRUE", COLOR_AMBER, "Certain elements verified, but key conditions altered, omitted, or unverified."),
        ("UNVERIFIED", TEXT_MUTED, "Available evidence is insufficient, purely contextual, off-topic, or inconclusive.")
    ]
    for v_name, v_col, v_desc in verdicts:
        p = tf_v.add_paragraph() if tf_v.paragraphs[0].text else tf_v.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"[{v_name}]\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = v_col
        r2 = p.add_run()
        r2.text = v_desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # Right: Calibrated Confidence Model
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Multi-Signal Confidence Engine", ACCENT_SKY)
    tb_c = s8.shapes.add_textbox(Inches(7.05), Inches(2.5), Inches(5.2), Inches(4.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    conf_bullets = [
        ("Independent Agreement (Not Averages):", "Never calculates confidence by naively averaging source scores. Demands multiple independent root domains."),
        ("Syndication Deduplication:", "Treats 5 syndicated copies of the same wire article as ONE source, preventing artificial confidence inflation."),
        ("Relevance & Stance Strength:", "Measures direct semantic alignment with the factual assertion, filtering out mere topical mentions."),
        ("Calibrated Levels: HIGH / MEDIUM / LOW", "Provides a transparent percentage score only when mathematical consensus criteria are satisfied.")
    ]
    for c_h, c_b in conf_bullets:
        p = tf_c.add_paragraph() if tf_c.paragraphs[0].text else tf_c.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"• {c_h}\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_SKY
        r2 = p.add_run()
        r2.text = c_b
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 9: FULL-STACK TECHNICAL ARCHITECTURE
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Full-Stack System Architecture & Engineering", "TECHNICAL IMPLEMENTATION")

    stack_w = Inches(3.64)
    stack_gap = Inches(0.39)
    stack_top = Inches(1.8)
    stack_h = Inches(4.9)

    # Col 1: Frontend
    add_card(s9, Inches(0.8), stack_top, stack_w, stack_h, "Frontend Client", ACCENT_SKY)
    tb_fe = s9.shapes.add_textbox(Inches(1.05), stack_top + Inches(0.7), stack_w - Inches(0.5), stack_h - Inches(0.9))
    tf_fe = tb_fe.text_frame
    tf_fe.word_wrap = True
    tf_fe.margin_left = tf_fe.margin_top = tf_fe.margin_right = tf_fe.margin_bottom = 0
    fe_items = [
        ("Framework:", "React 18 + Vite (fast HMR, production build)"),
        ("Styling:", "Tailwind CSS with high-contrast slate design system"),
        ("Visualization:", "Interactive Journey Timelines, SVG gauges, Confetti"),
        ("Icons & UI:", "Lucide React, accessible semantic badges"),
        ("Testing:", "10 Vitest component & regression test suites passing")
    ]
    for f_k, f_v in fe_items:
        p = tf_fe.add_paragraph() if tf_fe.paragraphs[0].text else tf_fe.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"{f_k} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = ACCENT_SKY
        r2 = p.add_run()
        r2.text = f_v
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # Col 2: Backend
    add_card(s9, Inches(0.8) + stack_w + stack_gap, stack_top, stack_w, stack_h, "Backend Services", COLOR_GREEN)
    tb_be = s9.shapes.add_textbox(Inches(1.05) + stack_w + stack_gap, stack_top + Inches(0.7), stack_w - Inches(0.5), stack_h - Inches(0.9))
    tf_be = tb_be.text_frame
    tf_be.word_wrap = True
    tf_be.margin_left = tf_be.margin_top = tf_be.margin_right = tf_be.margin_bottom = 0
    be_items = [
        ("Framework:", "FastAPI (asynchronous REST API on Python 3.14)"),
        ("Database:", "Modular SQLite + SQLAlchemy ORM with auto-migrations"),
        ("Data Models:", "Strict Pydantic V2 schemas for DNA, Evidence, Mutations"),
        ("HTTP Engine:", "Asynchronous HTTPX client with connection pooling"),
        ("Testing:", "34 Pytest unit & integration tests passing (1.95s)")
    ]
    for b_k, b_v in be_items:
        p = tf_be.add_paragraph() if tf_be.paragraphs[0].text else tf_be.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"{b_k} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_GREEN
        r2 = p.add_run()
        r2.text = b_v
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # Col 3: AI & APIs
    add_card(s9, Inches(0.8) + (stack_w + stack_gap) * 2, stack_top, stack_w, stack_h, "AI & Live Services", COLOR_PURPLE)
    tb_ai_stack = s9.shapes.add_textbox(Inches(1.05) + (stack_w + stack_gap) * 2, stack_top + Inches(0.7), stack_w - Inches(0.5), stack_h - Inches(0.9))
    tf_ai_s = tb_ai_stack.text_frame
    tf_ai_s.word_wrap = True
    tf_ai_s.margin_left = tf_ai_s.margin_top = tf_ai_s.margin_right = tf_ai_s.margin_bottom = 0
    ai_items = [
        ("Search Engine:", "Tavily Search API (advanced search depth)"),
        ("AI Provider:", "Google Gemini Developer API (`gemini-3.5-flash`)"),
        ("Resilience:", "Multi-model fallback + offline reference corpus"),
        ("Transparency:", "Dynamic UI badges showing current analysis mode"),
        ("Zero Overhead:", "Portable Node runtime bundled in `.tools/node`")
    ]
    for a_k, a_v in ai_items:
        p = tf_ai_s.add_paragraph() if tf_ai_s.paragraphs[0].text else tf_ai_s.paragraphs[0]
        p.space_after = Pt(12)
        r1 = p.add_run()
        r1.text = f"{a_k} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_PURPLE
        r2 = p.add_run()
        r2.text = a_v
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 10: REAL-WORLD DEMOS & CONCLUSION
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Demonstration Scenarios & Hackathon Impact", "SUMMARY & IMPACT")

    # 4 Demo Cards
    demo_w = Inches(2.7)
    demo_gap = Inches(0.3)
    d_top = Inches(1.8)
    d_h = Inches(3.6)

    demos = [
        ("DEMO 1: SCHOOLS", "School Closure Hoax", COLOR_AMBER,
         "V1: Oakridge High fumigation (2d)\n-> V2: All district schools shut\n-> V3: Statewide emergency decree\n\nShows: Scope inflation & dropped caveats."),
        
        ("DEMO 2: HEALTH", "Biotech Miracle Cure", COLOR_GREEN,
         "V1: Promising lab mouse trial\n-> V2: Universal cancer treatment\n-> V3: Big pharma coverup conspiracy\n\nShows: Condition loss & sensationalism."),
        
        ("DEMO 3: CELEBRITY", "Celebrity Death Rumour", COLOR_RED,
         "V1: Routine outpatient visit\n-> V2: Critical ICU hospitalization\n-> V3: False fatal obituary\n\nShows: Speed of unverified viral spreads."),
        
        ("DEMO 4: FINANCE", "Currency Demonetization", ACCENT_SKY,
         "V1: Routine security watermark update\n-> V2: Phasing out old denominations\n-> V3: Complete sudden cash ban panic\n\nShows: Panic triggers in financial news.")
    ]

    for idx, (d_badge, d_title, d_col, d_body) in enumerate(demos):
        dx = Inches(0.8) + idx * (demo_w + demo_gap)
        add_card(s10, dx, d_top, demo_w, d_h, "", d_col)
        
        tb = s10.shapes.add_textbox(dx + Inches(0.2), d_top + Inches(0.2), demo_w - Inches(0.4), d_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = d_badge
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = d_col
        
        p2 = tf.add_paragraph()
        p2.text = d_title
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(8)
        
        p3 = tf.add_paragraph()
        p3.text = d_body
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_LIGHT

    # Bottom Banner: Call to Action / Pitch Summary
    banner = add_card(s10, Inches(0.8), Inches(5.7), Inches(11.7), Inches(1.2), "", ACCENT_SKY)
    b_tb = s10.shapes.add_textbox(Inches(1.05), Inches(5.85), Inches(11.2), Inches(0.9))
    b_tf = b_tb.text_frame
    b_tf.word_wrap = True
    b_tf.margin_left = b_tf.margin_top = b_tf.margin_right = b_tf.margin_bottom = 0
    
    bp1 = b_tf.paragraphs[0]
    bp1.text = "VERIFY BEFORE YOU SHARE — EMPOWERING CRITICAL THINKING IN THE AI ERA"
    bp1.font.size = Pt(15)
    bp1.font.bold = True
    bp1.font.color.rgb = COLOR_GREEN
    
    bp2 = b_tf.add_paragraph()
    bp2.text = "Evolution Tracker 2.0 does not just debunk claims—it educates users on the mechanics of deception, equipping society with the tools to dissect misinformation at its source."
    bp2.font.size = Pt(12)
    bp2.font.color.rgb = TEXT_WHITE

    # Save presentation
    out_path = os.path.abspath(filename)
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")
    return out_path

if __name__ == "__main__":
    create_deck()
