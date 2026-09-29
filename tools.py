"""Custom web and weather tools for Travel Companion."""

from crewai.tools import tool
from ddgs import DDGS
import requests


def _search_web(query: str) -> str:
    """Internal web-search implementation with a small result packet."""
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No web results found."

        lines = []
        for i, r in enumerate(results, 1):
            title = str(r.get("title", "Untitled"))[:180]
            url = str(r.get("href", ""))[:500]
            snippet = str(r.get("body", ""))[:600]
            lines.append(f"{i}. {title}\nURL: {url}\nSnippet: {snippet}")

        return "\n\n".join(lines)
    except Exception as exc:
        return f"Web search failed: {exc}"


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the public web and return concise results."""
    return _search_web(query)


def _weather_forecast(city: str, country: str) -> str:
    """Direct Open-Meteo forecast lookup used without an LLM tool loop."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": f"{city}, {country}",
                "count": 5,
                "language": "en",
                "format": "json",
            },
            timeout=15,
        )
        geo.raise_for_status()
        places = geo.json().get("results", [])
        if not places:
            return f"Could not locate {city}, {country}."

        place = next(
            (p for p in places if p.get("country", "").lower() == country.lower()),
            places[0],
        )
        lat, lon = place["latitude"], place["longitude"]

        forecast = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": (
                    "weather_code,temperature_2m_max,temperature_2m_min,"
                    "precipitation_probability_max,wind_speed_10m_max"
                ),
                "forecast_days": 7,
                "timezone": "auto",
            },
            timeout=15,
        )
        forecast.raise_for_status()
        daily = forecast.json()["daily"]

        code_names = {
            0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
            55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
            71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
            81: "Rain showers", 82: "Heavy rain showers", 95: "Thunderstorm",
            96: "Thunderstorm with hail", 99: "Thunderstorm with hail",
        }

        rows = []
        for i, date in enumerate(daily["time"]):
            rows.append(
                f"{date}: {code_names.get(daily['weather_code'][i], 'Mixed')} | "
                f"High {daily['temperature_2m_max'][i]}°C | "
                f"Low {daily['temperature_2m_min'][i]}°C | "
                f"Rain {daily['precipitation_probability_max'][i]}% | "
                f"Wind {daily['wind_speed_10m_max'][i]} km/h"
            )

        return f"Location: {place.get('name')}, {place.get('country')}\n" + "\n".join(rows)
    except Exception as exc:
        return f"Weather lookup failed: {exc}"


@tool("Weather Forecast")
def weather_forecast(city: str, country: str) -> str:
    """Get a 7-day forecast using Open-Meteo."""
    return _weather_forecast(city, country)


@tool("Hotel Search")
def hotel_search(city: str, country: str) -> str:
    """Search the web for hotels and contact information."""
    return _search_web(
        f"hotels in {city}, {country} current price official website phone Booking Agoda"
    )


@tool("Restaurant Search")
def restaurant_search(city: str, country: str, category: str) -> str:
    """Search restaurants in a city."""
    return _search_web(f"{category} restaurants in {city}, {country} address phone website")


@tool("Safety Health Search")
def safety_health_search(city: str, country: str) -> str:
    """Search current safety, health and travel-advisory information."""
    return _search_web(
        f"{city} {country} travel advisory security law order disease outbreak health advisory WHO government"
    )


@tool("Immigration Search")
def immigration_search(city: str, country: str) -> str:
    """Search current visa and entry requirements."""
    return _search_web(
        f"{country} visa entry requirements passport validity official immigration embassy government"
    )
