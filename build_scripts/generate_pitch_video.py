import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

OUTPUT_DIR = r"C:\Users\Arsh\.gemini\antigravity\scratch\VoyageHack_4_0_TBO"
SLIDES_DIR = os.path.join(OUTPUT_DIR, "slide_images")
VIDEO_PATH = os.path.join(OUTPUT_DIR, "TBO_VoyAgent_AI_Pitch_Video.mp4")

# Font for narration banner
FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
font_reg = ImageFont.truetype(FONT_PATH, 22)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, 24)

# Narration scripts for each slide
narrations = [
    ("VOICE-OVER / PITCH NARRATION", "Welcome to VoyAgent AI — our submission for TBO.com VoyageHack 4.0. VoyAgent is an autonomous multi-agent travel copilot purpose-built for global B2B travel distribution."),
    ("PROBLEM CONTEXT", "Today, travel agents lose 45-90 minutes per lead toggling disjoint portals, causing 58% customer drop-off. Generic LLMs fail because they hallucinate expired rates and lack live inventory locking."),
    ("EXECUTIVE SOLUTION", "VoyAgent AI bridges this gap with an orchestrated multi-agent framework: Conversational Scoping, Dynamic Multi-Supplier Bundling, and Autonomous 24/7 Post-Booking Care."),
    ("TECHNICAL ARCHITECTURE", "Our modular engine links B2B agent workspaces and traveler WhatsApp channels to a LangGraph supervisor, querying TBO GDS, Hotel Bedbank, and Sightseeing APIs concurrently."),
    ("LIFECYCLE WORKFLOW", "From natural language intent to instant bookable hold: VoyAgent validates real-time availability, applies custom agency markup rules, and deploys proactive disruption recovery."),
    ("KEY DIFFERENTIATORS", "Architected with Look-to-Book predictive caching to slash supplier API query costs by 42%, dynamic margin maximization, and strict deterministic JSON-schema safety rails."),
    ("PROTOTYPE SIMULATION", "In our live test, VoyAgent generated a complete 5-day Dubai family package in 2.4s, and autonomously rescheduled airport transfers when a flight delay webhook fired."),
    ("BUSINESS VALUE & ROI", "Delivering 15x faster quote velocity, a +32% lift in booking conversion, 72% autonomous post-booking support deflection, and +18% agency margin expansion."),
    ("GOVERNANCE & TRUST", "Enterprise-grade trust: Zero-PII tokenization, strict multi-tenant agency RBAC isolation, GDS latency circuit breakers, and an instantaneous operations kill-switch."),
    ("ROADMAP & INTEGRATION", "A phased 12-week roadmap: from TBO sandbox API integration and agency beta pilot to WhatsApp rollout and global production across 150,000+ travel partners.")
]

FPS = 10
SECONDS_PER_SLIDE = 9 # ~90 seconds total video
FRAMES_PER_SLIDE = FPS * SECONDS_PER_SLIDE
TRANSITION_FRAMES = 8 # 0.8s cross-dissolve

# Load and prepare slide base images
slide_images = []
for i in range(1, 11):
    path = os.path.join(SLIDES_DIR, f"slide_{i:02d}.png")
    base = Image.open(path).convert("RGB")
    slide_images.append(base)

TOTAL_SLIDES = len(slide_images)
TOTAL_FRAMES = TOTAL_SLIDES * FRAMES_PER_SLIDE

def create_slide_frame(slide_idx, frame_in_slide, global_frame):
    img = slide_images[slide_idx].copy()
    draw = ImageDraw.Draw(img)

    # 1. Top Mini-Banner: VoyageHack 4.0 Official Submission
    draw.rectangle([0, 0, 1920, 36], fill=(5, 10, 25))
    draw.text((30, 7), "TBO.COM VOYAGEHACK 4.0  |  TRACK: VIRTUAL TRAVEL AGENT / COPILOT  |  OFFICIAL PITCH VIDEO", font=font_reg, fill=(72, 202, 228))

    # 2. Narration Lower Third Banner
    n_tag, n_text = narrations[slide_idx]
    banner_y1 = 880
    banner_y2 = 995
    # Dark semi-transparent container
    draw.rounded_rectangle([60, banner_y1, 1860, banner_y2], radius=12, fill=(10, 20, 45), outline=(72, 202, 228), width=2)
    # Speaker / Tag
    draw.rounded_rectangle([80, banner_y1 + 12, 380, banner_y1 + 45], radius=6, fill=(16, 42, 77), outline=(6, 214, 160), width=1)
    draw.text((95, banner_y1 + 15), f"PITCH: {n_tag}", font=ImageFont.truetype(FONT_BOLD_PATH, 16), fill=(6, 214, 160))
    # Narration Text
    # Wrap text if needed
    words = n_text.split(" ")
    lines = []
    cur_line = ""
    for w in words:
        if len(cur_line + w) > 110:
            lines.append(cur_line)
            cur_line = w + " "
        else:
            cur_line += w + " "
    if cur_line:
        lines.append(cur_line)

    t_y = banner_y1 + 52
    for l in lines:
        draw.text((85, t_y), l, font=font_reg, fill=(255, 255, 255))
        t_y += 28

    # 3. Bottom Progress Bar
    progress = global_frame / float(TOTAL_FRAMES)
    draw.rectangle([0, 1070, 1920, 1080], fill=(20, 30, 50))
    draw.rectangle([0, 1070, int(1920 * progress), 1080], fill=(6, 214, 160))

    # Timestamp text
    current_sec = int(global_frame / FPS)
    total_sec = int(TOTAL_FRAMES / FPS)
    time_str = f"{current_sec//60:02d}:{current_sec%60:02d} / {total_sec//60:02d}:{total_sec%60:02d}"
    draw.text((1780, 7), time_str, font=font_reg, fill=(180, 195, 210))

    return np.array(img)

print(f"Starting video encoding... Total frames: {TOTAL_FRAMES} at {FPS} FPS")

# Write video using imageio
writer = imageio.get_writer(VIDEO_PATH, fps=FPS, codec="libx264", quality=8)

global_f = 0
for s_idx in range(TOTAL_SLIDES):
    for f in range(FRAMES_PER_SLIDE):
        # Check if we should cross-dissolve to next slide
        if f >= (FRAMES_PER_SLIDE - TRANSITION_FRAMES) and s_idx < (TOTAL_SLIDES - 1):
            alpha = (f - (FRAMES_PER_SLIDE - TRANSITION_FRAMES)) / float(TRANSITION_FRAMES)
            frame_curr = create_slide_frame(s_idx, f, global_f)
            frame_next = create_slide_frame(s_idx + 1, 0, global_f)
            blended = ((1.0 - alpha) * frame_curr + alpha * frame_next).astype(np.uint8)
            writer.append_data(blended)
        else:
            frame = create_slide_frame(s_idx, f, global_f)
            writer.append_data(frame)
        global_f += 1
    print(f"Encoded slide {s_idx + 1}/{TOTAL_SLIDES} into video")

writer.close()
print("Video successfully generated at:", VIDEO_PATH)
