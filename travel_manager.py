from crewai import Agent, LLM


def create_travel_manager(llm: LLM) -> Agent:
    return Agent(
        role="Travel Companion Manager",
        goal="Turn compact specialist research into a short, factual travel overview for {city}, {country}.",
        backstory=(
            "You are a concise travel information editor. Use only supplied research. "
            "Do not invent facts. Preserve useful source links and clearly flag information "
            "that should be verified before travel."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
