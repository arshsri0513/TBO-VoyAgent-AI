import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = r"C:\Users\Arsh\.gemini\antigravity\scratch\VoyageHack_4_0_TBO"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PPTX_PATH = os.path.join(OUTPUT_DIR, "TBO_VoyAgent_AI_Submission.pptx")

# 16:9 Widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

prs = pptx.Presentation()
prs.slide_width = SLIDE_WIDTH
prs.slide_height = SLIDE_HEIGHT
blank_layout = prs.slide_layouts[6]

# Professional Color Palette
C_BG_DARK = RGBColor(11, 19, 43)        # #0B132B Deep Space Navy
C_CARD_BG = RGBColor(28, 37, 65)        # #1C2541 Card Slate Navy
C_CARD_BORDER = RGBColor(58, 80, 107)   # #3A506B Card Border
C_ACCENT_CYAN = RGBColor(72, 202, 228)  # #48CAE4 Bright Cyan
C_ACCENT_BLUE = RGBColor(0, 119, 182)   # #0077B6 Royal Blue
C_ACCENT_GREEN = RGBColor(6, 214, 160)  # #06D6A0 Mint Green / ROI
C_ACCENT_ORANGE = RGBColor(255, 159, 28)# #FF9F1C Amber / Warning
C_TEXT_WHITE = RGBColor(255, 255, 255)  # White
C_TEXT_MUTED = RGBColor(180, 195, 210)  # Light Slate Text
C_TAG_BG = RGBColor(16, 42, 77)         # Pill tag background

def add_header(slide, tag_text, title_text, subtitle_text=""):
    # Header tag pill
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(4.5), Inches(0.35))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = C_TAG_BG
    tag_box.line.color.rgb = C_ACCENT_CYAN
    tag_box.line.width = Pt(1)
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = "Segoe UI"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_ACCENT_CYAN
    p_tag.alignment = PP_ALIGN.CENTER

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = C_TEXT_WHITE

    # Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.4))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = C_TEXT_MUTED

def add_card(slide, left, top, width, height, title, items, badge_text="", badge_color=C_ACCENT_CYAN):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD_BG
    card.line.color.rgb = C_CARD_BORDER
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.2)

    # Card Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = C_ACCENT_CYAN
    p_title.space_after = Pt(8)

    if badge_text:
        p_badge = tf.add_paragraph()
        p_badge.text = f"[{badge_text}]"
        p_badge.font.name = "Segoe UI"
        p_badge.font.size = Pt(10)
        p_badge.font.bold = True
        p_badge.font.color.rgb = badge_color
        p_badge.space_after = Pt(8)

    for item in items:
        p_item = tf.add_paragraph()
        p_item.text = f"- {item}"
        p_item.font.name = "Segoe UI"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = C_TEXT_WHITE
        p_item.space_after = Pt(6)

def add_footer(slide, current_page, total_pages=10):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.35))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"CRP - VoyageHack 4.0 (TBO.com) | Track: Virtual travel Agent/travel agent copilot | Slide {current_page} of {total_pages}"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.RIGHT

# Set slide dark background
def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG_DARK
    bg.line.fill.background()
    return bg

# ==========================================
# SLIDE 1: Title & Executive Cover
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Big title badge
t_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.7), Inches(3.6))
t_box.fill.solid()
t_box.fill.fore_color.rgb = C_CARD_BG
t_box.line.color.rgb = C_ACCENT_CYAN
t_box.line.width = Pt(2)
tf1 = t_box.text_frame
tf1.word_wrap = True
tf1.margin_left = Inches(0.5)
tf1.margin_top = Inches(0.5)

p = tf1.paragraphs[0]
p.text = "CRP - VOYAGEHACK 4.0 | TBO.COM SUBMISSION"
p.font.name = "Segoe UI"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p.space_after = Pt(12)

p2 = tf1.add_paragraph()
p2.text = "VoyAgent AI"
p2.font.name = "Segoe UI"
p2.font.size = Pt(40)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_WHITE
p2.space_after = Pt(8)

p3 = tf1.add_paragraph()
p3.text = "Next-Generation Autonomous Multi-Agent Copilot for B2B Travel Distribution"
p3.font.name = "Segoe UI"
p3.font.size = Pt(18)
p3.font.color.rgb = C_ACCENT_GREEN
p3.space_after = Pt(14)

