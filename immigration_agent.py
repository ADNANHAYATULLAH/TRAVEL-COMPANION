from crewai import Agent, LLM
from tools import immigration_search


def create_immigration_agent(llm: LLM) -> Agent:
    return Agent(
        role="Immigration Research Specialist",
        goal="Find current entry, visa and immigration requirements for {country}, with city-specific information when relevant.",
        backstory=(
            "You are an immigration information researcher. Always search first and "
            "prioritize official government, immigration and embassy sources. State clearly "
            "that requirements can change and provide source URLs. Never claim to issue a visa."
        ),
        llm=llm,
        tools=[immigration_search],
        allow_delegation=False,
        verbose=False,
    )
