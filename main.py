from google import genai
from google.genai import types

from tools import (
    calculator,
    text_utility,
    get_weather,
    get_local_time,
    convert_currency
)

from fallback import fallback_agent

# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client()


# ============================================================
# AGENT INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTION = """
You are TravelMate AI, a helpful AI travel assistant.

Your job is to help users with travel-related questions.

You have access to these tools:

1. calculator
   Use this for mathematical calculations.

2. text_utility
   Use this for word counting, character counting,
   reversing text, converting text to uppercase,
   or converting text to lowercase.

3. get_weather
   Use this when the user asks about the weather
   in a particular location.

4. get_local_time
   Use this when the user asks for the current
   local time in a particular location.

5. convert_currency
   Use this when the user wants to convert money
   between currencies.

IMPORTANT RULES:

- Use tools when the user's request requires current
  information or a calculation.

- Do not make up weather, time, calculation, or
  exchange-rate data.

- If a required piece of information is missing,
  ask the user for it instead of guessing.

- You may use multiple tools for a single user request.

- Always trust the result returned by a tool over
  your own knowledge.

- Never guess, estimate, or invent an exchange rate.

- Only report a currency conversion when the
  currency tool successfully returns a result.

- If a tool reports an error, clearly tell the user
  that the requested information could not be retrieved.
  Do not replace the failed tool result with a guess.

- Do not expose raw API responses, debug information,
  or internal tool details to the user.

- After receiving tool results, give the user a clear,
  concise, and natural answer.

- If the request does not require a tool, answer normally.
"""


# ============================================================
# ASK THE AGENT
# ============================================================

chat = client.chats.create(
        model="gemini-3.6-flash",

        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,

            tools=[
                calculator,
                text_utility,
                get_weather,
                get_local_time,
                convert_currency
            ]
        )
    )

def ask_agent(user_input):

    try:
        response = chat.send_message(user_input)

        return response.text

    except Exception as e:

        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):

            return fallback_agent(user_input)

        raise e


# ============================================================
# CHAT LOOP
# ============================================================

print("=" * 55)
print("✈️  TravelMate AI")
print("=" * 55)

print("Your AI travel assistant.")
print("Ask about weather, time, currency, calculations,")
print("or text utilities.")
print("Type 'exit' to quit.")
print()


while True:

    user_input = input("Ask a Question: ")

    if user_input.lower().strip() == "exit":
        print("\nGoodbye! 👋")
        break

    if not user_input.strip():
        continue

    try:

        answer = ask_agent(user_input)

        print("\nTravelMate:", answer)
        print()

    except Exception as e:

        print("\nSomething went wrong:")
        print(e)
        print()