p4 = tf1.add_paragraph()
p4.text = "Transforming complex traveller intent into live bookable multi-supplier itineraries with real-time price locks, margin optimization, and 24/7 post-booking care."
p4.font.name = "Segoe UI"
p4.font.size = Pt(13)
p4.font.color.rgb = C_TEXT_MUTED

# Metadata Cards at bottom
meta1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(3.6), Inches(1.5))
meta1.fill.solid()
meta1.fill.fore_color.rgb = C_CARD_BG
meta1.line.color.rgb = C_CARD_BORDER
tf_m1 = meta1.text_frame
tf_m1.margin_left = Inches(0.3)
tf_m1.margin_top = Inches(0.2)
p = tf_m1.paragraphs[0]
p.text = "SUBMISSION TRACK"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m1.add_paragraph()
p2.text = "Virtual travel Agent/\ntravel agent copilot"
p2.font.size = Pt(14)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_WHITE

meta2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(5.1), Inches(3.6), Inches(1.5))
meta2.fill.solid()
meta2.fill.fore_color.rgb = C_CARD_BG
meta2.line.color.rgb = C_CARD_BORDER
tf_m2 = meta2.text_frame
tf_m2.margin_left = Inches(0.3)
tf_m2.margin_top = Inches(0.2)
p = tf_m2.paragraphs[0]
p.text = "TARGET PLATFORM"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m2.add_paragraph()
p2.text = "TBO.com Ecosystem\n(B2B Agents, GDS & Bedbanks)"
p2.font.size = Pt(14)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_WHITE

meta3 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(5.1), Inches(3.7), Inches(1.5))
meta3.fill.solid()
meta3.fill.fore_color.rgb = C_CARD_BG
meta3.line.color.rgb = C_CARD_BORDER
tf_m3 = meta3.text_frame
tf_m3.margin_left = Inches(0.3)
tf_m3.margin_top = Inches(0.2)
p = tf_m3.paragraphs[0]
p.text = "CORE DELIVERABLES"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m3.add_paragraph()
p2.text = "Working Architecture + Multi-Agent Engine + Demo Video Pitch"
p2.font.size = Pt(13)
p2.font.bold = True
p2.font.color.rgb = C_TEXT_WHITE

add_footer(s1, 1)

# ==========================================
# SLIDE 2: Problem Statement & Industry Pain Points
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "Challenge Context", "The B2B Travel Distribution Crisis & Operational Bottlenecks",
           "Why traditional travel booking engines and generic conversational chatbots fail travel agents today.")

add_card(s2, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "1. Extreme Tool Fragmentation",
         ["Travel agents toggle across 6-8 disjoint portals (GDS terminals, hotel bedbanks, local transfer providers).",
          "Stitching flights + hotels + sightseeing + insurance takes 45 to 90 minutes per customized quote.",
          "High lead abandonment (>58%) as travellers demand instant multi-option packages."],
         "Operational Friction", C_ACCENT_ORANGE)

add_card(s2, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "2. Chatbot Hallucination & Pricing Lag",
         ["Generic LLMs hallucinate flights, expired hotel room rates, or non-existent visa policies.",
          "Live inventory checks fail; price quotes change by the time the customer approves.",
          "Lack of atomic transaction support: chatbots cannot lock GDS PNRs or handle agency credit limits."],
         "Technical Gap", C_ACCENT_ORANGE)

add_card(s2, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "3. Post-Booking Support Blackhole",
         ["Over 65% of customer support tickets involve mundane changes: flight rescheduling, date shifts, vouchers.",
          "Flight cancellations trigger frantic manual scrambling across airline desks and hotel managers.",
          "No autonomous resolution: every disruption incurs high call-center costs and agent churn."],
         "Service Bottleneck", C_ACCENT_ORANGE)

add_footer(s2, 2)

# ==========================================
# SLIDE 3: Proposed Solution - VoyAgent AI
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "Executive Solution", "VoyAgent AI: The Autonomous Travel Copilot Architecture",
           "A multi-agent orchestrated intelligence layer purpose-built for TBO.com's B2B travel ecosystem.")

