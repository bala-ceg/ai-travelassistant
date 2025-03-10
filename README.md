# 🌍 AI Travel Assistant

**AI Travel Assistant** is a powerful AI-powered tool that helps users plan their trips effortlessly. It integrates **flight search, hotel booking, and sightseeing recommendations** to generate a structured **travel itinerary** using **LangChain, Apify, and OpenAI**.

---

## ✈️ Features

- 🛫 **Flight Search**: Finds the best flight options based on departure and arrival cities.
- 🏨 **Hotel Search**: Suggests accommodations with pricing, ratings, and amenities.
- 📍 **Sightseeing Recommendations**: Lists must-visit places at the destination.
- 📅 **AI-Generated Itinerary**: Creates a day-wise structured travel plan.
- 📜 **Markdown Report Generation**: Saves itinerary in a readable markdown format.
- ⚡ **Apify Actor Integration**: Uses Apify actors for web scraping travel data.
- 🔗 **LangChain & OpenAI**: Ensures intelligent, natural language processing.

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/ai-travelassistant.git
cd ai-travelassistant
```

### 2️⃣ Create a Virtual Environment (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Keys
Create a `.env` file and add your API keys:
```ini
OPENAI_API_KEY=your-openai-key
SERPAPI_KEY=your-serpapi-key
```

---

## 🎯 **How to Run Locally**
```bash
apify run --input-file=input.json
```
📜 **Example `input.json`**
```json
{
    "ticker": "Plan a 7-day trip to Bali from New York, staying in a beachfront hotel."
}
```

---
```
ai-travelassistant/
│── src/
│   ├── main.py         # Apify Actor entry point
│   ├── tools.py        # Flight, hotel, sightseeing scraping tools
│   ├── models.py       # Pydantic data models
│   ├── prompts.py      # AI prompt templates
│   ├── report.md       # Generated travel itinerary report
│── .venv/              # Virtual environment (optional)
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
│── input.json          # Example input format
│── .env                # API keys (gitignore this file)
```
---

## 📊 **Example Report Output**

# ✈️ AI Travel Assistant Report

## 🌍 Travel Itinerary Summary
- **Destination:** `Bali`
- **Departure Date:** `2025-03-17`
- **Return Date:** `2025-03-24`

---

## 📝 AI-Generated Itinerary
### Day 1:  
- 🌅 **Morning Activities:**  
    - Arrival in Bali
    - Check-in at Villa Karma Loka

- 🍽 **Lunch:**  
    - Enjoy a traditional Balinese meal at a local warung

- 🎭 **Afternoon & Evening Plans:**  
    - Visit Sacred Monkey Forest Sanctuary
    - Explore Ubud Market
    - Dinner at a local restaurant

- 🚖 **Transport:**  
    - Private car or taxi to attractions

- 💰 **Approximate Daily Costs:**  
    - Flight: $1001
    - Hotel: $60
    - Attractions: $10
    - Food: $20
    - Total: $1091

### Day 2:  
- 🌅 **Morning Activities:**  
    - Breakfast at Villa Karma Loka
    - Visit Uluwatu Temple

- 🍽 **Lunch:**  
    - Enjoy seafood by the beach at Jimbaran Bay

- 🎭 **Afternoon & Evening Plans:**  
    - Explore Ceking Rice Terrace
    - Relax at the beach
    - Dinner at a beachfront restaurant

- 🚖 **Transport:**  
    - Rent a scooter for the day

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $60
    - Attractions: $15
    - Food: $30
    - Total: $105

### Day 3:  
- 🌅 **Morning Activities:**  
    - Breakfast at The Kirana Ungasan
    - Visit Campuhan Ridge Walk

- 🍽 **Lunch:**  
    - Try local Balinese cuisine at a village restaurant

- 🎭 **Afternoon & Evening Plans:**  
    - Visit Ulun Danu Beratan Temple
    - Explore Bedugul Botanical Gardens
    - Dinner at a lakeside restaurant

- 🚖 **Transport:**  
    - Hire a private driver for the day

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $30
    - Attractions: $20
    - Food: $25
    - Total: $75

### Day 4:  
- 🌅 **Morning Activities:**  
    - Breakfast at Prasi Sunset Bungalows
    - Visit Waterbom Bali

- 🍽 **Lunch:**  
    - Have a poolside lunch at a resort

- 🎭 **Afternoon & Evening Plans:**  
    - Relax at the beach
    - Sunset dinner cruise

- 🚖 **Transport:**  
    - Shuttle or taxi to attractions

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $19
    - Attractions: $50
    - Food: $50
    - Total: $119

### Day 5:  
- 🌅 **Morning Activities:**  
    - Breakfast at Masna House
    - Visit Pura Tirta Empul

- 🍽 **Lunch:**  
    - Try Indonesian cuisine at a local restaurant

- 🎭 **Afternoon & Evening Plans:**  
    - Visit Tegenungan Waterfall
    - Explore Ubud Palace
    - Dinner at a rooftop restaurant

- 🚖 **Transport:**  
    - Rent a car for the day

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $18
    - Attractions: $15
    - Food: $35
    - Total: $68

### Day 6:  
- 🌅 **Morning Activities:**  
    - Breakfast at The Laguna, a Luxury Collection Resort & Spa, Nusa Dua, Bali
    - Visit Bali Safari and Marine Park

- 🍽 **Lunch:**  
    - Enjoy a buffet lunch at the park

- 🎭 **Afternoon & Evening Plans:**  
    - Relax at the resort
    - Dinner at a fine dining restaurant

- 🚖 **Transport:**  
    - Shuttle to the park

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $128
    - Attractions: $50
    - Food: $40
    - Total: $218

### Day 7:  
- 🌅 **Morning Activities:**  
    - Breakfast at Sumberkima Hill Retreat
    - Visit Besakih Great Temple

- 🍽 **Lunch:**  
    - Try traditional Balinese cuisine at a local restaurant

- 🎭 **Afternoon & Evening Plans:**  
    - Visit Bali Zoo
    - Sunset dinner at a beach club

- 🚖 **Transport:**  
    - Private car hire for the day

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $33
    - Attractions: $30
    - Food: $45
    - Total: $108

### Day 8:  
- 🌅 **Morning Activities:**  
    - Breakfast at The Anvaya Beach Resort Bali
    - Visit Penataran Agung Lempuyang Temple

- 🍽 **Lunch:**  
    - Enjoy a seafood lunch by the bay

- 🎭 **Afternoon & Evening Plans:**  
    - Visit Tirta Gangga
    - Relax at a natural hot spring
    - Farewell dinner at a beachfront restaurant

- 🚖 **Transport:**  
    - Private transfer to sights

- 💰 **Approximate Daily Costs:**  
    - Flight: $0 (no flight on this day)
    - Hotel: $112
    - Attractions: $20
    - Food: $40
    - Total: $172

### Overall Trip Cost:  
- Total Flight Cost: $1001
- Total Hotel Cost: $460
- Total Attractions Cost: $220
- Total Food Cost: $265
- **Grand Total: $1946 USD**

This itinerary provides a comprehensive plan for your trip to Bali, covering flights, hotels, attractions, and daily activities. Enjoy your vacation in Bali! 🌴🌞🍹

---

📌 *This report was generated automatically by AI Travel Assistant. Please verify details before booking.*
    



## 🚀 **Contributing**
We welcome contributions! Feel free to:
- **Open Issues** for bug reports or feature requests.
- **Submit Pull Requests** to improve the code.

---

## 📜 **License**
This project is licensed under the **MIT License**.
