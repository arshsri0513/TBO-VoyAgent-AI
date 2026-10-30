import re
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class TravellerIntent(BaseModel):
    destination: str = "Dubai, UAE"
    origin: str = "Mumbai (BOM)"
    dates: str = "Nov 15 - Nov 20, 2026"
    duration_days: int = 5
    adults: int = 2
    children: int = 1
    child_ages: List[int] = [7]
    budget_usd: float = 3500.0
    preferences: List[str] = ["Beachfront Hotel", "JBR area", "Direct Flights", "Desert Safari", "Burj Khalifa"]
    constraints: List[str] = ["Kid-friendly activities", "Non-peak hours"]

class IntentParser:
    """Parses natural language requests into structured travel schemas."""

    def parse(self, query: str) -> TravellerIntent:
        # Structured extraction simulation
        intent = TravellerIntent()
        if "dubai" in query.lower():
            intent.destination = "Dubai, UAE"
        if "mumbai" in query.lower():
            intent.origin = "Mumbai (BOM)"
        if "3500" in query or "3,500" in query or "3200" in query:
            intent.budget_usd = 3200.0
        return intent

    def clarify(self, intent: TravellerIntent) -> List[str]:
        questions = []
        if not intent.child_ages:
            questions.append("Could you confirm the age of the child to match hotel bed policies?")
        if "direct" in " ".join(intent.preferences).lower():
            questions.append("Do you have a preferred departure time slot (e.g., Morning vs Evening flights)?")
        return questions