add_card(s3, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Conversational Scoping Engine",
         ["Intent & Constraint Extractor: Parses multi-modal traveller inputs (budget, family preferences, dates, visas).",
          "Active Clarification: Formulates intelligent follow-ups rather than assuming ambiguous preferences.",
          "Context Memory: Retains traveler loyalty perks, airline seat choices, and past trip nuances."],
         "Phase 1: Inspiration & Planning", C_ACCENT_CYAN)

add_card(s3, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Dynamic Multi-Product Bundler",
         ["Multi-Supplier Live Querying: Concurrent lookups across Flights (NDC/GDS), Hotels, and Sightseeing.",
          "Intelligent Day-Wise Curation: Optimizes travel routes, opening hours, and transfer buffers.",
          "Real-Time Price & Availability Lock: Ensures zero quote slippage with instant TBO API holds."],
         "Phase 2: Validation & Booking", C_ACCENT_GREEN)

add_card(s3, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Autonomous Lifecycle Concierge",
         ["Disruption Sentinel: Real-time flight tracking triggers proactive hotel/transfer rescheduling.",
          "Instant Voucher & Ticket Retrieval: Autonomous WhatsApp & Web self-serve for travelers.",
          "Human-in-the-Loop Safeguards: Explicit approval gating for cancellations and financial transactions."],
         "Phase 3: Post-Booking Autonomy", C_ACCENT_CYAN)

add_footer(s3, 3)

# ==========================================
# SLIDE 4: Technical System Architecture
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Engineering Design", "End-to-End System Architecture & Agent Orchestration",
           "Modular, event-driven multi-agent framework built with high availability and deterministic safety.")

add_card(s4, Inches(0.8), Inches(1.9), Inches(2.75), Inches(4.7),
         "1. Channel & Interface",
         ["B2B Agent Web Workspace",
          "Customer WhatsApp Concierge",
          "Mobile SDK & Web Widget",
          "Voice IVR / Speech-to-Intent",
          "Multi-tenant Agency Auth (JWT / RBAC)"],
         "Omnichannel Ingestion", C_ACCENT_CYAN)

add_card(s4, Inches(3.8), Inches(1.9), Inches(3.1), Inches(4.7),
         "2. Multi-Agent Orchestrator",
         ["LangGraph Stateful Supervisor",
          "Intent Classifier & Entity Parser",
          "Routing Specialist Agent",
          "Itinerary Optimization Worker",
          "Safety & Policy Guardrail (JSON Schema)"],
         "Agentic Core", C_ACCENT_GREEN)

add_card(s4, Inches(7.15), Inches(1.9), Inches(2.9), Inches(4.7),
         "3. TBO Integration Bus",
         ["TBO Flight API (GDS / LCC)",
          "TBO Hotel Bedbank Hub",
          "Sightseeing & Transfer Gateway",
          "Credit Ledger & Wallet Service",
          "Booking Confirmation & PNR Engine"],
         "Enterprise Services", C_ACCENT_CYAN)

add_card(s4, Inches(10.3), Inches(1.9), Inches(2.2), Inches(4.7),
         "4. Data & Infra",
         ["Redis Look-to-Book Cache",
          "PostgreSQL Multi-Tenant",
          "ChromaDB Destination RAG",
          "Kafka Disruption Stream",
          "Prometheus SLA Monitor"],
         "Data Layer", C_ACCENT_ORANGE)

add_footer(s4, 4)

# ==========================================
# SLIDE 5: The Agentic Workflow & User Journey
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "Workflow Execution", "The Travel Lifecycle Journey: From Intent to Post-Booking Support",
           "How VoyAgent AI coordinates complex cross-product tasks seamlessly with full human transparency.")

add_card(s5, Inches(0.8), Inches(1.9), Inches(2.75), Inches(4.7),
         "Step 1: Intent & Discovery",
         ["Input: '5-day trip to Dubai for family of 3, budget $3,500, beach hotel, desert safari.'",
          "Agent extracts: dates, pax composition, budget caps, attraction constraints.",
          "Prompts clarifying questions on kid's age and flight timing preference."],
         "Stage: Planning", C_ACCENT_CYAN)

