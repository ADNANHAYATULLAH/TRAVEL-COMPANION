from crewai import Agent, LLM
from tools import weather_forecast


def create_weather_agent(llm: LLM) -> Agent:
    return Agent(
        role="Weather Specialist",
        goal="Provide a clear 7-day weather forecast for {city}, {country}.",
        backstory=(
            "You are a weather-focused travel assistant. Always call the weather "
            "forecast tool. Present dates, conditions, highs, lows, rain probability "
            "and wind in a traveler-friendly format."
        ),
        llm=llm,
        tools=[weather_forecast],
        allow_delegation=False,
        verbose=False,
    )
