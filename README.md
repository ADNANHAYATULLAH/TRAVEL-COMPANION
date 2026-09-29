# ✈️ Travel Companion AI

A modular CrewAI + Groq + Streamlit multi-agent travel research app.

## Agents
- Hotel Research Agent
- Weather Agent
- Restaurant Agent
- Safety & Health Agent
- Immigration Agent
- Travel Manager

## Tools
- Web search using DDGS
- Open-Meteo geocoding + 7-day forecast
- Specialized web-search tools for hotels, restaurants, safety/health and immigration

## Deployment
The app is designed for GitHub + Streamlit Community Cloud.

Add this secret in Streamlit Cloud:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Do not commit API keys.
