# ✈️ TravelMate AI

### An AI-powered travel assistant built with Gemini function calling, specialized tools, and real-time REST APIs.

---

## 🧭 About the Project

TravelMate AI is a conversational travel assistant developed as part of the **Pleximus AI Hackathon at FAMT Ratnagiri**.

The objective of the hackathon was to build an AI agent that goes beyond simply generating text. The agent should understand a user's natural-language request, determine which tool is required, call that tool, use the result, and provide an intelligent response.

The hackathon provided three core tools:

- **Calculator** — local mathematical logic
- **Weather Lookup** — retrieves real-time weather information through an external API
- **Word/Text Utility** — performs local text operations

Participants were also encouraged to extend their agents by integrating additional tools.

---

## 💡 My Approach

Instead of treating the required tools as separate, unrelated utilities, I decided to build them around a single practical use case: **travel assistance**.

I named the project **TravelMate AI** because the goal was to create something that could act as a digital travel companion and provide useful information a traveler may need while planning or taking a trip.

I chose two extensions from the hackathon's available tools:

- 💱 **Currency Converter**
- 🕐 **Date/Time & Timezone**

These extensions naturally complement the required Weather tool.

For example, someone planning a trip to Tokyo may want to know:

> What is the weather there?  
> What time is it there?  
> How much is my money worth in the local currency?

This allowed me to turn the required tools into one cohesive travel-focused agent rather than simply adding unrelated features.

---

## ✨ Features

### 🧮 Calculator
Performs mathematical calculations using local Python logic without requiring an external API.

### 🌤️ Weather Lookup
Retrieves current weather information for a requested location using the Open-Meteo API.

The tool performs location lookup, retrieves the current weather data, processes the returned JSON response, and presents the relevant information to the user.

### 📝 Text Utility
Provides text-based operations such as:

- Word counting
- Reversing text

The fallback implementation also recognizes several natural-language variations of these requests.

### 💱 Currency Converter
Converts between currencies using exchange-rate data from the Frankfurter API.

The tool retrieves the exchange rate, processes the JSON response, and calculates the requested conversion.

### 🕐 Local Time & Timezone
Retrieves the current local time for a requested city or location.

The tool first determines the location and its timezone and then retrieves the current local time using TimeAPI.

### 🤖 Gemini Function Calling
Gemini acts as the primary agent and decides which tool should be used based on the user's natural-language request.

The user does not need to explicitly select an API or function.

For example:

> "What's the weather in Mumbai?"

can be interpreted by the agent as a request to call the weather tool.

Similarly, a request involving multiple types of information can require multiple tools.

### 🛡️ Fallback Agent
A deterministic fallback agent is included so that the application can continue providing its core functionality when the Gemini API is unavailable or rate-limited.

The fallback uses rule-based intent detection and regular expressions to route requests directly to the appropriate tools.

This makes the application more resilient instead of allowing an LLM/API failure to bring down the entire application.

---

## 🏗️ Architecture

The project follows a tool-based AI agent architecture:

```text
                         USER
                           │
                           ▼
                    TravelMate AI
                           │
                           ▼
                    Gemini Agent
                           │
                    Tool Selection
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      Calculator        Weather         Text Utility
          │                │                │
          │                ▼                │
          │           REST API              │
          │                │                │
          │                ▼                │
          │           JSON Response         │
          │                │                │
          └────────────────┼────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       Currency Converter         Local Time
              │                         │
              ▼                         ▼
          REST API                  REST API
              │                         │
              └────────────┬────────────┘
                           ▼
                     Tool Results
                           │
                           ▼
                    Gemini Response
                           │
                           ▼
                         USER