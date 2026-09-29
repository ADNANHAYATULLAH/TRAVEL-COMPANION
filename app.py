import os
import re
import html
import streamlit as st

from travel_crew import run_travel_research

st.set_page_config(
    page_title="Travel Companion AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------------------------
# PRISMATIC GLASS UI
# -------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap');

:root {
    --ink: #334155;
    --ink-strong: #0f172a;
    --muted: #64748b;
    --cyan: #22d3ee;
    --violet: #8b5cf6;
    --rose: #f472b6;
    --amber: #fbbf24;
    --emerald: #10b981;
    --glass: rgba(255,255,255,.76);
    --line: rgba(255,255,255,.72);
    --soft-line: rgba(100,116,139,.15);
}

html, body, [class*="css"] { font-family: "DM Sans", sans-serif; }
.stApp {
    color: var(--ink);
    background:
      radial-gradient(circle at 4% 2%, rgba(34,211,238,.28), transparent 25rem),
      radial-gradient(circle at 96% 12%, rgba(167,139,250,.27), transparent 27rem),
      radial-gradient(circle at 16% 92%, rgba(244,114,182,.22), transparent 25rem),
      radial-gradient(circle at 90% 76%, rgba(251,191,36,.24), transparent 23rem),
      #f1f5f9;
    background-attachment: fixed;
}
.block-container { max-width: 1180px; padding-top: 1.2rem; padding-bottom: 4rem; }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.hero, .search-panel, .destination, .summary-card, .agent-card, .result-surface,
div[data-testid="stStatusWidget"], div[data-baseweb="tab-list"] {
    background: linear-gradient(150deg, rgba(255,255,255,.86), rgba(241,245,249,.96) 55%, rgba(238,242,255,.92));
    border: 1px solid var(--line);
    box-shadow: 0 18px 42px -24px rgba(71,85,105,.55), inset 0 1px 0 rgba(255,255,255,.9);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

.hero { position:relative; overflow:hidden; min-height:255px; padding:2.5rem 2.7rem; border-radius:24px; margin-bottom:1rem; }
.hero::before { content:""; position:absolute; inset:0; padding:1px; border-radius:inherit; background:linear-gradient(115deg,var(--cyan),var(--violet),var(--rose),var(--amber)); -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude; opacity:.6; pointer-events:none; }
.hero::after { content:"✈"; position:absolute; right:4%; bottom:-3.8rem; font-size:13rem; color:rgba(139,92,246,.07); transform:rotate(-12deg); }
.eyebrow { position:relative; z-index:1; display:inline-flex; align-items:center; padding:.42rem .75rem; border-radius:999px; background:rgba(16,185,129,.1); color:#047857; font-size:.7rem; font-weight:700; letter-spacing:.15em; }
.hero h1 { position:relative; z-index:1; font-family:"Fraunces",serif; font-size:clamp(2.5rem,5vw,4.5rem); font-weight:500; line-height:1.02; letter-spacing:0; color:var(--ink-strong); margin:.85rem 0 .65rem; max-width:760px; }
.hero p { position:relative; z-index:1; color:var(--muted); font-size:1rem; max-width:620px; margin:0; line-height:1.7; }

.search-panel { position:relative; z-index:5; margin-top:-2rem; padding:1.1rem 1.2rem 1.2rem; border-radius:22px; }
.search-panel::before, .destination::before, .summary-card::before, .result-surface::before { content:""; position:absolute; inset:0; padding:1px; border-radius:inherit; background:linear-gradient(115deg,var(--cyan),var(--violet),var(--rose),var(--amber)); -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude; opacity:.38; pointer-events:none; }
.search-label { color:var(--ink-strong); font-family:"Fraunces",serif; font-size:1.2rem; margin-bottom:.45rem; }
div[data-testid="stTextInput"] label { display:none; }
div[data-testid="stTextInput"] input { background:rgba(255,255,255,.72)!important; border:1px solid rgba(148,163,184,.25)!important; border-radius:999px!important; min-height:50px!important; color:var(--ink-strong)!important; font-size:.95rem!important; padding-left:1.15rem!important; }
div[data-testid="stTextInput"] input:focus { border-color:rgba(139,92,246,.6)!important; box-shadow:0 0 0 3px rgba(139,92,246,.1)!important; }
div.stButton > button { min-height:50px!important; border:0!important; border-radius:999px!important; color:#fff!important; font-weight:700!important; background:linear-gradient(135deg,#22d3ee,#8b5cf6 52%,#f472b6)!important; box-shadow:0 12px 24px -12px rgba(139,92,246,.65)!important; transition:transform .16s ease,box-shadow .16s ease!important; }
div.stButton > button:hover { transform:translateY(-1px); box-shadow:0 15px 30px -12px rgba(139,92,246,.75)!important; }
.helper { color:var(--muted); font-size:.75rem; margin-top:.55rem; }

.section-kicker { color:#7c3aed; font-size:.68rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-bottom:.3rem; }
.section-title { font-family:"Fraunces",serif; font-size:1.65rem; font-weight:500; letter-spacing:0; color:var(--ink-strong); margin:0 0 .9rem; }
.destination { position:relative; display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1.2rem 1.35rem; border-radius:22px; margin:1.5rem 0 1rem; }
.destination-name { font-family:"Fraunces",serif; font-size:1.65rem; font-weight:500; color:var(--ink-strong); }
.destination-sub { color:var(--muted); font-size:.8rem; margin-top:.15rem; }
.live-pill { display:inline-flex; align-items:center; background:rgba(16,185,129,.11); color:#047857; border-radius:999px; padding:.45rem .72rem; font-size:.68rem; font-weight:700; white-space:nowrap; }
.summary-card { position:relative; border-radius:22px; padding:1.35rem 1.45rem; line-height:1.72; color:#475569; }
.summary-card strong { color:var(--ink-strong); }

.agent-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:.7rem; margin:.75rem 0 1.5rem; }
.agent-card { border-radius:18px; padding:.9rem; }
.agent-icon { width:36px; height:36px; border-radius:12px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,rgba(34,211,238,.16),rgba(139,92,246,.15)); margin-bottom:.55rem; font-size:1rem; }
.agent-name { font-weight:700; font-size:.8rem; color:var(--ink-strong); }
.agent-status { color:#059669; font-size:.68rem; font-weight:600; margin-top:.18rem; }
.agent-running { border:1px solid rgba(139,92,246,.18); border-radius:14px; padding:.85rem 1rem; background:rgba(255,255,255,.7); color:#6d28d9; font-weight:600; }

/* Button-like report tabs */
div[data-baseweb="tab-list"] { gap:.35rem; padding:.35rem; border-radius:999px; overflow-x:auto; }
button[data-baseweb="tab"] { flex:1 0 auto; min-height:42px; border-radius:999px!important; padding:.65rem .9rem!important; color:var(--muted)!important; font-weight:600!important; font-size:.82rem!important; transition:background .15s ease,color .15s ease!important; }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--ink-strong)!important; background:rgba(255,255,255,.88)!important; box-shadow:0 8px 18px -12px rgba(71,85,105,.55); }
div[data-baseweb="tab-highlight"] { display:none; }

.result-surface { position:relative; border-radius:22px; padding:1.35rem 1.45rem; line-height:1.7; color:#475569; }
.result-surface a { color:#7c3aed; font-weight:600; }
.result-surface h1,.result-surface h2,.result-surface h3 { font-family:"Fraunces",serif; color:var(--ink-strong); letter-spacing:0; }
.weather-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:.55rem; margin-bottom:1rem; }
.weather-card { text-align:center; background:rgba(255,255,255,.7); border:1px solid rgba(148,163,184,.16); border-radius:16px; padding:.8rem .4rem; box-shadow:inset 0 1px 0 #fff; }
.weather-day { color:var(--muted); font-size:.66rem; font-weight:700; text-transform:uppercase; }
.weather-icon { font-size:1.35rem; margin:.25rem 0; }
.weather-high { font-weight:700; color:var(--ink-strong); }
.weather-low { color:var(--muted); font-size:.76rem; }
.weather-rain { color:#0891b2; font-size:.66rem; margin-top:.22rem; }
.footer { border-top:1px solid rgba(148,163,184,.2); margin-top:2.5rem; padding-top:1.15rem; color:#94a3b8; font-size:.72rem; line-height:1.6; text-align:center; }

@media (max-width:800px) {
  .block-container { padding:.75rem .75rem 2.5rem; }
  .hero { padding:1.7rem 1.25rem; min-height:255px; border-radius:22px; }
  .hero h1 { font-size:2.55rem; }
  .search-panel { margin-top:-1.25rem; }
  .agent-grid { grid-template-columns:repeat(2,1fr); }
  .weather-grid { display:flex; overflow-x:auto; padding-bottom:.35rem; }
  .weather-card { min-width:76px; }
  .destination { align-items:flex-start; flex-direction:column; }
}
@media (prefers-reduced-motion:no-preference) {
  .hero,.search-panel,.destination,.summary-card,.agent-card,.result-surface { animation:rise .45s ease both; }
  @keyframes rise { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# STATE
# -------------------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "searched_country" not in st.session_state:
    st.session_state.searched_country = ""
if "searched_city" not in st.session_state:
    st.session_state.searched_city = ""

# -------------------------------------------------------------------
# HERO
# -------------------------------------------------------------------
st.markdown("""
<section class="hero">
    <div class="eyebrow">● FIVE SPECIALISTS ONLINE</div>
    <h1>Your journey,<br>clearly researched.</h1>
    <p>
        A refined travel research desk for hotels, weather, dining, safety and entry requirements.
    </p>
</section>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SEARCH
# -------------------------------------------------------------------
st.markdown('<div class="search-panel">', unsafe_allow_html=True)
st.markdown('<div class="search-label">Where are you going?</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.15, 1.15, .72], gap="small")
with c1:
    country = st.text_input(
        "Country",
        placeholder="Country — e.g. Kazakhstan",
        key="country_input",
        label_visibility="collapsed",
    )
with c2:
    city = st.text_input(
        "City",
        placeholder="City — e.g. Almaty",
        key="city_input",
        label_visibility="collapsed",
    )
with c3:
    search = st.button("✈  Plan my trip", use_container_width=True)

st.markdown(
    '<div class="helper">Five research specialists • current web sources • one concise AI briefing</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# RESEARCH
# -------------------------------------------------------------------
if search:
    if not country.strip() or not city.strip():
        st.warning("Please enter both a country and city.")
    elif not os.getenv("GROQ_API_KEY") and "GROQ_API_KEY" not in st.secrets:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets.")
    else:
        if "GROQ_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

        st.session_state.results = None
        st.session_state.searched_country = country.strip()
        st.session_state.searched_city = city.strip()

        status_box = st.empty()

        icons = {
            "Hotel": "🏨",
            "Weather": "☀️",
            "Restaurant": "🍽️",
            "Safety & Health": "🛡️",
            "Immigration": "🛂",
            "Travel Manager": "✦",
        }

        def update_status(agent_name, state):
            icon = icons.get(agent_name, "●")
            if state == "working":
                text = f'<div class="agent-running">◌ &nbsp; {icon} {agent_name} is researching...</div>'
            else:
                text = f'<div class="agent-running" style="background:#e9f7f2;border-color:#cdebe0;color:#187a57;">✓ &nbsp; {icon} {agent_name} complete</div>'
            status_box.markdown(text, unsafe_allow_html=True)

        try:
            with st.status("✦  Researching your destination...", expanded=True) as overall:
                results = run_travel_research(
                    country.strip(),
                    city.strip(),
                    update_status,
                )
                overall.update(
                    label="✓  Your travel intelligence is ready",
                    state="complete",
                    expanded=False,
                )

            st.session_state.results = results
            st.toast("Travel research completed", icon="✈️")

        except Exception as exc:
            st.error(f"The research team could not complete the trip search: {exc}")

# -------------------------------------------------------------------
# RESULTS
# -------------------------------------------------------------------
results = st.session_state.results

if results:
    country_name = st.session_state.searched_country
    city_name = st.session_state.searched_city

    st.markdown(
        f"""
        <div class="destination">
            <div>
                <div class="section-kicker">YOUR DESTINATION</div>
                <div class="destination-name">📍 {html.escape(city_name)}, {html.escape(country_name)}</div>
                <div class="destination-sub">Travel intelligence gathered from current research sources</div>
            </div>
            <div class="live-pill">● RESEARCH COMPLETE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Research team overview
    agent_data = [
        ("🏨", "Hotels"),
        ("☀️", "Weather"),
        ("🍽️", "Dining"),
        ("🛡️", "Safety"),
        ("🛂", "Entry"),
    ]
    cards = '<div class="agent-grid">'
    for icon, name in agent_data:
        cards += f"""
        <div class="agent-card">
            <div class="agent-icon">{icon}</div>
            <div class="agent-name">{name}</div>
            <div class="agent-status">✓ Research ready</div>
        </div>
        """
    cards += "</div>"
    st.markdown(cards, unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">TRAVEL MANAGER</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your travel briefing</div>', unsafe_allow_html=True)

    overview = results.get("Overview", "")
    if overview:
        # Preserve URLs and line breaks while keeping the result inside a clean surface.
        safe_overview = html.escape(str(overview)).replace("\n", "<br>")
        st.markdown(
            f'<div class="summary-card">{safe_overview}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs([
        "🏨  Hotels",
        "☀️  Weather",
        "🍽️  Restaurants",
        "🛡️  Safety & Health",
        "🛂  Immigration",
    ])

    mapping = [
        ("Hotel", 0),
        ("Weather", 1),
        ("Restaurant", 2),
        ("Safety & Health", 3),
        ("Immigration", 4),
    ]

    for key, index in mapping:
        with tabs[index]:
            title_map = {
                "Hotel": ("HOTEL RESEARCH", "Places to stay and useful booking information"),
                "Weather": ("7-DAY FORECAST", "A compact view of the upcoming weather"),
                "Restaurant": ("DINING RESEARCH", "Halal and other restaurant options"),
                "Safety & Health": ("SAFETY & HEALTH", "Current travel, security and health research"),
                "Immigration": ("ENTRY REQUIREMENTS", "Visa and immigration information to verify"),
            }
            kicker, subtitle = title_map[key]
            st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-title">{subtitle}</div>', unsafe_allow_html=True)

            value = str(results.get(key, "No result returned."))

            # Render the weather report as visual cards.
            if key == "Weather":
                lines = [x.strip() for x in value.splitlines() if ":" in x and "High " in x]
                if lines:
                    cards_html = '<div class="weather-grid">'
                    for line in lines[:7]:
                        try:
                            date, rest = line.split(":", 1)
                            condition = rest.split("|")[0].strip()
                            high = re.search(r"High\s+([-\d.]+)°C", rest)
                            low = re.search(r"Low\s+([-\d.]+)°C", rest)
                            rain = re.search(r"Rain\s+([\d.]+)%", rest)
                            icons_weather = {
                                "Clear": "☀️", "Mainly clear": "🌤️",
                                "Partly cloudy": "⛅", "Overcast": "☁️",
                                "Fog": "🌫️", "Rime fog": "🌫️",
                                "Light drizzle": "🌦️", "Drizzle": "🌦️",
                                "Heavy drizzle": "🌧️", "Light rain": "🌦️",
                                "Rain": "🌧️", "Heavy rain": "🌧️",
                                "Light snow": "🌨️", "Snow": "❄️",
                                "Heavy snow": "❄️", "Rain showers": "🌦️",
                                "Heavy rain showers": "🌧️", "Thunderstorm": "⛈️",
                                "Thunderstorm with hail": "⛈️",
                            }
                            icon = icons_weather.get(condition, "🌤️")
                            day = date[-5:] if len(date) >= 5 else date
                            cards_html += f"""
                            <div class="weather-card">
                                <div class="weather-day">{html.escape(day)}</div>
                                <div class="weather-icon">{icon}</div>
                                <div class="weather-high">{high.group(1) if high else "—"}°</div>
                                <div class="weather-low">{low.group(1) if low else "—"}°</div>
                                <div class="weather-rain">💧 {rain.group(1) if rain else "—"}%</div>
                            </div>
                            """
                        except Exception:
                            continue
                    cards_html += "</div>"
                    st.markdown(cards_html, unsafe_allow_html=True)

            # Convert plain URLs to clickable links and preserve readable line breaks.
            escaped = html.escape(value)
            escaped = re.sub(
                r'(https?://[^\s<]+)',
                r'<a href="\1" target="_blank">\1</a>',
                escaped,
            )
            escaped = escaped.replace("\n\n", "<br><br>").replace("\n", "<br>")

            st.markdown(
                f'<div class="result-surface">{escaped}</div>',
                unsafe_allow_html=True,
            )

            st.caption("Verify time-sensitive details with the linked official source before booking or travelling.")

# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------
st.markdown("""
<div class="footer">
    <strong>Travel Companion AI</strong> · Prismatic travel research desk<br>
    Research can change quickly. Always verify visa, medical, security, weather and booking
    information with the relevant official or provider source before making travel decisions.
</div>
""", unsafe_allow_html=True)
