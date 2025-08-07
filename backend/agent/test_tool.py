

from restaurant_langgraph.tools import (
    check_availability,
    book_reservation,
    get_reservation,
    update_reservation,
    cancel_reservation,
)
from datetime import date, time

# Helper to print section headers
def section(title: str):
    print(f"\n=== {title} ===")

# 1. Check Availability via tool.invoke()
section("Check Availability via Tool")
availability = check_availability.invoke({
    "restaurant_name": "TheHungryUnicorn",
    "visit_date": "2025-08-06",
    "party_size": 2
})
print("Result:", availability)

# 2. Book Reservation via tool.invoke()
section("Book Reservation via Tool")
booking = book_reservation.invoke({
    "restaurant_name": "TheHungryUnicorn",
    "visit_date": "2025-08-06",
    "visit_time": "12:00:00",
    "party_size": 2,
    "special_requests": "Window seat"
})
print("Result:", booking)
reference = booking.get("booking_reference") if isinstance(booking, dict) else None

# 3. Get Reservation via tool.invoke()
if reference:
    section("Get Reservation via Tool")
    details = get_reservation.invoke({
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": reference
    })
    print("Result:", details)

# 4. Update Reservation via tool.invoke()
if reference:
    section("Update Reservation via Tool")
    updated = update_reservation.invoke({
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": reference,
        "party_size": 3
    })
    print("Result:", updated)

# 5. Cancel Reservation via tool.invoke()
if reference:
    section("Cancel Reservation via Tool")
    cancelled = cancel_reservation.invoke({
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": reference,
        "cancellation_reason_id": 1
    })
    print("Result:", cancelled)
