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

Retrieves current weather information for a requested location using the **Open-Meteo API**.

The tool performs location lookup, retrieves the current weather data, processes the returned JSON response, and presents the relevant information to the user.

### 📝 Text Utility

Provides text-based operations such as:

- Word counting
- Reversing text

The fallback implementation also recognizes several natural-language variations of these requests.

### 💱 Currency Converter

Converts between currencies using exchange-rate data from the **Frankfurter API**.

The tool retrieves the exchange rate, processes the JSON response, and calculates the requested conversion.

### 🕐 Local Time & Timezone

Retrieves the current local time for a requested city or location.

The tool first determines the location and its timezone and then retrieves the current local time using **TimeAPI**.

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

The project follows a tool-based AI agent architecture.

### 🤖 Primary Gemini Architecture

Under normal operation, the user request is processed by Gemini, which determines the appropriate tool to call.

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
```

### 🔄 Tool Execution Flow

The general request flow is:

```text
User Request
     │
     ▼
Gemini Agent
     │
     ▼
Tool Selection
     │
     ▼
Python Tool
     │
     ├── Local Logic
     │
     └── External REST API
              │
              ▼
         JSON Response
              │
              ▼
       Processed Tool Result
              │
              ▼
        Gemini Response
              │
              ▼
             User
```

---

## 🛡️ Fallback Architecture

TravelMate AI includes a deterministic fallback system to maintain core functionality when the Gemini API is unavailable, rate-limited, or unable to process a request.

The fallback does not attempt to replace Gemini's reasoning capabilities. Instead, it provides a lightweight rule-based routing layer for the supported tools.

### How It Works

Under normal operation:

```text
User Request
     │
     ▼
Gemini Agent
     │
     ▼
Tool Selection
     │
     ▼
Specialized Tool
     │
     ▼
REST API / Local Logic
     │
     ▼
Tool Result
     │
     ▼
Gemini Response
     │
     ▼
User
```

If Gemini cannot process the request because of a quota or service error, the application can use the fallback path:

```text
User Request
     │
     ▼
Gemini API
     │
     │ API unavailable / quota exceeded
     ▼
Fallback Agent
     │
     ▼
Rule-Based Intent Detection
     │
     ├──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
  Weather         Time         Currency       Calculator
     │              │              │              │
     ▼              ▼              ▼              ▼
  Weather API    Time API    Currency API     Local Logic
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                            │
                            ▼
                          Result
                            │
                            ▼
                           User
```

### Why a Fallback?

An AI agent can depend on external model availability and API quotas. During development, Gemini's request quota was reached, which demonstrated the importance of separating the **AI reasoning layer** from the **underlying tool layer**.

The fallback allows TravelMate to continue handling its core operations even when the LLM is temporarily unavailable.

For example:

```text
User: What's the weather?

TravelMate: Which city or location would you like the weather for?

User: Mumbai

TravelMate: Weather in Mumbai, India:
            Temperature: 28.5°C
            Wind speed: 18.0 km/h
            Conditions: Light drizzle
