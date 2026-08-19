import requests


# ============================================================
# 1. CALCULATOR
# ============================================================

def calculator(expression: str) -> str:
    """
    Performs a mathematical calculation.

    Use this tool for arithmetic such as addition, subtraction,
    multiplication, division, percentages, and brackets.

    Args:
        expression: A mathematical expression such as "250 * 4".

    Returns:
        The calculated result.
    """

    try:
        # Only allow basic arithmetic characters.
        allowed = "0123456789+-*/().% "

        if not all(char in allowed for char in expression):
            return "Invalid expression. Only basic arithmetic is supported."

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "I could not calculate that. Please check the expression."


# ============================================================
# 2. WORD / TEXT UTILITY
# ============================================================

def text_utility(operation: str, text: str) -> str:
    """
    Performs a text operation.

    Supported operations:
    - word_count
    - character_count
    - reverse
    - uppercase
    - lowercase

    Args:
        operation: The requested text operation.
        text: The text to process.

    Returns:
        The result of the requested operation.
    """

    operation = operation.lower().strip()

    if operation == "word_count":

        return f"The text contains {len(text.split())} words."

    elif operation == "character_count":

        return f"The text contains {len(text)} characters."

    elif operation == "reverse":

        return text[::-1]

    elif operation == "uppercase":

        return text.upper()

    elif operation == "lowercase":

        return text.lower()

    else:

        return (
            "Unsupported operation. "
            "Use word_count, character_count, reverse, "
            "uppercase, or lowercase."
        )


# ============================================================
# 3. LOCATION LOOKUP
# ============================================================

def get_location_info(location: str) -> dict:
    """
    Finds geographic information for a city or location.

    This uses Open-Meteo's free geocoding API to find the
    latitude, longitude, country, and IANA timezone.

    Args:
        location: City or location name, such as "Tokyo" or
                  "Paris, France".

    Returns:
        A dictionary containing location information.
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results")

        if not results:
            return {
                "error": f"Could not find the location '{location}'."
            }

        result = results[0]

        return {
            "name": result.get("name"),
            "country": result.get("country"),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
            "timezone": result.get("timezone")
        }

    except requests.RequestException as e:

        return {
            "error": f"Location lookup failed: {e}"
        }


# ============================================================
# 4. WEATHER
# ============================================================

def weather_description(code: int) -> str:

    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return descriptions.get(code, "Unknown conditions")

def get_weather(location: str) -> str:
    """
    Gets the current weather for a city or location.

    Args:
        location: City name, such as "Mumbai", "Tokyo",
                  or "Paris, France".

    Returns:
        Current temperature, wind speed, and weather information.
    """

    location_info = get_location_info(location)

    if "error" in location_info:
        return location_info["error"]

    latitude = location_info["latitude"]
    longitude = location_info["longitude"]

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
         "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        
        current = data.get("current_weather")

        if not current:
            return "Weather information was not available."

        temperature = current.get("temperature")
        wind_speed = current.get("windspeed")
        weather_code = current.get("weathercode")
        description = weather_description(weather_code)

        return (
            f"Weather in {location_info['name']}, "
            f"{location_info['country']}:\n"
            f"Temperature: {temperature}°C\n"
            f"Wind speed: {wind_speed} km/h\n"
            f"Conditions: {description}"
        )

    except requests.RequestException as e:

        return f"Weather API error: {e}"


# ============================================================
# 5. LOCAL TIME
# ============================================================

def get_local_time(location: str) -> str:
    """
    Gets the current local time for a city.

    Args:
        location: City name, such as "Tokyo", "London",
                  or "Dubai".

    Returns:
        The current local date and time.
    """

    location_info = get_location_info(location)

    if "error" in location_info:
        return location_info["error"]

    timezone = location_info["timezone"]

    url = "https://timeapi.io/api/time/current/zone"

    params = {
        "timeZone": timezone
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        date = data.get("date")
        time = data.get("time")
        day_of_week = data.get("dayOfWeek")

        if not time:
            return "Local time was not available."

        return (
            f"Local time in {location_info['name']}, "
            f"{location_info['country']}:\n"
            f"Date: {date}\n"
            f"Time: {time}\n"
            f"Day: {day_of_week}\n"
            f"Timezone: {timezone}"
        )

    except requests.RequestException as e:

        return f"Time API error: {e}"


# ============================================================
# 6. CURRENCY CONVERTER
# ============================================================

def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """
    Converts an amount from one currency to another.

    Use three-letter ISO currency codes.

    Examples:
        INR, USD, EUR, GBP, JPY, AED

    Args:
        amount: Amount to convert.
        from_currency: Source currency code.
        to_currency: Target currency code.

    Returns:
        Converted amount and exchange rate.
    """

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if amount <= 0:
        return "The amount must be greater than zero."

    if from_currency == to_currency:
        return (
            f"{amount:.2f} {from_currency} = "
            f"{amount:.2f} {to_currency}"
        )

    url = "https://api.frankfurter.dev/v1/latest"

    params = {
        "base": from_currency,
        "symbols": to_currency
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()


        rates = data.get("rates", {})

        rate = rates.get(to_currency)

        if rate is None:
            return (
                f"I could not find an exchange rate for "
                f"{from_currency} to {to_currency}."
            )

        converted = amount * rate

        return (
            f"{amount:.2f} {from_currency} = "
            f"{converted:.2f} {to_currency}\n"
            f"Exchange rate: 1 {from_currency} = "
            f"{rate} {to_currency}\n"
            f"Rate date: {data.get('date')}"
        )

    except requests.RequestException:
        return (
            f"Sorry, I couldn't retrieve an exchange rate "
            f"from {from_currency} to {to_currency}."
        )