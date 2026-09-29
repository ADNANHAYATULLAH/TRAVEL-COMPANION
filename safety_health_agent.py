from crewai import Agent, LLM
from tools import safety_health_search


def create_safety_health_agent(llm: LLM) -> Agent:
    return Agent(
        role="Safety and Health Research Specialist",
        goal="Research current safety, security, law-and-order and public-health information for {city}, {country}.",
        backstory=(
            "You are a cautious travel-risk researcher. Search first and prioritize "
            "official government, WHO and recognized travel-security sources. Clearly "
            "label the date/source of important claims and distinguish a city issue from "
            "a country-wide issue."
        ),
        llm=llm,
        tools=[safety_health_search],
        allow_delegation=False,
        verbose=False,
    )
