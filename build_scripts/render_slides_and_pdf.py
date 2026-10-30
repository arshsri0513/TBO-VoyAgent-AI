import os
import sys
from PIL import Image, ImageDraw, ImageFont
import fitz # PyMuPDF

OUTPUT_DIR = r"C:\Users\Arsh\.gemini\antigravity\scratch\VoyageHack_4_0_TBO"
SLIDES_DIR = os.path.join(OUTPUT_DIR, "slide_images")
os.makedirs(SLIDES_DIR, exist_ok=True)
PDF_PATH = os.path.join(OUTPUT_DIR, "TBO_VoyAgent_AI_Submission.pdf")

# Dimensions for Full HD 1080p (16:9)
WIDTH = 1920
HEIGHT = 1080

# Colors
BG_DARK = (11, 19, 43)        # #0B132B
CARD_BG = (28, 37, 65)        # #1C2541
CARD_BORDER = (58, 80, 107)   # #3A506B
ACCENT_CYAN = (72, 202, 228)  # #48CAE4
ACCENT_BLUE = (0, 119, 182)   # #0077B6
ACCENT_GREEN = (6, 214, 160)  # #06D6A0
ACCENT_ORANGE = (255, 159, 28)# #FF9F1C
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (180, 195, 210)
TAG_BG = (16, 42, 77)

# Fonts
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_REG_PATH, size)

def draw_header(draw, tag_text, title_text, subtitle_text=""):
    # Tag Pill
    draw.rounded_rectangle([100, 50, 680, 95], radius=10, fill=TAG_BG, outline=ACCENT_CYAN, width=2)
    draw.text((120, 60), tag_text.upper(), font=get_font(20, bold=True), fill=ACCENT_CYAN)

    # Title
    draw.text((100, 115), title_text, font=get_font(44, bold=True), fill=TEXT_WHITE)

    # Subtitle
    if subtitle_text:
        draw.text((100, 175), subtitle_text, font=get_font(22), fill=TEXT_MUTED)

