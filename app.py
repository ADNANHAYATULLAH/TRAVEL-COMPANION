import os
import html
import streamlit as st

from travel_crew import run_travel_research

st.set_page_config(
    page_title="Travel Companion AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --ink: #10233f;
    --muted: #63738a;
    --navy: #0b1f3a;
    --teal: #08a6a6;
    --teal-dark: #087f83;
    --sky: #e9f8fb;
    --cream: #f7f5ef;
    --white: #ffffff;
    --line: #dce5ec;
    --success: #16865b;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 7% 0%, rgba(8,166,166,.13), transparent 26%),
        radial-gradient(circle at 94% 7%, rgba(50,130,210,.11), transparent 24%),
        linear-gradient(180deg, #f8fbfc 0%, #f4f7f8 55%, #eef3f5 100%);
    color: var(--ink);
}

.block-container {
    max-width: 1240px;
    padding-top: 1.1rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit chrome that makes the app feel like a prototype. */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

/* Top brand bar */
.brandbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding: .2rem .1rem;
}
.brand {
    display: flex;
    align-items: center;
    gap: .75rem;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-weight: 800;
    font-size: 1.02rem;
    color: var(--navy);
}
.brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background: var(--navy);
    color: white;
    box-shadow: 0 8px 20px rgba(11,31,58,.18);
}
.brand-tag {
    color: #5f7084;
    font-size: .78rem;
    font-weight: 600;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 30px;
    min-height: 330px;
    padding: 3rem 3.2rem;
    background:
        radial-gradient(circle at 82% 30%, rgba(67,210,211,.28), transparent 25%),
        radial-gradient(circle at 95% 100%, rgba(42,121,193,.35), transparent 35%),
        linear-gradient(118deg, #09213e 0%, #0b3151 53%, #0a6f79 100%);
    box-shadow: 0 28px 70px rgba(11,31,58,.20);
    margin-bottom: 1.5rem;
}
.hero:after {
    content: "✈";
    position: absolute;
    right: 7%;
    top: 14%;
    font-size: 10rem;
    opacity: .075;
    transform: rotate(-12deg);
}
.hero-content { position: relative; z-index: 2; max-width: 760px; }
.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .45rem .75rem;
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 999px;
    background: rgba(255,255,255,.09);
    color: #bdf4f1;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .12em;
}
.hero h1 {
    margin: 1rem 0 .55rem;
    color: #fff;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: .98;
    letter-spacing: -.055em;
}
.hero h1 span { color: #6ce1dc; }
.hero p {
    margin: 0;
    color: #d5e5ee;
    font-size: 1.05rem;
    max-width: 650px;
    line-height: 1.65;
}
.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    margin-top: 1.5rem;
}
.hero-pill {
    color: #edfafa;
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 999px;
    padding: .42rem .72rem;
    font-size: .78rem;
    font-weight: 600;
}

/* Search panel */
.search-panel {
    margin-top: -2.2rem;
    position: relative;
    z-index: 5;
    background: rgba(255,255,255,.96);
    border: 1px solid rgba(11,31,58,.09);
    border-radius: 24px;
    padding: 1.25rem 1.35rem 1.15rem;
    box-shadow: 0 20px 50px rgba(24,55,79,.12);
    margin-bottom: 1.7rem;
}
.search-label {
    color: var(--navy);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: .8rem;
}

/* Streamlit inputs */
div[data-testid="stTextInput"] label {
    color: #41536b !important;
    font-size: .78rem !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: .06em;
}
div[data-testid="stTextInput"] input {
    height: 52px;
    border: 1px solid #d7e1e8;
    border-radius: 13px;
    background: #f9fbfc;
    color: var(--ink);
    font-size: .98rem;
    box-shadow: none;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(8,166,166,.12) !important;
}

