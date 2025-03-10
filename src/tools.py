import os
import logging
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from serpapi import GoogleSearch
from langchain_core.tools import tool



# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Initialize SerpAPI key
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def format_minutes(total_minutes):
    """Convert minutes into hours and minutes."""
    try:
        if not isinstance(total_minutes, int) or total_minutes < 0:
            raise ValueError("Total minutes must be a non-negative integer.")
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} hr {minutes} min" if hours else f"{minutes} min"
    except Exception as e:
        raise ValueError(f"Failed to format minutes: {str(e)}")


def format_one_flight(flight):
    """Format a single flight segment into a readable string."""
    try:
        flight_no = flight.get("flight_number", "N/A")
        dep_port = flight.get("departure_airport", {}).get("id", "Unknown")
        arr_port = flight.get("arrival_airport", {}).get("id", "Unknown")
        dep_time = flight.get("departure_airport", {}).get("time", "N/A")
        arr_time = flight.get("arrival_airport", {}).get("time", "N/A")
        duration = flight.get("duration", 0)
        airline = flight.get("airline", "Unknown Airline")  #  Fix: Handle missing airline
        airplane = flight.get("airplane", "N/A")

        return f"{airline} {flight_no} - {dep_port} ({dep_time}) → {arr_port} ({arr_time}) [{format_minutes(duration)}] - {airplane}"
    except Exception as e:
        return f"Error formatting flight: {str(e)}"


def get_formatted_flights_info(flights):
    """Format multiple flights into readable output."""
    formatted_flights = []
    for flight in flights:
        for part in flight.get("flights", []):
            formatted_flights.append(format_one_flight(part))

        if "layovers" in flight and flight["layovers"]:
            formatted_flights.append(
                f"Layover at {flight['layovers'][0].get('id', 'Unknown')}: {format_minutes(flight['layovers'][0].get('duration', 0))}"
            )

        formatted_flights.append(f"Total Duration: {format_minutes(flight.get('total_duration', 0))}")
        formatted_flights.append(f"Price (USD): ${flight.get('price', 'N/A')}")
        formatted_flights.append("")

    return "\n".join(formatted_flights)

#  Find flights (Using @tool)
class FlightInput(BaseModel):
    departure_airport: str = Field(..., description="3-letter IATA departure airport code (e.g., LHR)")
    arrival_airport: str = Field(..., description="3-letter IATA arrival airport code (e.g., JFK)")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date (YYYY-MM-DD) if round-trip")


@tool("find_flights", args_schema=FlightInput, return_direct=True)
def find_flights(departure_airport: str, arrival_airport: str, departure_date: str, return_date: Optional[str] = None) -> str:
    """Fetch flight details using Google Flights API (SerpAPI)."""
    params = {
        "engine": "google_flights",
        "hl": "en",
        "departure_id": departure_airport,
        "arrival_id": arrival_airport,
        "outbound_date": departure_date,
        "return_date": return_date,
        "stops": 2,  # Max 2 stops
        "currency": "USD",
        "api_key": SERPAPI_KEY,
    }
    if return_date:
        params["type"] = "1"  # Round Trip
    else:
        params["type"] = "2"  # One Way

    try:
        logger.info(f"Finding flights from {departure_airport} to {arrival_airport}...")
        search = GoogleSearch(params)
        results = search.get_dict()
        if "error" in results:
            raise ValueError(f"SerpAPI error: {results['error']}")
        return get_formatted_flights_info(results.get("best_flights", []))
    except Exception as e:
        logger.error(f"Failed to search flights: {e}")
        return {"error": str(e)}


#  Find hotels (Using @tool)
class HotelInput(BaseModel):
    city: str = Field(..., description="The city where the hotels are located")
    check_in_date: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    check_out_date: str = Field(..., description="Check-out date (YYYY-MM-DD)")


@tool("find_hotels", args_schema=HotelInput, return_direct=True)
def find_hotels(city: str, check_in_date: str, check_out_date: str) -> str:
    """Fetch hotel listings using Google Hotels API (SerpAPI)."""
    params = {
        "engine": "google_hotels",
        "q": city,
        "hl": "en",
        "gl": "us",
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "currency": "USD",
        "api_key": SERPAPI_KEY,
    }
    try:
        logger.info(f"Finding hotels in {city}...")
        search = GoogleSearch(params)
        results = search.get_dict()
        if "error" in results:
            raise ValueError(f"SerpAPI error: {results['error']}")
        return get_formatted_hotels_info(results.get("properties", []))
    except Exception as e:
        logger.error(f"Failed to find hotels: {e}")
        return {"error": str(e)}


#  Find places to visit (Using @tool)
class PlacesInput(BaseModel):
    location: str = Field(..., description="The location to find places to visit")


@tool("find_places_to_visit", args_schema=PlacesInput, return_direct=True)
def find_places_to_visit(location: str) -> str:
    """Fetch top places to visit using Google API (SerpAPI)."""
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": f"top sights in {location}",
        "location": location,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }
    try:
        logger.info(f"Finding places to visit in {location}...")
        search = GoogleSearch(params)
        results = search.get_dict()
        if "error" in results:
            raise ValueError(f"SerpAPI error: {results['error']}")
        return get_formatted_places_info(results.get("top_sights", {"sights": []})["sights"])
    except Exception as e:
        logger.error(f"Failed to find places: {e}")
        return {"error": str(e)}


#  Helper function to format hotel details
def get_formatted_hotels_info(hotels: List[dict]) -> str:
    """Format hotel details into a readable summary."""
    return "\n".join(
        [f"🏨 {h['name']} - 💰 {h['rate_per_night']['lowest']} USD" for h in hotels]
    )


#  Helper function to format sightseeing places
def get_formatted_places_info(sights: List[dict]) -> str:
    """Format places to visit into a readable summary."""
    return "\n".join(
        [f"📍 {s['title']} - ⭐ {s.get('rating', 'N/A')} ({s.get('reviews', '0')} reviews)" for s in sights]
    )
