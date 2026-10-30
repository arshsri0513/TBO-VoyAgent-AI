import time
from typing import Dict, Any, List

class MultiSupplierEngine:
    """Simulates TBO Core API Connectors (GDS Flights, Hotel Bedbanks, Tours) with Look-to-Book Caching."""

    def __init__(self):
        self.cache = {}
        self.cache_hits = 0
        self.api_calls = 0

    def search_flights(self, origin: str, destination: str, dates: str) -> List[Dict[str, Any]]:
        cache_key = f"flight:{origin}:{destination}:{dates}"
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]

        self.api_calls += 1
        results = [
            {
                "id": "FL-EK-501",
                "airline": "Emirates",
                "flight_no": "EK 501",
                "origin": origin,
                "destination": destination,
                "dept_time": "10:00 AM",
                "arr_time": "12:15 PM",
                "duration": "3h 45m",
                "direct": True,
                "price_usd": 420.0,
                "currency": "USD",
                "seats_available": 9
            },
            {
                "id": "FL-AI-995",
                "airline": "Air India",
                "flight_no": "AI 995",
                "origin": origin,
                "destination": destination,
                "dept_time": "08:15 AM",
                "arr_time": "10:30 AM",
                "duration": "3h 45m",
                "direct": True,
                "price_usd": 380.0,
                "currency": "USD",
                "seats_available": 5
            }
        ]
        self.cache[cache_key] = results
        return results

    def search_hotels(self, destination: str, area: str, nights: int) -> List[Dict[str, Any]]:
        cache_key = f"hotel:{destination}:{area}:{nights}"
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]

        self.api_calls += 1
        results = [
            {
                "id": "HT-JBR-01",
                "name": "Hilton Dubai Jumeirah Beach",
                "location": "JBR Walk, Dubai",
                "stars": 5,
                "room_type": "Deluxe Sea View (Free Cancellation)",
                "rate_per_night_usd": 280.0,
                "total_usd": 280.0 * nights,
                "amenities": ["Private Beach", "Kids Club", "Pool", "Breakfast Included"],
                "supplier": "Hotelbeds / TBO Direct"
            },
            {
                "id": "HT-JBR-02",
                "name": "Amwaj Rotana JBR",
                "location": "The Walk, JBR",
                "stars": 4,
                "room_type": "Family Sea Front Room",
                "rate_per_night_usd": 220.0,
                "total_usd": 220.0 * nights,
                "amenities": ["Direct Beach Access", "Kids Pool", "Free WiFi"],
                "supplier": "WebBeds / TBO Hub"
            }
        ]
        self.cache[cache_key] = results
        return results

    def search_activities(self, destination: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": "ACT-BURJ-124",
                "name": "At the Top - Burj Khalifa (Levels 124 & 125)",
                "recommended_time": "10:00 AM (Non-peak slot)",
                "duration": "2.5 hours",
                "price_per_pax_usd": 48.0,
                "cancellation": "Free up to 24h prior"
            },
            {
                "id": "ACT-DESERT-4X4",
                "name": "Premium Evening Desert Safari & BBQ Dinner",
                "recommended_time": "03:30 PM Pickup",
                "duration": "6 hours",
                "price_per_pax_usd": 75.0,
                "inclusions": ["4x4 Dune Bashing", "Camel Ride", "Buffet Dinner", "Kid buggy"]
            },
            {
                "id": "TRF-PVT-SUV",
                "name": "Private Airport Return Transfers (DXB <-> JBR)",
                "type": "Private Luxury SUV",
                "capacity": "4 Passengers + 4 Luggage",
                "price_usd": 90.0
            }
        ]
