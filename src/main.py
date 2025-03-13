import asyncio
import os
import json
import datetime
from apify import Actor
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.tools import find_flights, find_hotels, find_places_to_visit
from src.models import TravelState
from src.ppe_utils import charge_for_actor_start, charge_for_model_tokens


#  OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com")

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)


#  Extract structured travel data using AI
def extract_query(state: TravelState):
    """Extract structured travel data from user query using AI."""
    today = datetime.date.today().strftime("%Y-%m-%d")

    prompt = ChatPromptTemplate.from_template(
     """
        You're a seasoned travel planner with a knack for finding the best deals and exploring new destinations. You're known for your attention to detail
        and your ability to make travel planning easy for customers.

        From the user's request, you have to find the following information: 
        - **IATA code of the departure airport**
        - **IATA code of the arrival airport**
        - **Departure date**
        - **Return date** (If not provided, assume a one-week trip)
        - **Destination city**

        Today's date is {date_today}.

        User's request: {query}

        Now extract the necessary information from the user's request.
        Return the output **strictly** in the following JSON format:
        ```
        {{
            "departure_airport": "IATA code",
            "arrival_airport": "IATA code",
            "departure_date": "YYYY-MM-DD",
            "return_date": "YYYY-MM-DD",
            "destination": "City Name"
        }}
        ```
        """
    )

    chain = prompt | llm
    response = chain.invoke({"date_today": today, "query": state.query})

    total_tokens = response.response_metadata["token_usage"]["total_tokens"]
    asyncio.create_task(charge_for_model_tokens("gpt-3.5-turbo", total_tokens))

    # Extract JSON from AI response
    try:
        response_json = json.loads(response.content)
        Actor.log.info(f"Extracted structured query: {response_json}")
    except json.JSONDecodeError:
        Actor.log.error(f"Failed to parse JSON: {response.content}")
        response_json = {}

    return TravelState(
        query=state.query,
        departure_airport=response_json.get("departure_airport"),
        arrival_airport=response_json.get("arrival_airport"),
        departure_date=response_json.get("departure_date"),
        return_date=response_json.get("return_date"),
        destination=response_json.get("destination"),
    )


#  Fetch flights data
def fetch_flights(state: TravelState):
    """Fetch flight details for the planned trip."""
    if not state.departure_airport or not state.arrival_airport or not state.departure_date:
        Actor.log.warning("Skipping flight search: missing required details.")
        return state

    response = find_flights.invoke(
        {
            "departure_airport": state.departure_airport,
            "arrival_airport": state.arrival_airport,
            "departure_date": state.departure_date,
            "return_date": state.return_date,
        }
    )

    state.flights_info = response if isinstance(response, str) else json.dumps(response)
    Actor.log.info(f"Flights Info: {state.flights_info}")
    return state


#  Fetch hotel accommodations
def fetch_hotels(state: TravelState):
    """Fetch hotel listings in the destination city."""
    if not state.destination:
        Actor.log.warning("Skipping hotel search: missing destination.")
        return state

    response = find_hotels.invoke(
        {
            "city": state.destination,
            "check_in_date": state.departure_date,
            "check_out_date": state.return_date,
        }
    )

    state.hotels_info = response if isinstance(response, str) else json.dumps(response)
    Actor.log.info(f"Hotels Info: {state.hotels_info}")
    return state


#  Fetch sightseeing places
def fetch_places(state: TravelState):
    """Find top places to visit in the travel destination."""
    if not state.destination:
        Actor.log.warning("Skipping sightseeing search: missing destination.")
        return state

    response = find_places_to_visit.invoke({"location": state.destination})

    state.sights_info = response if isinstance(response, str) else json.dumps(response)
    Actor.log.info(f"Sightseeing Info: {state.sights_info}")
    return state


