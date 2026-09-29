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
# PREMIUM UI
# -------------------------------------------------------------------
st.markdown("""
<style>
:root {
    --ink: #12211d;
    --muted: #68756f;
    --primary: #0d766e;
    --primary-dark: #075a54;
    --mint: #dff5ed;
    --coral: #ef785f;
    --sun: #f3c45d;
    --paper: #fbfcfa;
    --surface: #ffffff;
    --line: #dce5e0;
    --success: #23845e;
    --shadow-sm: 0 8px 24px rgba(18,33,29,.07);
    --shadow-lg: 0 24px 70px rgba(18,33,29,.14);
}

html, body, [class*="css"] {
    font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background: var(--paper);
    color: var(--ink);
}

.block-container {
    max-width: 1240px;
    padding: 1rem 2rem 4rem;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.app-nav {
    height: 62px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1rem;
}
.brand { display: flex; align-items: center; gap: .7rem; color: var(--ink); }
.brand-mark {
    width: 34px; height: 34px; border-radius: 10px; display: grid; place-items: center;
    color: white; background: var(--primary); box-shadow: 0 7px 16px rgba(13,118,110,.2);
}
.brand-name { font-size: .98rem; font-weight: 800; }
.brand-sub { color: var(--muted); font-size: .68rem; font-weight: 600; }
.nav-status { color: var(--primary-dark); font-size: .72rem; font-weight: 800; display:flex; align-items:center; gap:.4rem; }
.nav-dot { width:7px; height:7px; border-radius:50%; background:var(--success); box-shadow:0 0 0 4px var(--mint); }

.hero {
    position: relative;
    overflow: hidden;
    min-height: 350px;
    padding: 3.25rem;
    border-radius: 18px;
    margin-bottom: 1.25rem;
    color: white;
    background: linear-gradient(120deg, #102c26 0%, #0d514a 54%, #167f76 100%);
    box-shadow: var(--shadow-lg);
}
.hero:before {
    content: ""; position:absolute; inset:0 0 0 52%; opacity:.24;
    background-image: linear-gradient(rgba(255,255,255,.18) 1px, transparent 1px), linear-gradient(90deg,rgba(255,255,255,.18) 1px,transparent 1px);
    background-size: 34px 34px; transform: skewX(-8deg) scale(1.12);
}
.hero:after {
    content: "✈"; position:absolute; right:7%; top:50%; transform:translateY(-50%) rotate(-9deg);
    font-size:10rem; line-height:1; color:rgba(255,255,255,.13);
}
.eyebrow {
    position:relative; z-index:1; display:inline-flex; align-items:center; gap:.45rem;
    color:#c8f6e7; font-size:.7rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase;
}
.hero h1 {
    position:relative; z-index:1; font-size:clamp(2.6rem,5vw,4.6rem); line-height:1.02;
    letter-spacing:0; margin:1rem 0 .9rem; max-width:720px; font-weight:800;
}
.hero p { position:relative; z-index:1; color:#d5e8e2; font-size:1.04rem; max-width:600px; margin:0; line-height:1.65; }
.hero-proof { position:relative; z-index:1; display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.5rem; }
.hero-proof span { border:1px solid rgba(255,255,255,.2); background:rgba(255,255,255,.08); padding:.4rem .65rem; border-radius:8px; font-size:.72rem; font-weight:700; }

.search-panel {
    background: var(--surface); border:1px solid var(--line); border-radius:14px;
    padding:1rem 1.15rem .5rem; box-shadow:var(--shadow-sm); margin-bottom:.4rem;
}
.search-label { color:var(--ink); font-weight:800; font-size:.86rem; margin-bottom:.25rem; }
div[data-testid="stTextInput"] label { display:none; }
div[data-testid="stTextInput"] input {
    min-height:52px !important; border:1px solid var(--line) !important; border-radius:9px !important;
    background:#f8faf9 !important; color:var(--ink) !important; font-size:.95rem !important;
}
div[data-testid="stTextInput"] input:focus { border-color:var(--primary) !important; box-shadow:0 0 0 3px rgba(13,118,110,.12) !important; }
div.stButton > button {
    min-height:52px !important; border-radius:9px !important; border:0 !important;
    color:white !important; background:var(--primary) !important; font-weight:800 !important;
    box-shadow:0 9px 18px rgba(13,118,110,.18); transition:transform .16s ease, background .16s ease;
}
div.stButton > button:hover { background:var(--primary-dark) !important; transform:translateY(-1px); }
.helper { color:var(--muted); font-size:.76rem; margin:.25rem 0 1rem; }

.section-kicker { color:var(--primary); font-size:.68rem; font-weight:900; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.3rem; }
.section-title { font-size:1.5rem; font-weight:800; letter-spacing:0; color:var(--ink); margin:0 0 1rem; }
.destination {
    display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1.15rem 1.3rem;
    background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--coral);
    border-radius:12px; margin:1.8rem 0 1rem; box-shadow:var(--shadow-sm);
}
.destination-name { font-size:1.4rem; font-weight:800; color:var(--ink); }
.destination-sub { color:var(--muted); font-size:.82rem; margin-top:.15rem; }
.live-pill { background:var(--mint); color:var(--primary-dark); border-radius:7px; padding:.45rem .65rem; font-size:.68rem; font-weight:900; white-space:nowrap; }
.summary-card { background:var(--surface); border:1px solid var(--line); border-top:3px solid var(--primary); border-radius:12px; padding:1.35rem 1.5rem; box-shadow:var(--shadow-sm); line-height:1.72; color:#34443e; }
.summary-card strong { color:var(--ink); }

.agent-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:.7rem; margin:.8rem 0 1.7rem; }
.agent-card { background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:.9rem; box-shadow:0 5px 16px rgba(18,33,29,.04); }
.agent-icon { width:36px; height:36px; border-radius:9px; display:flex; align-items:center; justify-content:center; background:var(--mint); margin-bottom:.55rem; font-size:1.05rem; }
.agent-name { font-weight:800; font-size:.82rem; color:var(--ink); }
.agent-status { color:var(--success); font-size:.68rem; font-weight:700; margin-top:.18rem; }

button[data-baseweb="tab"] { font-weight:800 !important; color:var(--muted) !important; padding:.85rem 1rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--primary-dark) !important; }
div[data-baseweb="tab-highlight"] { background-color:var(--primary) !important; }
.result-surface { background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:1.4rem 1.5rem; box-shadow:var(--shadow-sm); line-height:1.68; }
.result-surface a { color:var(--primary-dark); font-weight:700; }
.result-surface h1,.result-surface h2,.result-surface h3 { color:var(--ink); }

.weather-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:.55rem; margin-bottom:1rem; }
.weather-card { text-align:center; background:#f7faf8; border:1px solid var(--line); border-radius:10px; padding:.85rem .45rem; }
.weather-day { color:var(--muted); font-size:.66rem; font-weight:800; text-transform:uppercase; }
.weather-icon { font-size:1.45rem; margin:.3rem 0; }
.weather-high { font-weight:800; color:var(--ink); }
.weather-low { color:var(--muted); font-size:.76rem; }
.weather-rain { color:var(--primary-dark); font-size:.67rem; margin-top:.25rem; }
.agent-running { border-radius:9px !important; }
.footer { border-top:1px solid var(--line); margin-top:2.5rem; padding-top:1.2rem; color:var(--muted); font-size:.72rem; line-height:1.6; }

@media (max-width:800px) {
    .block-container { padding: .6rem 1rem 3rem; }
    .hero { min-height:330px; padding:2rem 1.35rem; }
    .hero:before { inset:60% 0 0 0; }
    .hero:after { right:4%; top:auto; bottom:-1rem; transform:rotate(-9deg); font-size:7rem; }
    .hero h1 { font-size:2.65rem; }
    .hero p { font-size:.95rem; }
    .nav-status { display:none; }
    .agent-grid { grid-template-columns:repeat(2,1fr); }
    .weather-grid { grid-template-columns:repeat(2,1fr); }
    .destination { align-items:flex-start; flex-direction:column; }
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
<nav class="app-nav">
    <div class="brand">
        <div class="brand-mark">✈</div>
        <div><div class="brand-name">Travel Companion</div><div class="brand-sub">AI trip intelligence</div></div>
    </div>
    <div class="nav-status"><span class="nav-dot"></span> Research team online</div>
</nav>
<section class="hero">
    <div class="eyebrow">✦ AI-POWERED TRAVEL INTELLIGENCE</div>
    <h1>Know your destination<br>before you arrive.</h1>
    <p>One reliable briefing for stays, weather, food, safety and entry requirements—researched in parallel by specialist travel agents.</p>
    <div class="hero-proof">
        <span>5 specialist agents</span><span>Current sources</span><span>One clear briefing</span>
    </div>
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
    '<div class="helper">Enter a city and country to start your personalized destination briefing.</div>',
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
                text = f'<div class="agent-running" style="background:#e8f7f1;border-color:#cdebe0;color:#187a57;">✓ &nbsp; {icon} {agent_name} complete</div>'
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
    <strong>Travel Companion AI</strong> · Multi-agent travel research assistant<br>
    Research can change quickly. Always verify visa, medical, security, weather and booking
    information with the relevant official or provider source before making travel decisions.
</div>
""", unsafe_allow_html=True)
