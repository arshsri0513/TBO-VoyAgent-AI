import sys
import json
import time
from app.agent import VoyAgentOrchestrator

def main():
    print("=" * 70)
    print("  VOYAGENT AI - AUTONOMOUS B2B TRAVEL COPILOT (TBO.COM)")
    print("  CRP - VoyageHack 4.0 | Track: Virtual travel Agent/copilot")
    print("=" * 70)

    agent = VoyAgentOrchestrator()

    # Scenario 1: Itinerary Generation
    query = (
        "Family holiday to Dubai, 2 adults + 1 child (age 7), Nov 15-20, budget $3,200. "
        "Direct flights from Mumbai, beachfront hotel near JBR, include Burj Khalifa & Desert Safari."
    )
    print(f"\n[TRAVELER QUERY]:\n\"{query}\"")
    print("\n>>> Orchestrating Multi-Agent Workers...")

    start_time = time.time()
    result = agent.plan_trip(query)
    elapsed = time.time() - start_time

    print(f"\n[EXECUTION COMPLETED in {elapsed:.2f}s]")
    print(f"- Destination: {result['traveller_intent']['destination']}")
    print(f"- Selected Hotel: {result['selected_hotel']['name']} ({result['selected_hotel']['room_type']})")
    print(f"- Selected Flight: {result['selected_flight']['airline']} ({result['selected_flight']['flight_no']})")
    print(f"- Net Supplier Cost: ${result['pricing']['net_supplier_cost_usd']}")
    print(f"- Agency Commission (+{result['pricing']['agency_margin_pct']}%): ${result['pricing']['agency_commission_usd']}")
    print(f"- Final Quoted Package: ${result['pricing']['final_quoted_price_usd']}")
    print(f"- Budget Headroom: ${result['budget_compliance']['savings_usd']} (Under Budget: {result['budget_compliance']['under_budget']})")

    print("\n[DAY-BY-DAY ITINERARY]")
    for day in result["day_wise_itinerary"]:
        print(f"  Day {day['day']}: {day['title']} -> {day['activity']}")

    # Scenario 2: Autonomous Disruption Recovery
    print("\n" + "=" * 70)
    print("  TRIGGERING GDS AIRLINE WEBHOOK: FLIGHT DELAY SIMULATION")
    print("=" * 70)
    print(">>> Webhook Received: EK 501 delayed by 5.0 hours (New Dept: 03:00 PM)")

    recovery = agent.sentinel.handle_flight_reschedule(
        pnr="TBO-DXB-98421",
        original_dept="10:00 AM",
        new_dept="03:00 PM",
        delay_hours=5.0
    )

    print(f"\n[AUTONOMOUS SENTINEL STATUS]: {recovery['status']}")
    for action in recovery["actions"]:
        print(f"  [AUTO-{action['action']}] {action['service']}: {action['details']} -> ({action['status']})")

    print("\n>>> Simulation complete! 100% disruption handled without human ops intervention.")

if __name__ == "__main__":
    main()