def generate_itinerary(state: TravelState):
    """Generate a detailed travel itinerary using OpenAI and structured prompts."""

    #  Ensure travel data is valid before using it
    flights_summary = state.flights_info if state.flights_info else "No flight information available."
    hotels_summary = state.hotels_info if state.hotels_info else "No hotel information available."
    sights_summary = state.sights_info if state.sights_info else "No sightseeing recommendations available."

    #  Ensure at least one category has meaningful data before proceeding
    if flights_summary == "No flight information available." and hotels_summary == "No hotel information available." and sights_summary == "No sightseeing recommendations available.":
        Actor.log.warning("No valid travel data found. Skipping itinerary generation.")
        state.itinerary = "Itinerary generation failed due to missing travel data."
        return state
    
    itinerary_prompt = ChatPromptTemplate.from_template("""
        # 🌍 AI-Powered Travel Itinerary Generator  

        **You are a professional travel planner.** Your goal is to create a **well-structured, detailed markdown itinerary**  
        based on the provided travel details, including **flights, hotels, and attractions**.

        ---
        ## ✈️ Trip Overview  
        - **Destination:** {destination}  
        - **Departure Date:** {departure_date}  
        - **Return Date:** {return_date}  

        ---
        ## 🛫 Flight Details  
        **Available flight options:**  
        {flights_summary}  

        ---
        ## 🏨 Hotel Accommodations  
        **Recommended hotels for the trip:**  
        {hotels_summary}  

        ---
        ## 📍 Sightseeing & Attractions  
        **Top attractions to visit:**  
        {sights_summary}  

        ---
        ## 📅 Day-by-Day Itinerary  
        Generate a structured **day-by-day itinerary** covering:  
        - 🌅 **Morning Activities**
        - 🍽 **Lunch Suggestions**
        - 🎭 **Afternoon & Evening Plans**
        - 🚖 **Transport Recommendations**
        - 💰 **Approximate Daily Costs (Flight, Hotel, Attractions, Food)**

        Generate a well-structured markdown itinerary. 
        """)

    #  Use structured prompt from `prompts.py`
    prompt_chain = itinerary_prompt | ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

    #  Invoke the LLM with structured input
    response = prompt_chain.invoke({
        "destination": state.destination,
        "departure_date": state.departure_date,
        "return_date": state.return_date,
        "flights_summary": flights_summary,
        "hotels_summary": hotels_summary,
        "sights_summary": sights_summary
    })

    #  Track token usage for billing
    total_tokens = response.response_metadata["token_usage"]["total_tokens"]
    asyncio.create_task(charge_for_model_tokens("gpt-3.5-turbo", total_tokens))

    #  Log sightseeing details for debugging
    Actor.log.info(f"Sightseeing Info: {json.dumps(state.sights_info, indent=2)}")

    #  Store itinerary safely
    state.itinerary = response.content if response and hasattr(response, "content") else "Itinerary generation failed."
    return state




#  Define LangGraph Workflow
graph = StateGraph(TravelState)
graph.add_node("extract_query", extract_query)
graph.add_node("fetch_flights", fetch_flights)
graph.add_node("fetch_hotels", fetch_hotels)
graph.add_node("fetch_places", fetch_places)
graph.add_node("generate_itinerary", generate_itinerary)

# Set up workflow steps
graph.add_edge("extract_query", "fetch_flights")
graph.add_edge("fetch_flights", "fetch_hotels")
graph.add_edge("fetch_hotels", "fetch_places")
graph.add_edge("fetch_places", "generate_itinerary")
graph.add_edge("generate_itinerary", END)

# Define entry point explicitly
graph.set_entry_point("extract_query")

#  Compile workflow
travel_workflow = graph.compile()



async def save_report(state):
    """Save the travel itinerary report in markdown format & store in Apify KV Store."""

    itinerary_content = state.get("itinerary", "Itinerary generation failed.").strip().replace("\t", "")

    # Construct markdown report
    report_content = f"""# ✈️ AI Travel Assistant Report

## 🌍 Travel Itinerary Summary
- **Destination:** `{state.get("destination", "N/A")}`
- **Departure Date:** `{state.get("departure_date", "N/A")}`
- **Return Date:** `{state.get("return_date", "N/A")}`

---

## 📝 AI-Generated Itinerary
{itinerary_content}

---

📌 *This report was generated automatically by AI Travel Assistant. Please verify details before booking.*
    """

    #  Store report in Apify Key-Value Store
    store = await Actor.open_key_value_store()
    await store.set_value("report.md", report_content)
    Actor.log.info('Saved the "report.md" file into the key-value store!')




#  Main Function
async def main():
    """Runs the AI Travel Planner workflow."""
    async with Actor:
        

        actor_input = await Actor.get_input() or {}
        Actor.log.info(f"Received input: {actor_input}")

        asyncio.create_task(charge_for_actor_start())

        travel_query = TravelState(**actor_input)

        # Execute workflow
        final_state = travel_workflow.invoke(travel_query)
        Actor.log.info(f"Workflow completed. Final state: {final_state}")
        # Save the final report
        await save_report(final_state)



#  Run Main
if __name__ == "__main__":
    asyncio.run(main())