add_card(s5, Inches(3.8), Inches(1.9), Inches(2.75), Inches(4.7),
         "Step 2: Multi-Item Assembly",
         ["Agent queries 3 airline APIs and 4 bedbanks concurrently.",
          "Synthesizes 2 optimal packages: 'Luxury Waterfront' vs 'Value Balanced'.",
          "Ranks hotel room types with free cancellation and included breakfast."],
         "Stage: Curating", C_ACCENT_BLUE)

add_card(s5, Inches(6.8), Inches(1.9), Inches(2.75), Inches(4.7),
         "Step 3: Verification & Lock",
         ["Agent validates live inventory hold via TBO booking sandbox.",
          "Applies agency markup rule (+12% gross profit).",
          "Renders instant white-label PDF proposal & interactive booking link."],
         "Stage: Booking", C_ACCENT_GREEN)

add_card(s5, Inches(9.8), Inches(1.9), Inches(2.75), Inches(4.7),
         "Step 4: Autonomous Care",
         ["Flight delayed by 3 hours: Agent receives airline webhook.",
          "Autonomous action: Reschedules private airport transfer.",
          "Notifies hotel reception of late check-in and informs guest on WhatsApp."],
         "Stage: Support", C_ACCENT_ORANGE)

add_footer(s5, 5)

# ==========================================
# SLIDE 6: Key Technical Differentiators
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Competitive Edge", "Key Technical Differentiators vs Traditional Solutions",
           "Architectural innovations engineered specifically to satisfy enterprise travel-tech demands.")

add_card(s6, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "1. Look-to-Book Smart Caching",
         ["Travel distribution systems suffer from harsh GDS query look-to-book ratio penalties.",
          "VoyAgent integrates predictive Redis caching for hotel availability and search routes.",
          "Reduces supplier API query costs by 42% while guaranteeing fresh price validation prior to booking."],
         "Cost & Speed Optimization", C_ACCENT_CYAN)

add_card(s6, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "2. Dynamic Margin Maximizer",
         ["Unlike B2C bots, VoyAgent is built for travel agents to maximize profitability.",
          "Algorithmically prioritizes preferred supplier contracts, higher-commission tours, and hotel upgrades.",
          "Delivers transparent net-to-gross commission breakdowns for the agent dashboard."],
         "Agency Profit Engine", C_ACCENT_GREEN)

add_card(s6, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "3. Deterministic Safety Rail",
         ["Zero Hallucination Guarantee: All pricing, flight schedules, and cancellation policies use strict JSON-schema API contracts.",
          "Consequential Action Gate: Irreversible actions (wallet debit, ticket cancel) require explicit agent/user confirmation.",
          "Full Audit Logging: Every LLM prompt, API payload, and user consent recorded for compliance."],
         "Enterprise Reliability", C_ACCENT_CYAN)

add_footer(s6, 6)

# ==========================================
# SLIDE 7: Prototype & Live Demo Walkthrough
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Prototype Walkthrough", "Demonstrated Capabilities & Multi-Product Live Simulation",
           "Real-time validation of multi-supplier discovery, dynamic itinerary bundling, and disruption handling.")

add_card(s7, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.7),
         "Live Scenario: Dubai Family Holiday Package",
         ["Traveler Prompt: 'Family holiday to Dubai, 2 adults + 1 child (age 7), Nov 15-20, budget $3,200. Prefer 4-star hotel near JBR, direct flights from Mumbai, include Burj Khalifa & Desert Safari.'",
          "Multi-Agent Execution Log:",
          "  [0.3s] Intent Parser: Dates: 2026-11-15:20 | BOM-DXB | Pax: 2A1C | Tag: Family, Beach",
          "  [1.1s] Supplier Query: 2 Direct flights found; 84 hotels filtered down to top 3 matching JBR.",
          "  [1.8s] Itinerary Bundler: Day 1: Arrival & Transfer | Day 2: Burj Khalifa (10 AM Non-peak) | Day 3: Desert Safari (Child-friendly buggy) | Day 4: Beach leisure | Day 5: Return.",
          "  [2.4s] Price Optimization: Total Package = $2,840. Agency Commission = $340 (12%). Budget headroom = $360.",
          "Output: Complete branded itinerary card generated with one-click bookable hold."],
         "End-to-End Itinerary Generation", C_ACCENT_GREEN)