```

The fallback agent also supports natural-language variations such as:

- `What is the reverse of hello?`
- `Reverse the word hello`
- `How do I write hello backwards?`
- `How many words are in "hello my name"?`

These requests are handled through deterministic pattern matching and regular expressions rather than an LLM.

### Design Principle

The fallback architecture follows a simple principle:

> **The LLM provides intelligent tool selection, while the tools remain independently usable.**

This separation makes the application more resilient and ensures that a temporary failure in the AI layer does not necessarily make the underlying functionality unavailable.

---

## 🌐 REST APIs & JSON

TravelMate demonstrates how an AI agent can interact with external services through REST APIs.

The external APIs used include:

| Tool | API | Purpose |
|------|-----|---------|
| 🌤️ Weather | Open-Meteo | Current weather information |
| 💱 Currency | Frankfurter | Currency exchange rates |
| 🕐 Local Time | TimeAPI | Current time and timezone |

The external APIs return structured **JSON responses**, which are parsed by the corresponding Python tools before the relevant information is presented to the user.

For example, a currency API may return information containing:

```json
{
  "amount": 1.0,
  "base": "INR",
  "rates": {
    "JPY": 1.669
  }
}
```

The tool processes this response and uses the exchange rate to calculate the requested conversion.

---

## 🔄 How the AI Agent Works

TravelMate follows a tool-calling workflow:

1. The user sends a natural-language request.
2. Gemini receives the request along with the available tool definitions.
3. Gemini determines which tool is appropriate.
4. The selected Python function is executed.
5. If the tool requires external information, it calls the relevant REST API.
6. The API returns structured JSON data.
7. The tool extracts and processes the required information.
8. The result is returned to the agent.
9. TravelMate provides a clear, natural-language response to the user.

This separates the **reasoning layer**, **tool layer**, and **external data layer**.

---

## 🧪 Testing

The project includes separate tests for the tools and fallback agent.

### Tool Testing

Run:

```bash
python test_tools.py
```

Tests include:

- Calculator
- Text Utility
- Weather API
- Local Time API
- Currency API

### Fallback Testing

Run:

```bash
python test_fallback.py
```

The fallback tests cover:

- Weather requests
- Local time requests
- Currency conversion
- Mathematical calculations
- Text reversal
- Word counting
- Missing information and follow-up requests
- Different natural-language variations of text operations

Example test result:

```text
==============================
       TRAVELMATE TESTS
==============================

✅ Calculator: PASS
✅ Text Utility: PASS
✅ Weather API: PASS
✅ Local Time API: PASS
✅ Currency API: PASS

==============================
🎉 ALL TESTS PASSED
==============================
```

---

## 💬 Example Queries

TravelMate can handle requests such as:

```text
What's the weather in Mumbai?

What time is it in Tokyo?

Convert 50000 INR to JPY.

What is 125 * 48?

What is the reverse of hello?

Reverse the word xyz.

How many words are in "hello my name"?

What's the weather?
Mumbai
```

The final example demonstrates the fallback agent's ability to remember that the user is providing the missing location for a previously requested weather lookup.

---

## 🧩 Project Structure

```text
TravelMate-AI/
│
├── main.py              # Main TravelMate application
├── tools.py             # Tool implementations and API integrations
├── fallback.py          # Deterministic fallback agent
├── test_tools.py        # Tool and API tests
├── test_fallback.py     # Fallback agent tests
├── requirements.txt     # Python dependencies
├── .gitignore           # Files excluded from Git
└── README.md            # Project documentation
```

---

## 🔐 API Key Security

The Gemini API key is stored as an environment variable rather than being hardcoded into the source code.

The application initializes the Gemini client using:

```python
client = genai.Client()
```

The API key itself is never included in the repository.

Sensitive files such as `.env` are excluded through `.gitignore`.

### Environment Variable

The application expects:

```text
GEMINI_API_KEY=your_api_key
```

The actual API key should never be committed to GitHub or shared publicly.

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TravelMate-AI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API Key

Set your Gemini API key as an environment variable.

The key should **not** be hardcoded into the source code or committed to the repository.

### 4. Run TravelMate

```bash
python main.py
```

### 5. Run the Tests

```bash
python test_tools.py
python test_fallback.py
```

---

## 🎯 Why TravelMate?

The main goal of TravelMate was not simply to combine multiple APIs, but to demonstrate how **an AI agent can use tools to perform real actions**.

The project combines:

- Natural-language interaction
- Gemini function calling
- Local Python tools
- External REST APIs
- JSON response processing
- Conversational state
- Error handling
- Deterministic fallback routing

Together, these components create a practical example of a tool-using AI agent built around a cohesive travel use case.

---

## 🏆 Hackathon

**Pleximus AI Hackathon — FAMT Ratnagiri**

A solo AI agent project built during the hackathon.

---

## 👩‍💻 Author

**Samiya Khalid**

Built with Python, Gemini, REST APIs, and a lot of debugging. ✈️