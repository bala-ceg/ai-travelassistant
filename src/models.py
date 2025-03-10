from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class TravelState(BaseModel):
    """Represents the state of a travel request through different processing stages."""

    query: str = Field(..., description="The user's natural language travel query.")
    
    departure_airport: Optional[str] = Field(None, description="IATA code of the departure airport.")
    arrival_airport: Optional[str] = Field(None, description="IATA code of the arrival airport.")
    departure_date: Optional[str] = Field(None, description="Departure date in YYYY-MM-DD format.")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format. Defaults to one week after departure if not provided.")
    destination: Optional[str] = Field(None, description="The main destination city.")

    flights_info: Optional[str] = Field(None, description="Formatted flight details.")
    hotels_info: Optional[str] = Field(None, description="Formatted hotel accommodation details.")
    sights_info: Optional[str] = Field(None, description="Formatted sightseeing recommendations.")
    itinerary: Optional[str] = Field(None, description="AI-generated structured travel itinerary.")

    class Config:
        arbitrary_types_allowed = True  # Allow non-Pydantic types if necessary
