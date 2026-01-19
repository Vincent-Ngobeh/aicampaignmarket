from pydantic import BaseModel


class Event(BaseModel):
    name: str
    date: str
    days_until: int
    is_active: bool
    marketing_window: int


class Suggestion(BaseModel):
    hook: str
    reason: str
    priority: str


class SeasonalResponse(BaseModel):
    success: bool = True
    current_season: str
    active_events: list[Event]
    upcoming_events: list[Event]
    suggestions: list[Suggestion]
