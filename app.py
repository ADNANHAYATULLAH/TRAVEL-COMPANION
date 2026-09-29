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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --navy: #071827;
    --navy-2: #0b2435;
    --ink: #10202d;
    --muted: #647484;
    --teal: #0e9f9a;
    --teal-dark: #087a78;
    --sky: #3aa6d8;
    --sand: #f4efe5;
    --cream: #fbfaf7;
    --line: #e3e9ed;
    --success: #198754;
    --warning: #c98216;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 7% 0%, rgba(58,166,216,.12), transparent 28%),
        radial-gradient(circle at 93% 12%, rgba(14,159,154,.10), transparent 25%),
        #f5f7f8;
    color: var(--ink);
}

.block-container {
    max-width: 1220px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit chrome that makes the app feel like a prototype */
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 330px;
    padding: 2.8rem 3rem;
    border-radius: 30px;
    margin-bottom: 1.3rem;
    color: white;
    background:
        radial-gradient(circle at 82% 20%, rgba(79,209,197,.30), transparent 24%),
        radial-gradient(circle at 70% 90%, rgba(58,166,216,.24), transparent 30%),
        linear-gradient(135deg, #071827 0%, #0b2c40 52%, #0d4652 100%);
    box-shadow: 0 22px 55px rgba(7,24,39,.18);
}

.hero:after {
    content: "✈";
    position: absolute;
    right: 5%;
    bottom: -34px;
    font-size: 15rem;
    line-height: 1;
    color: rgba(255,255,255,.045);
    transform: rotate(-10deg);
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .38rem .72rem;
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 999px;
    background: rgba(255,255,255,.08);
    color: #bcebe8;
    font-size: .74rem;
    font-weight: 800;
    letter-spacing: .12em;
}

.hero h1 {
    position: relative;
    z-index: 1;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(2.25rem, 5vw, 4.15rem);
    line-height: 1.02;
    letter-spacing: -.055em;
    margin: 1rem 0 .8rem;
    max-width: 760px;
}

.hero p {
    position: relative;
    z-index: 1;
    color: #c7d9e2;
    font-size: 1.05rem;
    max-width: 620px;
    margin: 0;
    line-height: 1.7;
}

/* Search panel */
.search-panel {
    margin-top: -2.5rem;
    position: relative;
    z-index: 5;
    background: rgba(255,255,255,.96);
    border: 1px solid rgba(16,32,45,.08);
    border-radius: 22px;
    padding: 1.15rem 1.25rem 1.25rem;
    box-shadow: 0 18px 45px rgba(16,32,45,.12);
}

.search-label {
    color: var(--ink);
    font-weight: 800;
    font-size: .88rem;
    margin-bottom: .35rem;
}

div[data-testid="stTextInput"] label {
    display: none;
}

div[data-testid="stTextInput"] input {
    background: #f7f9fa !important;
    border: 1px solid #dce4e8 !important;
    border-radius: 13px !important;
    min-height: 50px !important;
    color: var(--ink) !important;
    font-size: 1rem !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(14,159,154,.12) !important;
}

div.stButton > button {
    border-radius: 13px !important;
    min-height: 50px !important;
    font-weight: 800 !important;
    border: 0 !important;
    background: linear-gradient(135deg, var(--teal), #087f88) !important;
    color: white !important;
    box-shadow: 0 9px 20px rgba(14,159,154,.20);
    transition: transform .15s ease, box-shadow .15s ease;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 25px rgba(14,159,154,.28);
}

.helper {
    color: var(--muted);
    font-size: .78rem;
    margin-top: .65rem;
}

/* Section headings */
.section-kicker {
    color: var(--teal-dark);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: .35rem;
}

.section-title {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -.035em;
    color: var(--ink);
    margin: 0 0 1rem;
}

/* Destination strip */
.destination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 1.2rem 1.35rem;
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    margin: 1.8rem 0 1rem;
    box-shadow: 0 8px 25px rgba(16,32,45,.05);
}

.destination-name {
    font-family: "Plus Jakarta Sans";
    font-size: 1.45rem;
    font-weight: 800;
    color: var(--ink);
}

.destination-sub {
    color: var(--muted);
    font-size: .84rem;
    margin-top: .15rem;
}

.live-pill {
    background: #e7f7f4;
    color: #087a78;
    border-radius: 999px;
    padding: .45rem .72rem;
    font-size: .75rem;
    font-weight: 800;
    white-space: nowrap;
}

/* Summary card */
.summary-card {
    background: linear-gradient(135deg, #ffffff, #f3fbfa);
    border: 1px solid #d9ece9;
    border-radius: 22px;
    padding: 1.45rem 1.55rem;
    box-shadow: 0 10px 30px rgba(16,32,45,.06);
    line-height: 1.72;
    color: #2b3c48;
}

.summary-card strong { color: var(--ink); }

/* Agent cards */
.agent-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: .7rem;
    margin: .8rem 0 1.6rem;
}

.agent-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: .9rem;
    box-shadow: 0 7px 20px rgba(16,32,45,.045);
}

