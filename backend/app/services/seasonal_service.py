from datetime import date, timedelta


UK_EVENTS = [
    {"name": "New Year", "month": 1, "day": 1, "duration": 7},
    {"name": "Valentine's Day", "month": 2, "day": 14, "duration": 14},
    {"name": "Mother's Day", "month": 3, "day": 10, "duration": 14, "variable": True},
    {"name": "St Patrick's Day", "month": 3, "day": 17, "duration": 7},
    {"name": "Easter", "month": 4, "day": 1, "duration": 14, "variable": True},
    {"name": "St George's Day", "month": 4, "day": 23, "duration": 7},
    {"name": "Early May Bank Holiday", "month": 5, "day": 6, "duration": 7, "variable": True},
    {"name": "Spring Bank Holiday", "month": 5, "day": 27, "duration": 7, "variable": True},
    {"name": "Father's Day", "month": 6, "day": 16, "duration": 14, "variable": True},
    {"name": "Summer Holidays", "month": 7, "day": 20, "duration": 45},
    {"name": "Summer Bank Holiday", "month": 8, "day": 26, "duration": 7, "variable": True},
    {"name": "Back to School", "month": 9, "day": 1, "duration": 14},
    {"name": "Halloween", "month": 10, "day": 31, "duration": 21},
    {"name": "Bonfire Night", "month": 11, "day": 5, "duration": 14},
    {"name": "Black Friday", "month": 11, "day": 29, "duration": 7, "variable": True},
    {"name": "Christmas", "month": 12, "day": 25, "duration": 30},
    {"name": "Boxing Day Sales", "month": 12, "day": 26, "duration": 7},
    {"name": "New Year's Eve", "month": 12, "day": 31, "duration": 7},
]

UK_SEASONS = [
    {"name": "Spring", "start_month": 3, "end_month": 5},
    {"name": "Summer", "start_month": 6, "end_month": 8},
    {"name": "Autumn", "start_month": 9, "end_month": 11},
    {"name": "Winter", "start_month": 12, "end_month": 2},
]


def get_current_season(today: date = None) -> str:
    if today is None:
        today = date.today()

    month = today.month

    for season in UK_SEASONS:
        start = season["start_month"]
        end = season["end_month"]

        if start <= end:
            if start <= month <= end:
                return season["name"]
        else:
            if month >= start or month <= end:
                return season["name"]

    return "Winter"


def get_upcoming_events(today: date = None, days_ahead: int = 60) -> list[dict]:
    if today is None:
        today = date.today()

    upcoming = []
    end_date = today + timedelta(days=days_ahead)

    for event in UK_EVENTS:
        try:
            event_date = date(today.year, event["month"], event["day"])
        except ValueError:
            event_date = date(today.year, event["month"], 28)

        if event_date < today:
            try:
                event_date = date(today.year + 1, event["month"], event["day"])
            except ValueError:
                event_date = date(today.year + 1, event["month"], 28)

        lead_time = event_date - timedelta(days=event["duration"])

        if lead_time <= today <= event_date or today <= event_date <= end_date:
            days_until = (event_date - today).days
            upcoming.append({
                "name": event["name"],
                "date": event_date.isoformat(),
                "days_until": days_until,
                "is_active": lead_time <= today <= event_date,
                "marketing_window": event["duration"],
            })

    upcoming.sort(key=lambda x: x["days_until"])
    return upcoming


def get_seasonal_suggestions(today: date = None) -> dict:
    if today is None:
        today = date.today()

    current_season = get_current_season(today)
    upcoming_events = get_upcoming_events(today)

    active_events = [e for e in upcoming_events if e["is_active"]]
    future_events = [e for e in upcoming_events if not e["is_active"]][:5]

    suggestions = []

    if active_events:
        for event in active_events:
            suggestions.append({
                "hook": event["name"],
                "reason": f"Currently in marketing window ({event['days_until']} days until event)",
                "priority": "high",
            })

    suggestions.append({
        "hook": current_season,
        "reason": f"Current season - use seasonal themes and imagery",
        "priority": "medium",
    })

    for event in future_events[:3]:
        suggestions.append({
            "hook": event["name"],
            "reason": f"Coming up in {event['days_until']} days - start planning",
            "priority": "low" if event["days_until"] > 30 else "medium",
        })

    return {
        "current_season": current_season,
        "active_events": active_events,
        "upcoming_events": future_events,
        "suggestions": suggestions,
    }