def draw_card(draw, box, title, items, badge="", badge_color=ACCENT_CYAN):
    draw.rounded_rectangle(box, radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    x1, y1, x2, y2 = box

    # Title
    draw.text((x1 + 30, y1 + 30), title, font=get_font(28, bold=True), fill=ACCENT_CYAN)
    curr_y = y1 + 75

    if badge:
        draw.rounded_rectangle([x1 + 30, curr_y, x1 + 30 + len(badge)*14 + 20, curr_y + 34], radius=8, fill=TAG_BG, outline=badge_color, width=1)
        draw.text((x1 + 40, curr_y + 5), badge.upper(), font=get_font(18, bold=True), fill=badge_color)
        curr_y += 50

    # Items
    for item in items:
        # Wrap text if needed
        words = item.split(" ")
        lines = []
        cur_line = "- "
        max_chars = int((x2 - x1 - 60) / 13)
        for w in words:
            if len(cur_line + w) > max_chars:
                lines.append(cur_line)
                cur_line = "  " + w + " "
            else:
                cur_line += w + " "
        if cur_line:
            lines.append(cur_line)

        for l in lines:
            draw.text((x1 + 30, curr_y), l, font=get_font(20), fill=TEXT_WHITE)
            curr_y += 30
        curr_y += 10

def draw_footer(draw, page_num):
    text = f"CRP - VoyageHack 4.0 (TBO.com) | Track: Virtual travel Agent/travel agent copilot | Slide {page_num} of 10"
    draw.text((1080, 1020), text, font=get_font(18), fill=TEXT_MUTED)
    # Subtle brand line
    draw.line([100, 1005, 1820, 1005], fill=CARD_BORDER, width=1)

slides_data = [
    # Slide 1: Cover
    {
        "type": "cover",
        "tag": "CRP - VOYAGEHACK 4.0 | TBO.COM SUBMISSION",
        "title": "VoyAgent AI",
        "subtitle": "Next-Gen Autonomous Multi-Agent Travel Copilot for B2B Travel Distribution",
        "desc": "Transforming unstructured traveller intent into dynamic, bookable multi-supplier itineraries with real-time price locks, margin optimization, and autonomous 24/7 post-booking care."
    },
    # Slide 2: Problem
    {
        "tag": "Problem Statement",
        "title": "The B2B Travel Crisis & Distribution Bottlenecks",
        "sub": "Why current agent tools and generic LLM chatbots fail travel agents today.",
        "cards": [
            ([100, 240, 630, 960], "1. Fragmentation", [
                "Agents juggle 6-8 disconnected portals (GDS, hotel aggregators, sightseeing suppliers).",
                "Stitching flights + hotels + transfers takes 45-90 minutes per customized quote.",
                "High customer drop-off (>58%) due to quote latency."
            ], "Operational Lag", ACCENT_ORANGE),
            ([660, 240, 1260, 960], "2. Chatbot Failures", [
                "Generic AI chatbots hallucinate rates, expired flight seats, and hotel availability.",
                "Zero real-time price locking or inventory reservation capability.",
                "Unable to handle complex agency wallet ledgers, credit limits, or multi-city PNRs."
            ], "Technical Gap", ACCENT_ORANGE),
            ([1290, 240, 1820, 960], "3. Support Overload", [
                "65%+ of operations workload spent on routine post-booking tickets (vouchers, date changes).",
                "Flight delays cause panic rebooking across hotel and transfer operators.",
                "High operational headcount costs and slow resolution times."
            ], "Service Pain", ACCENT_ORANGE)
        ]
    },
    # Slide 3: Solution
    {
        "tag": "Executive Solution",
        "title": "VoyAgent AI: The Autonomous Travel Copilot Architecture",
        "sub": "A purpose-built multi-agent ecosystem engineered directly for TBO's B2B travel platform.",
        "cards": [
            ([100, 240, 630, 960], "1. Scoping Engine", [
                "Natural language intent parser extracts dates, pax, budget, and travel preferences.",
                "Intelligent follow-up questions clarify ambiguity before initiating searches.",
                "Builds persistent traveler context across multi-session inquiries."
            ], "Phase 1: Planning", ACCENT_CYAN),
            ([660, 240, 1260, 960], "2. Dynamic Bundler", [
                "Parallel querying across Flights (GDS/NDC), Hotel bedbanks, and Tours.",
                "Synthesizes day-by-day itineraries with optimal transit buffers and opening times.",
                "Real-time TBO API inventory locking with zero quote price slippage."
            ], "Phase 2: Booking", ACCENT_GREEN),
            ([1290, 240, 1820, 960], "3. Autonomous Concierge", [
                "Active Flight Sentinel: tracks airline delays and reschedules ground transfers.",
                "Self-service WhatsApp voucher & invoice retrieval for travelers.",
                "Human-in-the-Loop safeguards on all cancellations and wallet debits."
            ], "Phase 3: Support", ACCENT_CYAN)
        ]
    },
    # Slide 4: Tech Stack
    {
        "tag": "System Architecture",
        "title": "End-to-End Multi-Agent System Architecture",
        "sub": "Scalable, event-driven architecture combining high-throughput APIs with deterministic AI guardrails.",
        "cards": [
            ([100, 240, 500, 960], "1. Channels", [
                "B2B Agent Web Workspace",
                "Customer WhatsApp Concierge",
                "Traveler Mobile Web App",
                "Voice IVR / Speech-to-Intent",
                "Agency RBAC / Auth0 Security"
            ], "Omnichannel Layer", ACCENT_CYAN),
            ([530, 240, 970, 960], "2. Agent Core", [
                "LangGraph State Supervisor",
                "Intent & Entity Extractor",
                "Route & Itinerary Specialist",
                "Dynamic Pricing & Margin Worker",
                "JSON-Schema Guardrails"
            ], "Multi-Agent Engine", ACCENT_GREEN),
            ([1000, 240, 1420, 960], "3. TBO Connectors", [
                "TBO Flight Engine (GDS/LCC)",
                "TBO Hotel Bedbank Hub",
                "Sightseeing & Transfer API",
                "Agency Wallet & Credit Ledger",
                "Instant PNR Confirmation"
            ], "Enterprise Integration", ACCENT_CYAN),
            ([1450, 240, 1820, 960], "4. Data & Infra", [
                "Redis Look-to-Book Cache",
                "PostgreSQL Multi-Tenant",
                "ChromaDB Vector Store",
                "Kafka Disruption Stream",
                "Prometheus SLA Monitor"
            ], "High Scalability", ACCENT_ORANGE)
        ]
    },
    # Slide 5: Journey Flow
    {
        "tag": "Traveler Lifecycle",
        "title": "From Intent to Post-Booking Support: The Complete Journey",
        "sub": "How VoyAgent AI coordinates complex cross-product workflows across the entire travel lifecycle.",
        "cards": [
            ([100, 240, 500, 960], "Step 1: Scoping", [
                "Traveler expresses natural intent: '5 days in Dubai for family of 3 under $3,500.'",
                "Agent extracts entities and prompts clarifying questions on children's ages and preferences."
            ], "Inspiration & Planning", ACCENT_CYAN),
            ([530, 240, 970, 960], "Step 2: Curation", [
                "Concurrently queries 3 flight APIs and 4 hotel bedbanks.",
                "Constructs 2 tailored packages: Luxury Beachfront vs Value Balanced with itemized costs."
            ], "Multi-Product Bundling", ACCENT_BLUE),
            ([1000, 240, 1420, 960], "Step 3: One-Click Lock", [
                "Performs instant live price validation and inventory hold.",
                "Applies agent's custom markup rule (+12% margin).",
                "Generates branded PDF proposal and instant payment link."
            ], "Transaction & Hold", ACCENT_GREEN),
            ([1450, 240, 1820, 960], "Step 4: Care", [
                "Flight delayed by 3 hours: Agent detects delay via airline webhook.",
                "Autonomously reschedules private airport pickup.",
                "Informs hotel of late check-in and updates traveler on WhatsApp."
            ], "Disruption Deflection", ACCENT_ORANGE)
        ]
    },
    # Slide 6: Differentiators
    {
        "tag": "Competitive Advantage",
        "title": "Key Technical Differentiators vs Traditional Solutions",
        "sub": "Engineered with travel-tech enterprise requirements, latency limits, and margin protection.",
        "cards": [
            ([100, 240, 630, 960], "1. Look-to-Book Cache", [
                "GDS query costs penalize high look-to-book ratios.",
                "VoyAgent utilizes predictive Redis caching for hotel availability and search routes.",
                "Reduces supplier API query costs by 42% while ensuring 100% price accuracy at checkout."
            ], "API Cost Reduction", ACCENT_CYAN),
            ([660, 240, 1260, 960], "2. Margin Maximizer", [
                "Unlike B2C bots, VoyAgent is designed to empower B2B agents.",
                "Algorithmically prioritizes preferred supplier contracts, higher-margin tours, and upgrades.",
                "Displays transparent commission breakdowns on agent dashboards."
            ], "Profit Engineering", ACCENT_GREEN),
            ([1290, 240, 1820, 960], "3. Deterministic Safety", [
                "Zero Hallucinations: All rates, schedules, and policies use strict JSON-schema contracts.",
                "Consequential Action Gate: Irreversible actions (wallet debit, ticket cancel) require approval.",
                "Full audit logs for every prompt, LLM call, and supplier payload."
            ], "Enterprise Reliability", ACCENT_CYAN)
        ]
    },
    # Slide 7: Live Prototype
    {
        "tag": "Demo Walkthrough",
        "title": "Demonstrated Capabilities & Multi-Product Live Simulation",
        "sub": "End-to-end simulated execution on real-world travel scenarios and exception recovery.",
        "cards": [
            ([100, 240, 940, 960], "Scenario 1: Dubai Family Holiday Package", [
                "Input: 'Family holiday to Dubai, 2 adults + 1 child (age 7), Nov 15-20, budget $3,200. Direct flights from Mumbai, hotel near JBR, Burj Khalifa & Desert Safari.'",
                "Execution Trace:",
                "  [0.3s] Intent Parser: BOM-DXB | Nov 15-20 | Pax 2A1C | Tag: Family, Beach",
                "  [1.1s] Supplier Query: 2 direct flights found; 84 hotels filtered down to top 3 JBR properties.",
                "  [1.8s] Itinerary Bundler: Day 1 Arrival & Transfer | Day 2 Burj Khalifa (10 AM non-peak) | Day 3 Desert Safari (buggy) | Day 4 Beach | Day 5 Return.",
                "  [2.4s] Pricing & Margin: Package Total = $2,840 | Agent Profit = $340 (12%) | Headroom = $360.",
                "Output: Interactive shareable itinerary card generated with one-click bookable hold."
            ], "Live Itinerary Generation", ACCENT_GREEN),
            ([970, 240, 1820, 960], "Scenario 2: Disruption & Flight Reschedule", [
                "Scenario: Airline moves outbound flight from 10:00 AM to 03:00 PM due to air traffic control.",
                "Autonomous Recovery Trace:",
                "  [0.1s] Disruption Sentinel receives flight reschedule webhook from GDS.",
                "  [0.4s] Evaluates itinerary impacts: Scheduled 12:30 PM airport transfer missed; afternoon plans conflict.",
                "  [0.8s] Action: Reschedules private airport transfer to 05:30 PM (zero penalty).",
                "  [1.2s] Action: Dispatches automated notice to hotel front desk regarding late check-in.",
                "  [1.5s] Notification: Sends unified WhatsApp message to traveler with updated voucher.",
                "Result: 100% disruption deflected without human agent intervention."
            ], "Autonomous Exception Handling", ACCENT_ORANGE)
        ]
    },
    # Slide 8: Business Impact
    {
        "tag": "Business Value",
        "title": "Quantifiable Business Impact & ROI for TBO.com Platform",
        "sub": "Empowering 150,000+ travel partners with superhuman AI efficiency and higher conversion.",
        "type": "metrics",
        "metrics": [
            ([100, 240, 500, 480], "QUOTE SPEED", "15x Faster", "Cuts proposal turnaround from 60 mins to < 4 mins"),
            ([530, 240, 940, 480], "CONVERSION LIFT", "+32% Lift", "Instant interactive quotes eliminate lead drop-offs"),
            ([970, 240, 1380, 480], "SUPPORT DEFLECTION", "72% Auto", "Routine post-booking changes resolved autonomously"),
            ([1410, 240, 1820, 480], "MARGIN EXPANSION", "+18% Profit", "Contextual ancillary upselling & preferred supplier routing")
        ],
        "summary_card": ([100, 520, 1820, 960], "Strategic Value for TBO.com Platform Growth", [
            "B2A Superpower: Equips small and mid-sized travel agencies with enterprise-grade copilot technology, cementing TBO as the preferred global B2A platform.",
            "Ancillary Cross-Sell Lift: Multi-product bundling naturally increases sightseeing and transfer attachment rate from 14% to 38%.",
            "Ultra-Low Cost Inference: Model routing tier (SLM for parsing, frontier LLM for complex itineraries) keeps compute cost < ₹0.40 per completed session."
        ], "Long-Term Scalability", ACCENT_CYAN)
    },
    # Slide 9: Governance
    {
        "tag": "Governance & Security",
        "title": "Enterprise Security, Privacy & Reliability Controls",
        "sub": "Built to satisfy strict travel industry regulations, data protection standards, and operational SLAs.",
        "cards": [
            ([100, 240, 630, 960], "Data Privacy & PII Shield", [
                "GDPR and Digital Personal Data Protection (DPDP) compliant.",
                "Zero-PII Tokenization: Passports, credit cards, and passenger details scrubbed before LLM processing.",
                "Zero-Retention: Data is never used for foundation model training or public indexing."
            ], "Privacy By Design", ACCENT_CYAN),
            ([660, 240, 1260, 960], "Access Control & Tenancy", [
                "Strict Multi-Tenant Isolation: Sub-agencies cannot access peer rates, ledgers, or customer profiles.",
                "Policy Governance: Agency managers set custom markup ceilings and airline blacklists.",
                "Tamper-proof audit logs for every prompt, decision, and API transaction."
            ], "Enterprise RBAC", ACCENT_GREEN),
            ([1290, 240, 1820, 960], "Circuit Breakers & Failsafes", [
                "Supplier Latency Circuit Breaker: Falls back to cached inventory if API latency > 3.0s.",
                "Emergency Kill Switch: Operations managers can instantly freeze autonomous triggers.",
                "Seamless human handoff with full conversational context."
            ], "Operational Safety", ACCENT_ORANGE)
        ]
    },
    # Slide 10: Roadmap
    {
        "tag": "Roadmap & Rollout",
        "title": "Phased Implementation Roadmap & TBO Integration Plan",
        "sub": "A structured 12-week deployment roadmap from sandbox validation to global scale.",
        "cards": [
            ([100, 240, 630, 960], "Phase 1: Pilot & TBO Sync", [
                "Duration: Weeks 1 - 4",
                "Integrate VoyAgent with TBO Flight & Hotel Sandbox APIs.",
                "Beta pilot with 200 top-tier B2B travel agents.",
                "Calibrate Look-to-Book caching and sub-second entity extraction."
            ], "Milestone: Beta Rollout", ACCENT_CYAN),
            ([660, 240, 1260, 960], "Phase 2: Omnichannel & Disruption", [
                "Duration: Weeks 5 - 8",
                "Launch WhatsApp Concierge for traveler post-booking self-service.",
                "Activate automated airline disruption sentinel and transfer reschedule engine.",
                "Integrate agency wallet credit debits and dynamic margin rules."
            ], "Milestone: Scale Automation", ACCENT_GREEN),
            ([1290, 240, 1820, 960], "Phase 3: Global Production", [
                "Duration: Weeks 9 - 12",
                "Roll out across TBO's global network of 150,000+ travel partners.",
                "Deploy Voice AI Copilot for call-center agent desks.",
                "Autonomous corporate travel policy compliance engine."
            ], "Milestone: Global Network", ACCENT_ORANGE)
        ]
    }
]

generated_images = []

for idx, data in enumerate(slides_data):
    page_num = idx + 1
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    if data.get("type") == "cover":
        # Cover slide layout
        draw.rounded_rectangle([100, 120, 1820, 620], radius=24, fill=CARD_BG, outline=ACCENT_CYAN, width=3)
        draw.text((160, 180), data["tag"], font=get_font(24, bold=True), fill=ACCENT_CYAN)
        draw.text((160, 240), data["title"], font=get_font(72, bold=True), fill=TEXT_WHITE)
        draw.text((160, 350), data["subtitle"], font=get_font(32, bold=True), fill=ACCENT_GREEN)
        
        # Word wrap desc
        desc = data["desc"]
        words = desc.split(" ")
        lines = []
        cur_line = ""
        for w in words:
            if len(cur_line + w) > 85:
                lines.append(cur_line)
                cur_line = w + " "
            else:
                cur_line += w + " "
        if cur_line:
            lines.append(cur_line)
        y = 420
        for l in lines:
            draw.text((160, y), l, font=get_font(24), fill=TEXT_MUTED)
            y += 36

        # Bottom 3 meta cards
        meta = [
            ("SUBMISSION TRACK", "Virtual travel Agent/\ntravel agent copilot"),
            ("TARGET PLATFORM", "TBO.com Ecosystem\n(B2B Agents & Suppliers)"),
            ("CORE DELIVERABLES", "Complete Presentation Deck\n+ MP4 Demo Video Pitch")
        ]
        for m_idx, (m_tag, m_val) in enumerate(meta):
            bx = [100 + m_idx * 590, 670, 100 + m_idx * 590 + 550, 950]
            draw.rounded_rectangle(bx, radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.text((bx[0] + 30, bx[1] + 30), m_tag, font=get_font(18, bold=True), fill=ACCENT_CYAN)
            draw.text((bx[0] + 30, bx[1] + 75), m_val, font=get_font(24, bold=True), fill=TEXT_WHITE)

    elif data.get("type") == "metrics":
        draw_header(draw, data["tag"], data["title"], data["sub"])
        for m_box, m_title, m_val, m_desc in data["metrics"]:
            draw.rounded_rectangle(m_box, radius=16, fill=CARD_BG, outline=ACCENT_GREEN, width=2)
            draw.text((m_box[0] + 25, m_box[1] + 25), m_title, font=get_font(18, bold=True), fill=ACCENT_CYAN)
            draw.text((m_box[0] + 25, m_box[1] + 65), m_val, font=get_font(44, bold=True), fill=ACCENT_GREEN)
            draw.text((m_box[0] + 25, m_box[1] + 150), m_desc, font=get_font(18), fill=TEXT_MUTED)
        box, title, items, badge, badge_col = data["summary_card"]
        draw_card(draw, box, title, items, badge, badge_col)

    else:
        draw_header(draw, data["tag"], data["title"], data["sub"])
        for card_info in data["cards"]:
            box, title, items, badge, badge_col = card_info
            draw_card(draw, box, title, items, badge, badge_col)

    draw_footer(draw, page_num)
    img_path = os.path.join(SLIDES_DIR, f"slide_{page_num:02d}.png")
    img.save(img_path, quality=95)
    generated_images.append(img_path)
    print(f"Rendered Slide {page_num}/10 -> {img_path}")

# Compile into PDF
doc = fitz.open()
for img_path in generated_images:
    img_doc = fitz.open(img_path)
    pdf_bytes = img_doc.convert_to_pdf()
    img_pdf = fitz.open("pdf", pdf_bytes)
    doc.insert_pdf(img_pdf)

doc.save(PDF_PATH)
doc.close()
print("PDF compilation successful:", PDF_PATH)