.agent-icon {
    width: 36px;
    height: 36px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e8f7f5;
    margin-bottom: .55rem;
    font-size: 1.05rem;
}

.agent-name {
    font-weight: 800;
    font-size: .82rem;
    color: var(--ink);
}

.agent-status {
    color: var(--success);
    font-size: .7rem;
    font-weight: 700;
    margin-top: .18rem;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 800 !important;
    color: #687985 !important;
    padding: .85rem 1rem !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--teal-dark) !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: var(--teal) !important;
}

/* Result surface */
.result-surface {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1.35rem 1.45rem;
    box-shadow: 0 8px 25px rgba(16,32,45,.045);
    line-height: 1.65;
}

.result-surface a {
    color: var(--teal-dark);
    font-weight: 700;
}

.result-surface h1, .result-surface h2, .result-surface h3 {
    font-family: "Plus Jakarta Sans";
    color: var(--ink);
}

/* Weather cards */
.weather-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: .55rem;
    margin-bottom: 1rem;
}

.weather-card {
    text-align: center;
    background: #f7fbfc;
    border: 1px solid #e1edf0;
    border-radius: 15px;
    padding: .85rem .45rem;
}

.weather-day {
    color: var(--muted);
    font-size: .68rem;
    font-weight: 800;
    text-transform: uppercase;
}

.weather-icon { font-size: 1.45rem; margin: .3rem 0; }
.weather-high { font-weight: 800; color: var(--ink); }
.weather-low { color: var(--muted); font-size: .78rem; }
.weather-rain { color: var(--teal-dark); font-size: .68rem; margin-top: .25rem; }

/* Footer */
.footer {
    border-top: 1px solid #dfe6e9;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    color: #7b8a94;
    font-size: .75rem;
    line-height: 1.6;
}

/* Mobile */
@media (max-width: 800px) {
    .hero { padding: 2rem 1.35rem; min-height: 285px; }
    .hero h1 { font-size: 2.35rem; }
    .search-panel { margin-top: -1.3rem; }
    .agent-grid { grid-template-columns: repeat(2, 1fr); }
    .weather-grid { grid-template-columns: repeat(2, 1fr); }
    .destination { align-items: flex-start; flex-direction: column; }
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
    <div class="eyebrow">✦ AI-POWERED TRAVEL INTELLIGENCE</div>
    <h1>Travel smarter.<br>Arrive prepared.</h1>
    <p>
        Research hotels, weather, restaurants, safety and entry requirements
        in one focused travel briefing.
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
    <strong>Travel Companion AI</strong> · Multi-agent travel research assistant<br>
    Research can change quickly. Always verify visa, medical, security, weather and booking
    information with the relevant official or provider source before making travel decisions.
</div>
""", unsafe_allow_html=True)
