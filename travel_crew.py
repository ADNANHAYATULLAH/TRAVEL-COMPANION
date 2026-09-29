import os
import time

# Workaround for a CrewAI/LiteLLM cache_breakpoint compatibility issue with Groq.
try:
    import crewai.llms.cache as crew_cache
    crew_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

from crewai import Crew, LLM, Process, Task
from travel_manager import create_travel_manager
from tools import (
    _search_web,
    _weather_forecast,
)


def build_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0.1,
        max_completion_tokens=300,
        reasoning_effort="low",
        include_reasoning=False,
    )


def _compact(text: str, limit: int = 2200) -> str:
    """Keep research packets small enough for the 8K TPM Groq limit."""
    text = str(text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _research_hotel(city: str, country: str) -> str:
    return _search_web(
        f"hotels in {city}, {country} current price official website phone Booking Agoda"
    )


def _research_restaurants(city: str, country: str) -> str:
    halal = _search_web(
        f"halal restaurants in {city}, {country} address phone website"
    )
    non_halal = _search_web(
        f"restaurants in {city}, {country} non-halal address phone website"
    )
    return "HALAL:\n" + _compact(halal, 1400) + "\n\nOTHER RESTAURANTS:\n" + _compact(non_halal, 1400)


def _research_safety(city: str, country: str) -> str:
    return _search_web(
        f"{city} {country} travel advisory security law order disease outbreak health advisory WHO government"
    )


def _research_immigration(city: str, country: str) -> str:
    return _search_web(
        f"{country} visa entry requirements passport validity official immigration embassy government"
    )


def _run_manager(llm, country: str, city: str, reports: dict) -> str:
    manager = create_travel_manager(llm)

    packet = "\n\n".join(
        f"[{name}]\n{_compact(value, 2200)}" for name, value in reports.items()
    )

    task = Task(
        description=(
            f"Create a concise travel overview for {city}, {country}. "
            "Use ONLY the research packet below. Do not invent facts. "
            "Mention important verification points and keep useful URLs. "
            "Maximum about 250 words.\n\nRESEARCH PACKET:\n" + packet
        ),
        expected_output="A concise factual travel overview with source links.",
        agent=manager,
    )

    crew = Crew(
        agents=[manager],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    # If the account has just used most of its 8K TPM window, give it time to reset.
    last_error = None
    for attempt in range(2):
        try:
            return str(crew.kickoff(inputs={"country": country, "city": city}))
        except Exception as exc:
            last_error = exc
            if "rate_limit" not in str(exc).lower() and "rate limit" not in str(exc).lower():
                raise
            if attempt == 0:
                time.sleep(15)

    raise last_error


def run_travel_research(country: str, city: str, progress_callback=None):
    """
    Token-efficient travel research pipeline.

    The five specialist stages perform direct web/API research and do NOT call Groq.
    Only the final Travel Manager uses CrewAI + Groq once.
    """
    reports = {}

    stages = [
        ("Hotel", lambda: _research_hotel(city, country)),
        ("Weather", lambda: _weather_forecast(city, country)),
        ("Restaurant", lambda: _research_restaurants(city, country)),
        ("Safety & Health", lambda: _research_safety(city, country)),
        ("Immigration", lambda: _research_immigration(city, country)),
    ]

    for name, researcher in stages:
        if progress_callback:
            progress_callback(name, "working")

        try:
            reports[name] = _compact(researcher(), 2200)
        except Exception as exc:
            reports[name] = f"Research failed: {exc}"

        if progress_callback:
            progress_callback(name, "complete")

    if progress_callback:
        progress_callback("Travel Manager", "working")

    llm = build_llm()
    summary = _run_manager(llm, country, city, reports)
    reports["Overview"] = summary

    if progress_callback:
        progress_callback("Travel Manager", "complete")

    return reports
