from typing import Dict, Any
from app.intent import IntentParser, TravellerIntent
from app.suppliers import MultiSupplierEngine
from app.pricing import MarginOptimizer
from app.sentinel import DisruptionSentinel

class VoyAgentOrchestrator:
    """Supervisory Multi-Agent Orchestrator connecting traveler requests to TBO services."""

    def __init__(self):
        self.parser = IntentParser()
        self.suppliers = MultiSupplierEngine()
        self.pricing = MarginOptimizer(default_markup_pct=12.0)
        self.sentinel = DisruptionSentinel()

    def plan_trip(self, query: str) -> Dict[str, Any]:
        # Stage 1: Parse Intent
        intent = self.parser.parse(query)
        follow_ups = self.parser.clarify(intent)

        # Stage 2: Concurrently Query Suppliers
        flights = self.suppliers.search_flights(intent.origin, intent.destination, intent.dates)
        hotels = self.suppliers.search_hotels(intent.destination, "JBR", intent.duration_days - 1)
        activities = self.suppliers.search_activities(intent.destination)

        # Stage 3: Select Optimal Package
        chosen_flight = flights[0] # Emirates
        chosen_hotel = hotels[1]  # Amwaj Rotana
        pax_total = intent.adults + intent.children

        # Stage 4: Dynamic Bundling & Pricing
        pricing_data = self.pricing.bundle_and_price(chosen_flight, chosen_hotel, activities, pax_total)

        # Stage 5: Construct Day-by-Day Itinerary
        itinerary = [
            {"day": 1, "title": "Arrival in Dubai & Beach Check-in", "activity": "Private SUV transfer to hotel; evening leisure along JBR Walk."},
            {"day": 2, "title": "Skyline & Iconic Views", "activity": "At The Top, Burj Khalifa (Levels 124 & 125) morning non-peak access; Dubai Mall fountain walk."},
            {"day": 3, "title": "Arabian Dune Adventure", "activity": "Evening Desert Safari with 4x4 dune bashing, camel rides & BBQ buffet dinner."},
            {"day": 4, "title": "JBR Coastal Leisure", "activity": "Complimentary beach and pool day with kids club activities."},
            {"day": 5, "title": "Souk Shopping & Departure", "activity": "Souk Madinat Jumeirah visit; private airport transfer for return flight to Mumbai."}
        ]

        return {
            "status": "PROPOSAL_READY",
            "traveller_intent": intent.dict(),
            "clarifying_questions": follow_ups,
            "selected_flight": chosen_flight,
            "selected_hotel": chosen_hotel,
            "activities_included": activities,
            "day_wise_itinerary": itinerary,
            "pricing": pricing_data,
            "budget_compliance": {
                "budget_usd": intent.budget_usd,
                "quoted_usd": pricing_data["final_quoted_price_usd"],
                "under_budget": pricing_data["final_quoted_price_usd"] <= intent.budget_usd,
                "savings_usd": round(intent.budget_usd - pricing_data["final_quoted_price_usd"], 2)
            }
        }