add_card(s7, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7),
         "Disruption & Post-Booking Recovery Test",
         ["Scenario: Airline reschedules outbound flight from 10:00 AM to 03:00 PM due to air traffic control.",
          "Autonomous Disruption Handling:",
          "  [0.1s] Flight Sentinel receives GDS webhook delay event.",
          "  [0.4s] Agent evaluates itinerary impact: Scheduled 12:30 PM airport transfer will be missed; afternoon marina walk conflicted.",
          "  [0.8s] Automated Action: Modifies private transfer booking to 05:30 PM pickup (zero penalty within window).",
          "  [1.2s] Automated Action: Informs hotel front desk of late check-in to prevent room auto-release.",
          "  [1.5s] Notification: Sends unified WhatsApp update to traveler with revised day plan and updated digital voucher.",
          "Result: 100% disruption deflected without human agent intervention."],
         "Autonomous Exception Handling", C_ACCENT_ORANGE)

add_footer(s7, 7)

# ==========================================
# SLIDE 8: Business Impact & ROI for TBO.com
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "Business Value", "Quantifiable Business Impact & ROI for TBO.com Platform",
           "Delivering massive operational efficiencies, booking conversion lifts, and margin expansion.")

# 4 Metric Highlights
m1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(2.75), Inches(1.8))
m1.fill.solid()
m1.fill.fore_color.rgb = C_CARD_BG
m1.line.color.rgb = C_ACCENT_GREEN
tf_m1 = m1.text_frame
tf_m1.margin_left = Inches(0.2)
p = tf_m1.paragraphs[0]
p.text = "QUOTE VELOCITY"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m1.add_paragraph()
p2.text = "15x Faster"
p2.font.size = Pt(28)
p2.font.bold = True
p2.font.color.rgb = C_ACCENT_GREEN
p3 = tf_m1.add_paragraph()
p3.text = "Cuts itinerary turnaround from 60 mins to < 4 mins"
p3.font.size = Pt(10)
p3.font.color.rgb = C_TEXT_MUTED

m2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.8), Inches(1.9), Inches(2.75), Inches(1.8))
m2.fill.solid()
m2.fill.fore_color.rgb = C_CARD_BG
m2.line.color.rgb = C_ACCENT_GREEN
tf_m2 = m2.text_frame
tf_m2.margin_left = Inches(0.2)
p = tf_m2.paragraphs[0]
p.text = "CONVERSION RATE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m2.add_paragraph()
p2.text = "+32% Lift"
p2.font.size = Pt(28)
p2.font.bold = True
p2.font.color.rgb = C_ACCENT_GREEN
p3 = tf_m2.add_paragraph()
p3.text = "Instant interactive quotes eliminate lead drop-offs"
p3.font.size = Pt(10)
p3.font.color.rgb = C_TEXT_MUTED

m3 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(2.75), Inches(1.8))
m3.fill.solid()
m3.fill.fore_color.rgb = C_CARD_BG
m3.line.color.rgb = C_ACCENT_GREEN
tf_m3 = m3.text_frame
tf_m3.margin_left = Inches(0.2)
p = tf_m3.paragraphs[0]
p.text = "SUPPORT DEFLECTION"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m3.add_paragraph()
p2.text = "72% Automated"
p2.font.size = Pt(28)
p2.font.bold = True
p2.font.color.rgb = C_ACCENT_GREEN
p3 = tf_m3.add_paragraph()
p3.text = "Routine post-booking changes resolved autonomously"
p3.font.size = Pt(10)
p3.font.color.rgb = C_TEXT_MUTED

m4 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.8), Inches(1.9), Inches(2.75), Inches(1.8))
m4.fill.solid()
m4.fill.fore_color.rgb = C_CARD_BG
m4.line.color.rgb = C_ACCENT_GREEN
tf_m4 = m4.text_frame
tf_m4.margin_left = Inches(0.2)
p = tf_m4.paragraphs[0]
p.text = "MARGIN EXPANSION"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_ACCENT_CYAN
p2 = tf_m4.add_paragraph()
p2.text = "+18% Profit"
p2.font.size = Pt(28)
p2.font.bold = True
p2.font.color.rgb = C_ACCENT_GREEN
p3 = tf_m4.add_paragraph()
p3.text = "Dynamic ancillary cross-selling & high-tier supplier routing"
p3.font.size = Pt(10)
p3.font.color.rgb = C_TEXT_MUTED