/* Primary CTA */
div.stButton > button[kind="primary"] {
    height: 52px;
    border: 0;
    border-radius: 13px;
    background: linear-gradient(135deg, #0b6e79, #08a6a6);
    color: white;
    font-weight: 800;
    box-shadow: 0 10px 22px rgba(8,166,166,.22);
    transition: transform .15s ease, box-shadow .15s ease;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 28px rgba(8,166,166,.30);
}

/* Research status */
.team-title {
    margin: .2rem 0 .8rem;
    color: var(--navy);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
}
.team-subtitle { color: var(--muted); font-size: .86rem; margin-bottom: 1rem; }
.agent-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: .9rem 1rem;
    box-shadow: 0 7px 22px rgba(29,55,76,.055);
}
.agent-card .top { display:flex; justify-content:space-between; gap:.5rem; }
.agent-name { font-weight: 800; color: var(--navy); font-size: .88rem; }
.agent-state { font-size: .72rem; font-weight: 800; color: var(--success); }
.agent-dot { width:8px; height:8px; border-radius:50%; background:#1db579; display:inline-block; margin-right:.35rem; }

/* Destination heading */
.destination {
    background: var(--navy);
    border-radius: 22px;
    padding: 1.35rem 1.5rem;
    margin: 1.8rem 0 1.15rem;
    color: white;
    box-shadow: 0 18px 38px rgba(11,31,58,.14);
}
.destination-kicker { color:#8edbd8; font-size:.72rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.destination h2 { margin:.25rem 0 0; font-family:"Plus Jakarta Sans"; font-size:1.8rem; color:white; }
.destination p { margin:.25rem 0 0; color:#b9cddd; font-size:.84rem; }

/* Metric cards */
.metric-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1rem 1.05rem;
    min-height: 108px;
    box-shadow: 0 9px 25px rgba(29,55,76,.055);
}
.metric-icon { font-size: 1.35rem; }
.metric-title { margin-top:.35rem; color:#728196; font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
.metric-value { color:var(--navy); font-family:"Plus Jakarta Sans"; font-weight:800; font-size:1.05rem; margin-top:.15rem; }

/* Briefing */
.brief {
    background: linear-gradient(135deg, #e8f8f7, #f7fbfb);
    border: 1px solid #cce8e6;
    border-radius: 22px;
    padding: 1.35rem 1.45rem;
    margin: 1.35rem 0;
    color: #18344b;
    line-height: 1.7;
}
.brief-title { color:#0b6e79; font-family:"Plus Jakarta Sans"; font-weight:800; font-size:1.05rem; margin-bottom:.45rem; }

/* Tabs */
button[data-baseweb="tab"] {
    color: #68788d !important;
    font-weight: 700 !important;
    font-size: .83rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #087f83 !important;
}
div[data-baseweb="tab-highlight"] { background: #08a6a6 !important; }

.result-shell {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 1.35rem 1.45rem;
    margin-top: .8rem;
    box-shadow: 0 10px 28px rgba(29,55,76,.05);
}
.result-heading {
    color: var(--navy);
    font-family:"Plus Jakarta Sans";
    font-weight:800;
    font-size:1.15rem;
    margin-bottom:.7rem;
}

/* Status / alerts */
div[data-testid="stAlert"] { border-radius: 14px; }

.footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #d9e2e8;
    color: #78879a;
    font-size: .75rem;
    line-height: 1.55;
}

@media (max-width: 800px) {
    .block-container { padding-top: .7rem; }
    .hero { padding: 2rem 1.4rem; min-height: 290px; }
    .hero h1 { font-size: 2.65rem; }
    .search-panel { margin-top: -1.3rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# STATE
# -----------------------------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {}

# -----------------------------------------------------------------------------
# HEADER / HERO
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="brandbar">
  <div class="brand"><span class="brand-icon">✈</span> Travel Companion AI</div>
  <div class="brand-tag">AI-POWERED TRAVEL INTELLIGENCE</div>
</div>

<section class="hero">
  <div class="hero-content">
    <div class="eyebrow">✦ MULTI-AGENT TRAVEL RESEARCH</div>
    <h1>Plan less.<br><span>Travel smarter.</span></h1>
    <p>Research your destination with a specialist AI team covering hotels, weather, restaurants, safety, health and immigration.</p>
    <div class="hero-pills">
      <span class="hero-pill">🏨 Hotels</span>
      <span class="hero-pill">☀️ 7-Day Weather</span>
      <span class="hero-pill">🍽️ Dining</span>
      <span class="hero-pill">🛡️ Safety</span>
      <span class="hero-pill">🛂 Immigration</span>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SEARCH
# -----------------------------------------------------------------------------
st.markdown('<div class="search-panel"><div class="search-label">Where are you going?</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, .72], gap="medium", vertical_alignment="bottom")
with c1:
    country = st.text_input("Country", placeholder="e.g. Kazakhstan", label_visibility="visible")
with c2:
    city = st.text_input("City", placeholder="e.g. Almaty", label_visibility="visible")
with c3:
    search = st.button("✦  Plan My Trip", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="small-muted" style="text-align:center;margin-top:-.7rem;margin-bottom:1.2rem;color:#748398;font-size:.78rem;">One search • Five research specialists • One concise travel briefing</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# RUN RESEARCH
# -----------------------------------------------------------------------------
if search:
    if not country.strip() or not city.strip():
        st.warning("Please enter both a country and city.")
    elif not os.getenv("GROQ_API_KEY") and "GROQ_API_KEY" not in st.secrets:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets.")
    else:
        if "GROQ_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

        st.session_state.results = None
        st.session_state.agent_status = {}

        status_box = st.empty()

        def update_status(agent_name, state):
            st.session_state.agent_status[agent_name] = state
            icon = "🟢" if state == "complete" else "🔵"
            label = "Complete" if state == "complete" else "Researching"
            status_box.markdown(
                f'''<div class="agent-card"><div class="top"><span class="agent-name">{icon} {html.escape(agent_name)}</span><span class="agent-state"><span class="agent-dot"></span>{label}</span></div></div>''',
                unsafe_allow_html=True,
            )

        try:
            st.markdown('<div class="team-title">Your research team</div><div class="team-subtitle">Specialists are checking the destination now.</div>', unsafe_allow_html=True)
            with st.status("✦ Researching your destination...", expanded=True) as overall:
                results = run_travel_research(country.strip(), city.strip(), update_status)
                overall.update(label="✓ Research complete", state="complete", expanded=False)
            st.session_state.results = results
            st.success(f"Your travel intelligence for {city.strip()}, {country.strip()} is ready.")
        except Exception as exc:
            st.error(f"The research team could not complete the trip search: {exc}")

# -----------------------------------------------------------------------------
# RESULTS
# -----------------------------------------------------------------------------
results = st.session_state.results

if results:
    destination = f"{city.strip()}, {country.strip()}"

    st.markdown(
        f'''<div class="destination">
            <div class="destination-kicker">YOUR DESTINATION</div>
            <h2>{html.escape(destination)}</h2>
            <p>Fresh travel research collected by your AI specialist team.</p>
        </div>''',
        unsafe_allow_html=True,
    )

    # Overview metric strip
    cards = [
        ("🏨", "Hotels", "Research ready"),
        ("☀️", "Weather", "7-day forecast"),
        ("🍽️", "Restaurants", "Halal + other"),
        ("🛡️", "Safety", "Health + security"),
        ("🛂", "Immigration", "Entry research"),
    ]
    cols = st.columns(5, gap="small")
    for col, (icon, title, value) in zip(cols, cards):
        with col:
            st.markdown(
                f'''<div class="metric-card"><div class="metric-icon">{icon}</div>
                <div class="metric-title">{title}</div><div class="metric-value">{value}</div></div>''',
                unsafe_allow_html=True,
            )

    overview = results.get("Overview", "")
    if overview:
        st.markdown(
            f'<div class="brief"><div class="brief-title">✦ Travel Manager Briefing</div>{overview}</div>',
            unsafe_allow_html=True,
        )

    tabs = st.tabs([
        "🏨  Hotels",
        "☀️  Weather",
        "🍽️  Restaurants",
        "🛡️  Safety & Health",
        "🛂  Immigration",
    ])

    mapping = [
        ("Hotel", 0, "Hotel intelligence"),
        ("Weather", 1, "7-day forecast"),
        ("Restaurant", 2, "Dining options"),
        ("Safety & Health", 3, "Safety & health intelligence"),
        ("Immigration", 4, "Entry & visa information"),
    ]

    for key, index, heading in mapping:
        with tabs[index]:
            st.markdown(
                f'<div class="result-shell"><div class="result-heading">{heading}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(results.get(key, "No result returned."))
            st.markdown(
                '<div style="margin-top:1rem;color:#7b8a9d;font-size:.75rem;">↗ Verify important information at the original source before booking or travelling.</div></div>',
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="footer">
<strong>Travel Companion AI</strong> · AI-assisted destination research.<br>
Information can change quickly. Always verify visa, medical, security, weather and booking details with the relevant official or primary source before making travel decisions.
</div>
""",
    unsafe_allow_html=True,
)

