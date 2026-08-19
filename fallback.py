import re

from tools import (
    calculator,
    text_utility,
    get_weather,
    get_local_time,
    convert_currency
)


pending_action = None


def fallback_agent(user_input):

    global pending_action

    text = user_input.lower().strip()


    # -----------------------------------------
    # HANDLE PREVIOUSLY REQUESTED INFORMATION
    # -----------------------------------------

    if pending_action:

        location = user_input.strip().rstrip("?.!")

        if pending_action == "weather":

            pending_action = None

            return get_weather(location)

        if pending_action == "time":

            pending_action = None

            return get_local_time(location)


    # -----------------------------------------
    # WEATHER
    # -----------------------------------------

    if "weather" in text:

        location_match = re.search(
            r"weather\s+(?:in|at|for)\s+(.+)",
            text
        )

        if location_match:

            location = (
                location_match.group(1)
                .strip()
                .rstrip("?.!")
            )

            return get_weather(location)

        pending_action = "weather"

        return "Which city or location would you like the weather for?"


    # -----------------------------------------
    # TIME
    # -----------------------------------------

    if (
        "what time" in text
        or "current time" in text
        or "local time" in text
    ):

        location_match = re.search(
            r"(?:time|timezone)\s+(?:is\s+it\s+)?(?:in|at|for)\s+(.+)",
            text
        )

        if location_match:

            location = (
                location_match.group(1)
                .strip()
                .rstrip("?.!")
            )

            return get_local_time(location)

        pending_action = "time"

        return "Which city or location would you like the local time for?"


    # -----------------------------------------
    # CURRENCY
    # -----------------------------------------

    currency_match = re.search(
        r"(\d+(?:\.\d+)?)\s*([A-Za-z]{3})\s+(?:to|in)\s+([A-Za-z]{3})",
        text
    )

    if currency_match:

        amount = float(currency_match.group(1))

        from_currency = currency_match.group(2)

        to_currency = currency_match.group(3)

        return convert_currency(
            amount,
            from_currency,
            to_currency
        )


    # -----------------------------------------
    # CALCULATOR
    # -----------------------------------------

    if any(
        symbol in text
        for symbol in ["+", "-", "*", "/", "%"]
    ):

        expression = re.sub(
            r"[^0-9+\-*/().% ]",
            "",
            text
        )

        if expression.strip():

            return calculator(expression)


    # -----------------------------------------
    # TEXT - REVERSE
    # -----------------------------------------

    if "reverse" in text or "backwards" in text:

        patterns = [

            # "what is the reverse of xyz?"
            r"what\s+is\s+the\s+reverse\s+of\s+(.+)",

            # "what's the reverse of xyz?"
            r"what's\s+the\s+reverse\s+of\s+(.+)",

            # "what about the reverse of xyz?"
            r"what\s+about\s+the\s+reverse\s+of\s+(.+)",

            # "give me the reverse of xyz"
            r"give\s+me\s+the\s+reverse\s+of\s+(.+)",

            # "how do I write xyz backwards?"
            r"how\s+do\s+i\s+write\s+(.+?)\s+backwards",

            # "what is xyz backwards?"
            r"what\s+is\s+(.+?)\s+backwards",

            # "reverse the word xyz"
            r"reverse\s+the\s+word\s+(.+)",

            # "reverse the string xyz"
            r"reverse\s+the\s+string\s+(.+)",

            # "reverse this string xyz"
            r"reverse\s+this\s+string\s+(.+)",

            # "reverse the text xyz"
            r"reverse\s+the\s+text\s+(.+)",

            # "reverse xyz"
            r"reverse\s+(.+)"
        ]


        text_to_reverse = None


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                text_to_reverse = (
                    match.group(1)
                    .strip()
                    .strip('"\'')
                    .rstrip("?.!")
                )

                break


        # No actual text provided

        if text_to_reverse in [
            "this string",
            "the string",
            "this text",
            "the text"
        ]:

            return "Please provide the text you want me to reverse."


        if text_to_reverse:

            return text_utility(
                "reverse",
                text_to_reverse
            )


    # -----------------------------------------
    # TEXT - WORD COUNT
    # -----------------------------------------

    if (
        "how many words" in text
        or "word count" in text
    ):

        patterns = [

            # "how many words are in this sentence?"
            r"how\s+many\s+words\s+are\s+in\s+(.+)",

            # "how many words in this sentence?"
            r"how\s+many\s+words\s+in\s+(.+)",

            # "what is the word count of this sentence?"
            r"what\s+is\s+the\s+word\s+count\s+of\s+(.+)",

            # "word count of this sentence"
            r"word\s+count\s+of\s+(.+)",

            # "word count: this sentence"
            r"word\s+count\s*[:\-]\s*(.+)"
        ]


        text_to_count = None


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                text_to_count = match.group(1).strip()

                break


        if not text_to_count:

            return "Please provide the sentence you'd like me to count."


        # Remove trailing punctuation

        text_to_count = (
            text_to_count
            .rstrip("?.!")
            .strip()
        )


        # If the user put the actual text in quotation marks,
        # extract only the quoted text.

        quoted_match = re.search(
            r'["\'](.+?)["\']',
            text_to_count
        )


        if quoted_match:

            text_to_count = quoted_match.group(1)


        # The user said "this sentence" but didn't provide one

        if text_to_count.lower() in [
            "this sentence",
            "the sentence",
            "this text",
            "the text"
        ]:

            return "Please provide the sentence you'd like me to count."


        return text_utility(
            "word_count",
            text_to_count
        )


    # -----------------------------------------
    # DEFAULT RESPONSE
    # -----------------------------------------

    return (
        "I'm currently in fallback mode. "
        "I can help with weather, local time, "
        "currency conversion, calculations, "
        "and text utilities."
    )