# Strategic Value Summary below
add_card(s8, Inches(0.8), Inches(4.0), Inches(11.75), Inches(2.6),
         "Strategic Alignment with TBO.com Platform Growth",
         ["B2A (Business-to-Agents) Empowerment: Equips 150,000+ travel buyers with AI superhuman capabilities, driving agent loyalty to TBO.",
          "Ancillary Attachment Expansion: Increases attach rate of Sightseeing, Transfers, and Activities from 14% to 38% via natural contextual bundling.",
          "Ultra-Low Cost Inference: Model routing architecture ensures routine workflows cost < ₹0.40 per session, ensuring massive gross margin sustainability."],
         "Enterprise Scale Impact", C_ACCENT_CYAN)

add_footer(s8, 8)

# ==========================================
# SLIDE 9: Security, Compliance & Governance
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "Governance & Trust", "Enterprise Security, Privacy & Reliability Controls",
           "Built ground-up with travel-industry compliance, role-based isolation, and fail-safe controls.")

add_card(s9, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Data Privacy & PII Protection",
         ["GDPR & Digital Personal Data Protection (DPDP) compliant.",
          "Zero-PII Tokenization: Passport numbers, credit cards, and passenger details scrubbed before LLM processing.",
          "Zero-Retention Agreement: Data is never used for foundation model training or public indexing."],
         "Privacy By Design", C_ACCENT_CYAN)

add_card(s9, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Access Control & Multi-Tenancy",
         ["Strict Role-Based Access Control (RBAC): Agent sub-accounts cannot inspect other agencies' rates or ledgers.",
          "Policy Configuration: Agency admins can define custom markup ceilings, allowed airlines, and credit thresholds.",
          "Audit Trail: Tamper-proof event logs for all agentic decisions and API triggers."],
         "Enterprise RBAC", C_ACCENT_GREEN)

add_card(s9, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Circuit Breakers & Graceful Fallback",
         ["Supplier Latency Circuit Breaker: Automatically falls back to cached rates if GDS endpoint latency > 3.0s.",
          "Emergency Kill Switch: Ops managers can instantly freeze autonomous booking triggers via single-click dashboard.",
          "Seamless Human Hand-off: Unresolved ambiguous requests escalate to live human travel desk with full chat context."],
         "Resilience & Safety", C_ACCENT_ORANGE)

add_footer(s9, 9)

# ==========================================
# SLIDE 10: Implementation Roadmap & TBO Integration
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "Execution Roadmap", "Integration Roadmap & TBO.com Platform Rollout",
           "A phased, production-grade integration strategy designed for rapid pilot and global scale.")

add_card(s10, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Phase 1: Pilot & TBO Core Sync",
         ["Duration: Weeks 1 to 4",
          "Connect VoyAgent with TBO Flight & Hotel Sandbox APIs.",
          "Deploy Agent Web Copilot to select cohort of 200 high-volume B2B travel agents.",
          "Benchmark Look-to-Book caching efficiency and latency SLA (< 2.5s end-to-end response)."],
         "Milestone: Beta Rollout", C_ACCENT_CYAN)

add_card(s10, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Phase 2: Omnichannel & Disruption",
         ["Duration: Weeks 5 to 8",
          "Launch WhatsApp & Mobile Traveler Concierge for post-booking support.",
          "Activate autonomous airline disruption sentinel & transfer rescheduling engine.",
          "Integrate multi-currency agency credit ledger and dynamic markup rules."],
         "Milestone: Automation Scale", C_ACCENT_GREEN)

add_card(s10, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7),
         "Phase 3: Global Production Rollout",
         ["Duration: Weeks 9 to 12",
          "Roll out to TBO's global network of 150,000+ travel partners.",
          "Deploy Voice AI Copilot for agency call-center operations.",
          "Autonomous group booking negotiation engine & corporate policy compliance."],
         "Milestone: Full Ecosystem", C_ACCENT_ORANGE)

add_footer(s10, 10)

# Save presentation
prs.save(PPTX_PATH)
print("Presentation successfully created at:", PPTX_PATH)
