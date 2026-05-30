import streamlit as st
import openai
import json
import time
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="Crew Bridge — Princess Cruises",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  .stApp {
    background: #f4f1ec;
  }

  /* Column backgrounds */
  [data-testid="column"]:first-child {
    background: #1a2744 !important;
    padding: 24px 20px !important;
    min-height: calc(100vh - 64px);
    border-right: 1px solid #2d3f6b;
  }
  [data-testid="column"]:last-child {
    background: #f4f1ec !important;
    padding: 24px 28px !important;
  }

  /* Hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* Header */
  .cb-header {
    background: #1a2744;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #c9a84c;
  }
  .cb-logo {
    font-family: 'Playfair Display', serif;
    color: #fff;
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  .cb-logo span {
    color: #c9a84c;
  }
  .cb-tagline {
    font-family: 'DM Sans', sans-serif;
    color: #a0aec0;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .cb-princess {
    font-family: 'DM Sans', sans-serif;
    color: #c9a84c;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500;
  }

  /* Main layout */
  .cb-main {
    display: grid;
    grid-template-columns: 380px 1fr;
    gap: 0;
    height: calc(100vh - 64px);
  }

  /* Device panel */
  .cb-device-panel {
    background: #1a2744;
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
    border-right: 1px solid #2d3f6b;
  }
  .cb-device-frame {
    background: #111827;
    border-radius: 28px;
    padding: 20px 18px;
    border: 2px solid #2d3f6b;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
  }
  .cb-device-frame::before {
    content: '';
    display: block;
    width: 40px;
    height: 4px;
    background: #2d3f6b;
    border-radius: 2px;
    margin: 0 auto 16px;
  }
  .cb-device-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 14px;
    text-align: center;
  }
  .cb-crew-info {
    background: #1a2744;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 14px;
    border: 1px solid #2d3f6b;
  }
  .cb-crew-name {
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
  }
  .cb-crew-role {
    font-size: 11px;
    color: #c9a84c;
    margin-top: 2px;
  }
  .cb-crew-location {
    font-size: 10px;
    color: #4a5568;
    margin-top: 2px;
  }

  .phrase-section-label {
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 8px;
    font-family: 'DM Sans', sans-serif;
  }

  /* Dashboard panel */
  .cb-dashboard {
    background: #f4f1ec;
    padding: 28px 32px;
    overflow-y: auto;
  }
  .cb-dash-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 24px;
  }
  .cb-dash-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    color: #1a2744;
    font-weight: 600;
  }
  .cb-dash-subtitle {
    font-size: 12px;
    color: #8a8a7a;
    margin-top: 2px;
    letter-spacing: 0.04em;
  }

  /* Stat cards */
  .cb-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
  }
  .cb-stat {
    background: #fff;
    border-radius: 12px;
    padding: 14px 16px;
    border: 1px solid #e8e4da;
  }
  .cb-stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: #1a2744;
    line-height: 1;
  }
  .cb-stat-label {
    font-size: 10px;
    color: #8a8a7a;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* Incident table */
  .cb-table-wrap {
    background: #fff;
    border-radius: 16px;
    border: 1px solid #e8e4da;
    overflow: hidden;
  }
  .cb-table-header {
    background: #1a2744;
    padding: 12px 20px;
    display: grid;
    grid-template-columns: 80px 1fr 90px 140px 80px 100px;
    gap: 12px;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a0aec0;
    font-family: 'DM Sans', sans-serif;
  }
  .cb-incident-row {
    padding: 14px 20px;
    display: grid;
    grid-template-columns: 80px 1fr 90px 140px 80px 100px;
    gap: 12px;
    border-bottom: 1px solid #f0ece4;
    align-items: center;
    transition: background 0.15s;
    font-family: 'DM Sans', sans-serif;
  }
  .cb-incident-row:hover { background: #faf8f4; }
  .cb-incident-row:last-child { border-bottom: none; }
  .cb-cabin { font-size: 13px; font-weight: 600; color: #1a2744; }
  .cb-issue { font-size: 12px; color: #4a5568; line-height: 1.4; }
  .cb-time { font-size: 11px; color: #8a8a7a; }
  .cb-dept { font-size: 11px; color: #1a2744; font-weight: 500; }

  .sev-urgent {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #fff1f0; color: #cf1322; font-size: 10px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid #ffa39e;
  }
  .sev-high {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #fff7e6; color: #d46b08; font-size: 10px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid #ffd591;
  }
  .sev-medium {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #e6f7ff; color: #0958d9; font-size: 10px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid #91caff;
  }
  .sev-low {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #f6ffed; color: #389e0d; font-size: 10px; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid #b7eb8f;
  }

  .status-open {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #f0f0f0; color: #595959; font-size: 10px; font-weight: 500;
    letter-spacing: 0.04em; border: 1px solid #d9d9d9;
  }
  .status-progress {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #e6f4ff; color: #0958d9; font-size: 10px; font-weight: 500;
    letter-spacing: 0.04em; border: 1px solid #91caff;
  }
  .status-resolved {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    background: #f6ffed; color: #389e0d; font-size: 10px; font-weight: 500;
    letter-spacing: 0.04em; border: 1px solid #b7eb8f;
  }

  /* Translation display */
  .cb-translation-box {
    background: #0f1728;
    border-radius: 14px;
    padding: 16px;
    margin-top: 12px;
    border: 1px solid #2d3f6b;
    min-height: 100px;
  }
  .cb-kannada {
    font-size: 16px;
    color: #c9a84c;
    line-height: 1.5;
    margin-bottom: 10px;
  }
  .cb-english {
    font-size: 12px;
    color: #a0aec0;
    line-height: 1.5;
    padding-top: 10px;
    border-top: 1px solid #2d3f6b;
  }
  .cb-classification {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #2d3f6b;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  .cb-class-badge {
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .cb-empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #8a8a7a;
    font-size: 13px;
  }
  .cb-empty-icon {
    font-size: 36px;
    margin-bottom: 12px;
    opacity: 0.4;
  }

  /* Streamlit button overrides */
  .stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
  }

  /* New incident pulse */
  @keyframes pulse-new {
    0% { background: #fffbe6; }
    100% { background: #fff; }
  }
  .new-incident { animation: pulse-new 2s ease-out; }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'incidents' not in st.session_state:
    st.session_state.incidents = []
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None
if 'selected_phrase' not in st.session_state:
    st.session_state.selected_phrase = None
if 'incident_created' not in st.session_state:
    st.session_state.incident_created = False

# Preset phrases
PHRASES = [
    {
        "kannada": "ಕ್ಯಾಬಿನ್‌ನಲ್ಲಿ ಏರ್ ಕಂಡಿಷನರ್ ಸೋರುತ್ತಿದೆ ಮತ್ತು ಶಬ್ದ ಮಾಡುತ್ತಿದೆ",
        "english_hint": "AC leaking and making noise in cabin",
        "label": "AC Leak & Noise"
    },
    {
        "kannada": "ಈ ಬೆಳಿಗ್ಗೆಯಿಂದ ಕೋಣೆಯನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿಲ್ಲ",
        "english_hint": "Room not cleaned since this morning",
        "label": "Room Not Cleaned"
    },
    {
        "kannada": "ಎದೆ ನೋವು ಆಗುತ್ತಿದೆ, ಅನಾರೋಗ್ಯ ಅನಿಸುತ್ತಿದೆ",
        "english_hint": "Chest pain, feeling unwell",
        "label": "Medical: Chest Pain"
    },
    {
        "kannada": "ಕ್ಯಾಬಿನ್ ಬಾಗಿಲಿನ ಬೀಗ ಮುರಿದಿದೆ",
        "english_hint": "Broken lock on cabin door",
        "label": "Broken Door Lock"
    }
]

CABINS = ["4112", "7089", "5234", "8301", "6445", "3178", "9022", "2567"]
CREW_NAMES = ["Maria R.", "James T.", "Ana S.", "David K.", "Rose M."]

def classify_with_claude(kannada_text, english_hint):
    client = openai.OpenAI()
    prompt = f"""You are the AI engine behind Crew Bridge, a ship coordination system for Princess Cruises.

A crew member has captured a guest concern. Analyze it and return ONLY a JSON object with these exact fields:

{{
  "translation": "Clean English translation of the guest's concern",
  "severity": "urgent|high|medium|low",
  "department": "Medical|Security|Hotel Services Engineering|Housekeeping|Food & Beverage|Guest Services",
  "summary": "10 words max — issue summary for the incident card",
  "action": "One sentence — what the assigned department should do immediately"
}}

Guest said (Kannada): {kannada_text}
Context hint: {english_hint}

Severity guide: urgent=medical/safety, high=security/significant damage, medium=maintenance/comfort, low=housekeeping/minor
Return ONLY the JSON. No markdown, no explanation."""

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=400,
        messages=[{"role": "system", "content": "You are the AI engine behind Crew Bridge."}, {"role": "user", "content": prompt}]
    )
    
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)

# HEADER
st.markdown("""
<div class="cb-header">
  <div>
    <div class="cb-logo">Crew<span>Bridge</span></div>
    <div class="cb-tagline">Ship-wide coordination · Every crew member · Every language · Every shift</div>
  </div>
  <div class="cb-princess">⚓ Princess Cruises · mv Regal Princess</div>
</div>
""", unsafe_allow_html=True)

# MAIN LAYOUT
col_device, col_dash = st.columns([1.1, 2.2])

# ── LEFT: CREW DEVICE PANEL ──
with col_device:
    t = st.session_state.translation_result
    phrase = st.session_state.selected_phrase
    created = st.session_state.incident_created

    sev_colors = {
        'urgent': ('#cf1322', '#fff1f0', '#ffa39e'),
        'high':   ('#d46b08', '#fff7e6', '#ffd591'),
        'medium': ('#0958d9', '#e6f7ff', '#91caff'),
        'low':    ('#389e0d', '#f6ffed', '#b7eb8f'),
    }

    def build_screen():
        if not phrase:
            return (
                '<div style="text-align:center;padding:24px 0;">'
                '<div style="font-size:32px;opacity:0.15;margin-bottom:10px;">🎙</div>'
                '<div style="font-size:9px;letter-spacing:0.12em;text-transform:uppercase;'
                'color:#4a5568;font-family:sans-serif;">Awaiting guest input</div>'
                '</div>'
            )
        if t is None:
            return (
                '<div style="text-align:center;padding:16px 0;">'
                '<div style="font-size:9px;text-transform:uppercase;color:#4a5568;'
                'margin-bottom:8px;font-family:sans-serif;">Guest said</div>'
                '<div style="font-size:13px;color:#c9a84c;line-height:1.5;'
                'font-family:sans-serif;">' + phrase['kannada'] + '</div>'
                '<div style="font-size:10px;color:#4a5568;margin-top:12px;">⏳ Translating...</div>'
                '</div>'
            )
        sev = t.get('severity', 'medium').lower()
        sc, sbg, sb = sev_colors.get(sev, sev_colors['medium'])
        done = (
            '<div style="background:#0d2b1a;border-radius:8px;padding:8px;'
            'margin-top:8px;border:1px solid #b7eb8f;text-align:center;">'
            '<div style="font-size:10px;color:#52c41a;font-weight:600;">✓ Routed to dashboard</div>'
            '</div>'
        ) if created else ''
        return (
            '<div>'
            '<div style="font-size:9px;text-transform:uppercase;color:#4a5568;'
            'margin-bottom:4px;font-family:sans-serif;">Guest said</div>'
            '<div style="font-size:11px;color:#c9a84c;line-height:1.4;'
            'padding-bottom:8px;border-bottom:1px solid #1e2530;margin-bottom:8px;">'
            + phrase['kannada'] +
            '</div>'
            '<div style="font-size:9px;text-transform:uppercase;color:#4a5568;'
            'margin-bottom:4px;font-family:sans-serif;">Translation</div>'
            '<div style="font-size:11px;color:#e2e8f0;line-height:1.5;margin-bottom:8px;">'
            + t.get('translation', '') +
            '</div>'
            '<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:6px;">'
            '<span style="font-size:9px;padding:2px 8px;border-radius:20px;font-weight:700;'
            'text-transform:uppercase;color:' + sc + ';background:' + sbg + ';border:1px solid ' + sb + ';">'
            + sev.upper() +
            '</span>'
            '<span style="font-size:9px;padding:2px 8px;border-radius:20px;'
            'color:#c9a84c;background:#1a2744;border:1px solid #2d3f6b;">→ '
            + t.get('department', '') +
            '</span>'
            '</div>'
            '<div style="font-size:9px;color:#4a5568;font-style:italic;">'
            + t.get('action', '') +
            '</div>'
            + done +
            '</div>'
        )

    screen = build_screen()

    device_html = (
        '<div style="display:flex;flex-direction:column;align-items:center;padding:12px 8px 0;">'
        '<div style="width:230px;background:linear-gradient(160deg,#23272f,#1a1d23);'
        'border-radius:28px;border:2px solid #3a3f4a;'
        'box-shadow:0 30px 80px rgba(0,0,0,0.7);overflow:hidden;">'

        # TOP BAR
        '<div style="background:#111317;padding:10px 16px 8px;display:flex;'
        'align-items:center;justify-content:space-between;border-bottom:1px solid #2a2d35;">'
        '<div style="font-size:8px;color:#3a3f4a;letter-spacing:0.12em;'
        'text-transform:uppercase;font-family:sans-serif;">CREW BRIDGE</div>'
        '<div style="display:flex;align-items:center;gap:8px;">'
        '<div style="width:13px;height:13px;border-radius:50%;'
        'background:radial-gradient(circle at 35% 35%,#4a5060,#1a1d23);'
        'border:2px solid #2a2d35;">'
        '<div style="width:4px;height:4px;border-radius:50%;'
        'background:rgba(100,120,180,0.4);margin:3px 0 0 3px;"></div>'
        '</div>'
        '<div style="width:7px;height:7px;border-radius:50%;'
        'background:#22c55e;box-shadow:0 0 6px #22c55e;"></div>'
        '</div></div>'

        # CREW INFO
        '<div style="background:#111827;padding:10px 14px 8px;border-bottom:1px solid #2a2d35;">'
        '<div style="display:flex;justify-content:space-between;align-items:center;">'
        '<div>'
        '<div style="font-size:12px;font-weight:600;color:#e2e8f0;font-family:sans-serif;">Maria R.</div>'
        '<div style="font-size:9px;color:#c9a84c;margin-top:1px;font-family:sans-serif;">Stateroom Attendant · Deck 7</div>'
        '</div>'
        '<div style="text-align:right;">'
        '<div style="font-size:9px;color:#22c55e;font-family:sans-serif;">● ONLINE</div>'
        '<div style="font-size:9px;color:#4a5568;margin-top:1px;font-family:sans-serif;">Shift: 08:00–20:00</div>'
        '</div></div></div>'

        # SCREEN
        '<div style="background:#0d1117;margin:10px 10px 6px;border-radius:12px;'
        'padding:12px;min-height:190px;border:1px solid #1e2530;'
        'box-shadow:inset 0 2px 8px rgba(0,0,0,0.5);font-family:sans-serif;">'
        + screen +
        '</div>'

        # ACTIVATE + PHOTO
        '<div style="display:flex;gap:8px;padding:4px 14px 8px;">'
        '<div style="flex:1;background:#1e2530;border-radius:10px;padding:8px;'
        'text-align:center;border:1px solid #2a3040;box-shadow:0 3px 0 #111317;">'
        '<div style="font-size:16px;">🎙</div>'
        '<div style="font-size:7px;color:#6b7280;letter-spacing:0.1em;'
        'text-transform:uppercase;font-family:sans-serif;margin-top:2px;">Activate</div>'
        '</div>'
        '<div style="flex:1;background:#1e2530;border-radius:10px;padding:8px;'
        'text-align:center;border:1px solid #2a3040;box-shadow:0 3px 0 #111317;">'
        '<div style="font-size:16px;">📷</div>'
        '<div style="font-size:7px;color:#6b7280;letter-spacing:0.1em;'
        'text-transform:uppercase;font-family:sans-serif;margin-top:2px;">Photo</div>'
        '</div></div>'

        # URGENT
        '<div style="padding:2px 14px 10px;">'
        '<div style="background:#1a0a0a;border-radius:14px;padding:6px;'
        'border:2px solid #3a1010;box-shadow:inset 0 3px 8px rgba(0,0,0,0.6);">'
        '<div style="background:linear-gradient(160deg,#dc2626,#991b1b);'
        'border-radius:10px;padding:10px;text-align:center;border:1px solid #ef4444;'
        'box-shadow:0 2px 0 #7f1d1d;">'
        '<div style="font-size:18px;">🚨</div>'
        '<div style="font-size:9px;font-weight:700;color:#fff;letter-spacing:0.15em;'
        'text-transform:uppercase;font-family:sans-serif;">URGENT / MEDICAL</div>'
        '<div style="font-size:8px;color:rgba(255,255,255,0.45);margin-top:2px;'
        'font-family:sans-serif;">Press and hold 2 sec</div>'
        '</div></div></div>'

        # SHIFT END
        '<div style="border-top:1px solid #2a2d35;padding:8px 14px 14px;'
        'display:flex;justify-content:center;">'
        '<div style="background:#111317;border-radius:8px;padding:5px 24px;'
        'border:1px solid #2a2d35;box-shadow:0 2px 0 #0a0b0e;">'
        '<div style="font-size:8px;color:#3a3f4a;letter-spacing:0.1em;'
        'text-transform:uppercase;font-family:sans-serif;">Shift End Sign-off</div>'
        '</div></div>'

        '</div></div>'
    )

    st.markdown(device_html, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:9px;letter-spacing:0.12em;text-transform:uppercase;"
        "color:#4a5568;margin-bottom:6px;text-align:center;font-family:sans-serif;'>"
        "Simulate guest speaking</div>",
        unsafe_allow_html=True
    )

    for i, p in enumerate(PHRASES):
        if st.button(f"🎙 {p['label']}", key=f"phrase_{i}", use_container_width=True):
            st.session_state.selected_phrase = p
            st.session_state.translation_result = None
            st.session_state.incident_created = False
            st.rerun()

    if phrase and t is None:
        with st.spinner("Translating and classifying..."):
            try:
                result = classify_with_claude(phrase['kannada'], phrase['english_hint'])
                st.session_state.translation_result = result
                st.rerun()
            except Exception as e:
                st.error(f"API error: {e}")

    if t and not created:
        if st.button("⚡ Create Incident → Dashboard", key="create_btn",
                     use_container_width=True, type="primary"):
            sev = t.get('severity', 'medium').lower()
            cabin = random.choice(CABINS)
            incident = {
                "id": f"INC-{1000 + len(st.session_state.incidents) + 1}",
                "cabin": cabin,
                "summary": t.get('summary', t.get('translation', '')[:40]),
                "severity": sev,
                "department": t.get('department', ''),
                "time": datetime.now().strftime("%H:%M"),
                "status": "open",
                "reported_by": "Maria R.",
                "action": t.get('action', '')
            }
            st.session_state.incidents.insert(0, incident)
            st.session_state.incident_created = True
            st.rerun()


with col_dash:

    # Dashboard header
    open_count = sum(1 for i in st.session_state.incidents if i['status'] == 'open')
    progress_count = sum(1 for i in st.session_state.incidents if i['status'] == 'in progress')
    resolved_count = sum(1 for i in st.session_state.incidents if i['status'] == 'resolved')
    total = len(st.session_state.incidents)

    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <div style="font-family:'Playfair Display',serif; font-size:26px; 
      color:#1a2744; font-weight:600;">Operations Dashboard</div>
      <div style="font-size:12px; color:#8a8a7a; margin-top:2px; letter-spacing:0.04em;">
      mv Regal Princess · Live incident tracking · {datetime.now().strftime("%d %b %Y, %H:%M")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px;">
      <div style="background:#fff; border-radius:12px; padding:14px 16px; border:1px solid #e8e4da;">
        <div style="font-family:'Playfair Display',serif; font-size:30px; color:#1a2744;">{total}</div>
        <div style="font-size:10px; color:#8a8a7a; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;">Total Today</div>
      </div>
      <div style="background:#fff; border-radius:12px; padding:14px 16px; border:1px solid #e8e4da;">
        <div style="font-family:'Playfair Display',serif; font-size:30px; color:#cf1322;">{open_count}</div>
        <div style="font-size:10px; color:#8a8a7a; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;">Open</div>
      </div>
      <div style="background:#fff; border-radius:12px; padding:14px 16px; border:1px solid #e8e4da;">
        <div style="font-family:'Playfair Display',serif; font-size:30px; color:#0958d9;">{progress_count}</div>
        <div style="font-size:10px; color:#8a8a7a; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;">In Progress</div>
      </div>
      <div style="background:#fff; border-radius:12px; padding:14px 16px; border:1px solid #e8e4da;">
        <div style="font-family:'Playfair Display',serif; font-size:30px; color:#389e0d;">{resolved_count}</div>
        <div style="font-size:10px; color:#8a8a7a; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;">Resolved</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Incident table
    st.markdown("""
    <div style="background:#fff; border-radius:16px; border:1px solid #e8e4da; overflow:hidden;">
      <div style="background:#1a2744; padding:12px 20px; display:grid; 
      grid-template-columns:90px 70px 1fr 95px 150px 110px 110px; gap:10px;
      font-size:10px; letter-spacing:0.1em; text-transform:uppercase; 
      color:#a0aec0; font-family:'DM Sans',sans-serif;">
        <div>Incident</div>
        <div>Cabin</div>
        <div>Issue</div>
        <div>Severity</div>
        <div>Department</div>
        <div>Status</div>
        <div>Action</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.incidents:
        st.markdown("""
        <div style="background:#fff; border-radius:0 0 16px 16px; border:1px solid #e8e4da; 
        border-top:none; text-align:center; padding:60px 20px;">
          <div style="font-size:32px; opacity:0.3; margin-bottom:12px;">⚓</div>
          <div style="font-size:13px; color:#8a8a7a; font-family:'DM Sans',sans-serif;">
          No incidents yet. Use the crew device to report a guest concern.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sev_html = {
            'urgent': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#fff1f0;color:#cf1322;font-size:10px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;border:1px solid #ffa39e;font-family:\'DM Sans\',sans-serif;">URGENT</span>',
            'high': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#fff7e6;color:#d46b08;font-size:10px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;border:1px solid #ffd591;font-family:\'DM Sans\',sans-serif;">HIGH</span>',
            'medium': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#e6f7ff;color:#0958d9;font-size:10px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;border:1px solid #91caff;font-family:\'DM Sans\',sans-serif;">MEDIUM</span>',
            'low': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#f6ffed;color:#389e0d;font-size:10px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;border:1px solid #b7eb8f;font-family:\'DM Sans\',sans-serif;">LOW</span>',
        }

        for idx, inc in enumerate(st.session_state.incidents):
            sev = inc['severity']
            status = inc['status']

            status_html = {
                'open': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#f0f0f0;color:#595959;font-size:10px;font-weight:500;border:1px solid #d9d9d9;font-family:\'DM Sans\',sans-serif;">Open</span>',
                'in progress': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#e6f4ff;color:#0958d9;font-size:10px;font-weight:500;border:1px solid #91caff;font-family:\'DM Sans\',sans-serif;">In Progress</span>',
                'resolved': '<span style="display:inline-block;padding:3px 10px;border-radius:20px;background:#f6ffed;color:#389e0d;font-size:10px;font-weight:500;border:1px solid #b7eb8f;font-family:\'DM Sans\',sans-serif;">Resolved</span>',
            }.get(status, '')

            bg = "#fffbe6" if idx == 0 and st.session_state.incident_created else "#fff"

            st.markdown(f"""
            <div style="background:{bg}; padding:13px 20px; display:grid; 
            grid-template-columns:90px 70px 1fr 95px 150px 110px 110px; gap:10px;
            border-bottom:1px solid #f0ece4; align-items:center; 
            font-family:'DM Sans',sans-serif; transition:background 0.5s;">
              <div style="font-size:11px; font-weight:600; color:#1a2744;">{inc['id']}</div>
              <div style="font-size:13px; font-weight:600; color:#1a2744;">{inc['cabin']}</div>
              <div style="font-size:12px; color:#4a5568; line-height:1.4;">{inc['summary']}</div>
              <div>{sev_html.get(sev, '')}</div>
              <div style="font-size:11px; color:#1a2744; font-weight:500;">{inc['department']}</div>
              <div>{status_html}</div>
              <div style="font-size:10px; color:#8a8a7a;">{inc['time']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            bcol1, bcol2, bcol3 = st.columns([1, 1, 2])
            with bcol1:
                if inc['status'] != 'resolved':
                    if st.button("In Progress", key=f"prog_{idx}", use_container_width=True):
                        st.session_state.incidents[idx]['status'] = 'in progress'
                        st.rerun()
            with bcol2:
                if inc['status'] != 'resolved':
                    if st.button("✓ Resolve", key=f"res_{idx}", use_container_width=True):
                        st.session_state.incidents[idx]['status'] = 'resolved'
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

