from fallback import fallback_agent


tests = [
    "What's the weather in Mumbai?",
    "What time is it in Tokyo?",
    "Convert 50000 INR to JPY",
    "What is 125 * 48?",
    "Reverse Hackathon"
]


print("\n==============================")
print("   CONVERSATION TEST")
print("==============================\n")

print("You: What's the weather?")

response = fallback_agent("What's the weather?")

print("TravelMate:", response)

print("\nYou: Delhi")

response = fallback_agent("Delhi")

print("TravelMate:", response)