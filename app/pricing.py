from typing import Dict, Any

class MarginOptimizer:
    """Calculates agent commissions, dynamic markups, and currency conversions."""

    def __init__(self, default_markup_pct: float = 12.0):
        self.markup_pct = default_markup_pct

    def bundle_and_price(self, flight: Dict[str, Any], hotel: Dict[str, Any], activities: list, pax_count: int) -> Dict[str, Any]:
        flight_cost = flight["price_usd"] * pax_count
        hotel_cost = hotel["total_usd"]
        activity_cost = sum(a.get("price_per_pax_usd", 0) * pax_count for a in activities if "price_per_pax_usd" in a)
        transfer_cost = sum(a.get("price_usd", 0) for a in activities if "price_usd" in a)

        net_supplier_total = flight_cost + hotel_cost + activity_cost + transfer_cost
        agency_markup = round(net_supplier_total * (self.markup_pct / 100.0), 2)
        gross_client_price = round(net_supplier_total + agency_markup, 2)

        return {
            "net_supplier_cost_usd": net_supplier_total,
            "agency_margin_pct": self.markup_pct,
            "agency_commission_usd": agency_markup,
            "final_quoted_price_usd": gross_client_price,
            "cost_breakdown": {
                "flights": flight_cost,
                "hotel": hotel_cost,
                "sightseeing": activity_cost,
                "transfers": transfer_cost
            }
        }
