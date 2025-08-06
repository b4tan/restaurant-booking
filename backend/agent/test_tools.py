"""
Test script for LangGraph tools.

This script tests the restaurant booking tools to ensure they work correctly
with the mock API server.

Author: AI Assistant
"""

from datetime import date, time

# Import our tools
from langgraph.tools import check_availability, book_reservation, get_reservation, update_reservation, cancel_reservation


def test_check_availability():
    """Test the check_availability tool."""
    print("Testing check_availability tool...")
    
    params = {
        "restaurant_name": "TheHungryUnicorn",
        "visit_date": "2025-01-15",
        "party_size": 4,
        "channel_code": "ONLINE"
    }
    
    result = check_availability.func(params)
    print(f"Result: {result}")
    return result


def test_book_reservation():
    """Test the book_reservation tool."""
    print("\nTesting book_reservation tool...")
    
    params = {
        "restaurant_name": "TheHungryUnicorn",
        "visit_date": "2025-01-15",
        "visit_time": "19:00:00",
        "party_size": 4,
        "channel_code": "ONLINE",
        "special_requests": "Window table please",
        "customer_data": {
            "FirstName": "John",
            "Surname": "Doe",
            "Email": "john.doe@example.com",
            "Mobile": "1234567890"
        }
    }
    
    result = book_reservation.func(params)
    print(f"Result: {result}")
    return result


def test_get_reservation():
    """Test the get_reservation tool."""
    print("\nTesting get_reservation tool...")
    
    # First create a booking to get a reference
    booking_result = test_book_reservation()
    if "error" in booking_result:
        print("Skipping get_reservation test due to booking error")
        return
    
    booking_reference = booking_result.get("booking_reference")
    if not booking_reference:
        print("No booking reference found, skipping test")
        return
    
    params = {
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": booking_reference
    }
    
    result = get_reservation.func(params)
    print(f"Result: {result}")
    return result


def test_update_reservation():
    """Test the update_reservation tool."""
    print("\nTesting update_reservation tool...")
    
    # First create a booking to get a reference
    booking_result = test_book_reservation()
    if "error" in booking_result:
        print("Skipping update_reservation test due to booking error")
        return
    
    booking_reference = booking_result.get("booking_reference")
    if not booking_reference:
        print("No booking reference found, skipping test")
        return
    
    params = {
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": booking_reference,
        "party_size": 6,
        "special_requests": "Updated special requests"
    }
    
    result = update_reservation.func(params)
    print(f"Result: {result}")
    return result


def test_cancel_reservation():
    """Test the cancel_reservation tool."""
    print("\nTesting cancel_reservation tool...")
    
    # First create a booking to get a reference
    booking_result = test_book_reservation()
    if "error" in booking_result:
        print("Skipping cancel_reservation test due to booking error")
        return
    
    booking_reference = booking_result.get("booking_reference")
    if not booking_reference:
        print("No booking reference found, skipping test")
        return
    
    params = {
        "restaurant_name": "TheHungryUnicorn",
        "booking_reference": booking_reference,
        "cancellation_reason_id": 1
    }
    
    result = cancel_reservation.func(params)
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    print("Testing LangGraph Restaurant Booking Tools")
    print("=" * 50)
    
    # Test all tools
    test_check_availability()
    test_book_reservation()
    test_get_reservation()
    test_update_reservation()
    test_cancel_reservation()
    
    print("\n" + "=" * 50)
    print("Testing complete!") 