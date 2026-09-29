from crewai import Agent, LLM
from tools import restaurant_search


def create_restaurant_agent(llm: LLM) -> Agent:
    return Agent(
        role="Restaurant Research Specialist",
        goal="Find restaurants in {city}, {country}, grouped into halal and non-halal options.",
        backstory=(
            "You research food options for travelers. Use your search tool for both "
            "categories. Do not assume a restaurant is halal unless the source supports it. "
            "Include address, website and phone when available."
        ),
        llm=llm,
        tools=[restaurant_search],
        allow_delegation=False,
        verbose=False,
    )
