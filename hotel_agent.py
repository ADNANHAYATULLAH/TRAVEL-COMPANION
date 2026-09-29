from crewai import Agent, LLM
from tools import hotel_search


def create_hotel_agent(llm: LLM) -> Agent:
    return Agent(
        role="Hotel Research Specialist",
        goal="Find useful, current hotel options in {city}, {country}, including price information, official links and contact details.",
        backstory=(
            "You are a careful travel researcher. Use your hotel search tool before "
            "writing anything. Separate verified facts from estimates and never invent prices, "
            "phone numbers or websites."
        ),
        llm=llm,
        tools=[hotel_search],
        allow_delegation=False,
        verbose=False,
    )
