from datetime import datetime
from zoneinfo import ZoneInfo


def get_time(query: str):

    query_lower = query.lower()

    locations = {
        # India
        "india": ("India", "Asia/Kolkata"),
        "hyderabad": ("Hyderabad", "Asia/Kolkata"),
        "vizag": ("Vizag", "Asia/Kolkata"),
        "visakhapatnam": ("Visakhapatnam", "Asia/Kolkata"),
        "delhi": ("Delhi", "Asia/Kolkata"),
        "mumbai": ("Mumbai", "Asia/Kolkata"),
        "chennai": ("Chennai", "Asia/Kolkata"),
        "bangalore": ("Bangalore", "Asia/Kolkata"),
        "bengaluru": ("Bengaluru", "Asia/Kolkata"),
        "kolkata": ("Kolkata", "Asia/Kolkata"),

        # UK
        "london": ("London", "Europe/London"),
        "uk": ("London", "Europe/London"),

        # USA
        "new york": ("New York", "America/New_York"),
        "usa": ("New York", "America/New_York"),
        "chicago": ("Chicago", "America/Chicago"),
        "denver": ("Denver", "America/Denver"),
        "los angeles": ("Los Angeles", "America/Los_Angeles"),
        "california": ("California", "America/Los_Angeles"),

        # Asia
        "tokyo": ("Tokyo", "Asia/Tokyo"),
        "japan": ("Tokyo", "Asia/Tokyo"),
        "singapore": ("Singapore", "Asia/Singapore"),
        "dubai": ("Dubai", "Asia/Dubai"),
        "uae": ("Dubai", "Asia/Dubai"),
    }

    location = "India"
    timezone = "Asia/Kolkata"

    # Find location from query
    for keyword, (name, tz) in locations.items():

        if keyword in query_lower:
            location = name
            timezone = tz
            break

    # Get current time
    current_time = datetime.now(
        ZoneInfo(timezone)
    )

    formatted_time = current_time.strftime("%I:%M %p")

    print(
        f"🕐 Time Tool → {location}: {formatted_time}"
    )

    return {
        "location": location,
        "timezone": timezone,
        "time": formatted_time,
        "snippet": (
            f"Current time in {location}: "
            f"{formatted_time}"
        )
    }