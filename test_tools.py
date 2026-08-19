from tools import (
    calculator,
    text_utility,
    get_weather,
    get_local_time,
    convert_currency,
    weather_description
)


def test_calculator():
    result = calculator("250 * 48")

    assert result == "12000"

    print("✅ Calculator: PASS")


def test_text_utility():
    result = text_utility(
        "word_count",
        "I am building a travel AI agent"
    )

    assert result == "The text contains 7 words."

    print("✅ Text Utility: PASS")


def test_weather():
    result = get_weather("Mumbai")

    assert "Mumbai" in result
    assert "Temperature:" in result
    assert "Wind speed:" in result

    print("✅ Weather API: PASS")


def test_local_time():
    result = get_local_time("Tokyo")

    assert "Tokyo" in result
    assert "Time:" in result
    assert "Timezone:" in result

    print("✅ Local Time API: PASS")


def test_currency():
    result = convert_currency(
        50000,
        "INR",
        "JPY"
    )

    assert "50000.00 INR" in result
    assert "JPY" in result

    print("✅ Currency API: PASS")

def test_invalid_location():

    result = get_weather("XYZNonexistent123")

    assert "Could not find" in result

    print("✅ Invalid Location: PASS")

def test_invalid_amount():

    result = convert_currency(
        -500,
        "INR",
        "JPY"
    )

    assert "greater than zero" in result

    print("✅ Invalid Currency Amount: PASS")

def test_unsupported_currency():

    result = convert_currency(
        50000,
        "INR",
        "KWD"
    )

    assert "couldn't retrieve" in result.lower()

    print("✅ Unsupported Currency: PASS")

def test_weather_description():

    assert weather_description(0) == "Clear sky"
    assert weather_description(51) == "Light drizzle"
    assert weather_description(95) == "Thunderstorm"

    print("✅ Weather Description: PASS")




print("\n==============================")
print("       TRAVELMATE TESTS")
print("==============================\n")

try:
    test_calculator()
    test_text_utility()
    test_weather()
    test_local_time()
    test_currency()

    print("\n==============================")
    print("🎉 ALL TESTS PASSED")
    print("==============================")

except AssertionError as e:

    print("\n❌ TEST FAILED")
    print(e)

except Exception as e:

    print("\n❌ ERROR")
    print(e)