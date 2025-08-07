from clients.restaurant_api import RestaurantAPI
from datetime import date, time

# Initialize client (ensure mock server is running on port 8547)
client = RestaurantAPI(base_url="http://localhost:8547")

# Helper to print section headers
def section(title: str):
    print(f"\n=== {title} ===")

# 1. Check Availability
section("Check Availability")
try:
    availability = client.check_availability(
        restaurant_name="TheHungryUnicorn",
        visit_date=date(2025, 8, 6),
        party_size=2
    )
    print("Success:", availability)
except Exception as e:
    print("Error during availability check:", e)

# 2. Book Reservation
section("Book Reservation")
reference = None
try:
    booking = client.book_reservation(
        restaurant_name="TheHungryUnicorn",
        visit_date=date(2025, 8, 6),
        visit_time=time(12, 0),
        party_size=2,
        special_requests="Window seat"
    )
    print("Success:", booking)
    reference = booking.get("booking_reference")
except Exception as e:
    print("Error during booking:", e)

# 3. Get Booking Details
if reference:
    section("Get Booking Details")
    try:
        details = client.get_booking(
            restaurant_name="TheHungryUnicorn",
            booking_reference=reference
        )
        print("Success:", details)
    except Exception as e:
        print("Error during get booking:", e)

# 4. Update Booking
if reference:
    section("Update Booking")
    try:
        updated = client.update_booking(
            restaurant_name="TheHungryUnicorn",
            booking_reference=reference,
            party_size=3
        )
        print("Success:", updated)
    except Exception as e:
        print("Error during update booking:", e)

# 5. Cancel Booking
if reference:
    section("Cancel Booking")
    try:
        canceled = client.cancel_booking(
            restaurant_name="TheHungryUnicorn",
            booking_reference=reference,
            cancellation_reason_id=1
        )
        print("Success:", canceled)
    except Exception as e:
        print("Error during cancellation:", e)
