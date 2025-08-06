"""
LangGraph Tools for Restaurant Booking API.

This module defines LangGraph Tool objects that wrap the restaurant booking API endpoints,
providing a clean interface for the agent to interact with the booking system.

Author: AI Assistant
"""

from datetime import date, time
from typing import Dict, Any, Optional

from langgraph.agents import Tool
from clients.restaurant_api import RestaurantAPI
from langgraph.utils import handle_api_error

# Initialize the API client
api_client = RestaurantAPI(base_url="http://localhost:8547")


@handle_api_error
def check_availability_tool(params: dict) -> dict:
    """
    Check availability for a restaurant on a specific date.
    
    Args:
        params: Dictionary containing:
            - restaurant_name: Name of the restaurant
            - visit_date: Date in YYYY-MM-DD format
            - party_size: Number of people
            - channel_code: Booking channel (optional, defaults to "ONLINE")
    
    Returns:
        Dict containing availability information or error details
    """
    try:
        restaurant_name = params.get("restaurant_name")
        visit_date_str = params.get("visit_date")
        party_size = params.get("party_size")
        channel_code = params.get("channel_code", "ONLINE")
        
        if not all([restaurant_name, visit_date_str, party_size]):
            return {"error": "Missing required parameters: restaurant_name, visit_date, party_size"}
        
        # Parse date
        try:
            visit_date = date.fromisoformat(visit_date_str)
        except ValueError:
            return {"error": f"Invalid date format: {visit_date_str}. Use YYYY-MM-DD format"}
        
        # Parse party size
        try:
            party_size = int(party_size)
        except (ValueError, TypeError):
            return {"error": f"Invalid party size: {party_size}. Must be a number"}
        
        result = api_client.check_availability(
            restaurant_name=restaurant_name,
            visit_date=visit_date,
            party_size=party_size,
            channel_code=channel_code
        )
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


@handle_api_error
def book_reservation_tool(params: dict) -> dict:
    """
    Create a new restaurant booking.
    
    Args:
        params: Dictionary containing:
            - restaurant_name: Name of the restaurant
            - visit_date: Date in YYYY-MM-DD format
            - visit_time: Time in HH:MM:SS format
            - party_size: Number of people
            - channel_code: Booking channel (optional, defaults to "ONLINE")
            - special_requests: Special requests (optional)
            - is_leave_time_confirmed: Boolean for time confirmation (optional)
            - room_number: Room/table number (optional)
            - customer_data: Dictionary of customer information (optional)
    
    Returns:
        Dict containing booking information or error details
    """
    try:
        restaurant_name = params.get("restaurant_name")
        visit_date_str = params.get("visit_date")
        visit_time_str = params.get("visit_time")
        party_size = params.get("party_size")
        channel_code = params.get("channel_code", "ONLINE")
        special_requests = params.get("special_requests")
        is_leave_time_confirmed = params.get("is_leave_time_confirmed")
        room_number = params.get("room_number")
        customer_data = params.get("customer_data", {})
        
        if not all([restaurant_name, visit_date_str, visit_time_str, party_size]):
            return {"error": "Missing required parameters: restaurant_name, visit_date, visit_time, party_size"}
        
        # Parse date
        try:
            visit_date = date.fromisoformat(visit_date_str)
        except ValueError:
            return {"error": f"Invalid date format: {visit_date_str}. Use YYYY-MM-DD format"}
        
        # Parse time
        try:
            visit_time = time.fromisoformat(visit_time_str)
        except ValueError:
            return {"error": f"Invalid time format: {visit_time_str}. Use HH:MM:SS format"}
        
        # Parse party size
        try:
            party_size = int(party_size)
        except (ValueError, TypeError):
            return {"error": f"Invalid party size: {party_size}. Must be a number"}
        
        # Parse boolean fields
        if is_leave_time_confirmed is not None:
            if isinstance(is_leave_time_confirmed, str):
                is_leave_time_confirmed = is_leave_time_confirmed.lower() in ['true', '1', 'yes']
        
        result = api_client.book_reservation(
            restaurant_name=restaurant_name,
            visit_date=visit_date,
            visit_time=visit_time,
            party_size=party_size,
            channel_code=channel_code,
            special_requests=special_requests,
            is_leave_time_confirmed=is_leave_time_confirmed,
            room_number=room_number,
            customer_data=customer_data
        )
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


@handle_api_error
def get_reservation_tool(params: dict) -> dict:
    """
    Get details of an existing booking.
    
    Args:
        params: Dictionary containing:
            - restaurant_name: Name of the restaurant
            - booking_reference: Unique booking reference
    
    Returns:
        Dict containing booking details or error details
    """
    try:
        restaurant_name = params.get("restaurant_name")
        booking_reference = params.get("booking_reference")
        
        if not all([restaurant_name, booking_reference]):
            return {"error": "Missing required parameters: restaurant_name, booking_reference"}
        
        result = api_client.get_booking(
            restaurant_name=restaurant_name,
            booking_reference=booking_reference
        )
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


@handle_api_error
def update_reservation_tool(params: dict) -> dict:
    """
    Update an existing booking.
    
    Args:
        params: Dictionary containing:
            - restaurant_name: Name of the restaurant
            - booking_reference: Unique booking reference
            - visit_date: New date in YYYY-MM-DD format (optional)
            - visit_time: New time in HH:MM:SS format (optional)
            - party_size: New party size (optional)
            - special_requests: Updated special requests (optional)
            - is_leave_time_confirmed: Updated time confirmation (optional)
    
    Returns:
        Dict containing update information or error details
    """
    try:
        restaurant_name = params.get("restaurant_name")
        booking_reference = params.get("booking_reference")
        visit_date_str = params.get("visit_date")
        visit_time_str = params.get("visit_time")
        party_size = params.get("party_size")
        special_requests = params.get("special_requests")
        is_leave_time_confirmed = params.get("is_leave_time_confirmed")
        
        if not all([restaurant_name, booking_reference]):
            return {"error": "Missing required parameters: restaurant_name, booking_reference"}
        
        # Parse optional date
        visit_date = None
        if visit_date_str:
            try:
                visit_date = date.fromisoformat(visit_date_str)
            except ValueError:
                return {"error": f"Invalid date format: {visit_date_str}. Use YYYY-MM-DD format"}
        
        # Parse optional time
        visit_time = None
        if visit_time_str:
            try:
                visit_time = time.fromisoformat(visit_time_str)
            except ValueError:
                return {"error": f"Invalid time format: {visit_time_str}. Use HH:MM:SS format"}
        
        # Parse optional party size
        if party_size is not None:
            try:
                party_size = int(party_size)
            except (ValueError, TypeError):
                return {"error": f"Invalid party size: {party_size}. Must be a number"}
        
        # Parse optional boolean field
        if is_leave_time_confirmed is not None:
            if isinstance(is_leave_time_confirmed, str):
                is_leave_time_confirmed = is_leave_time_confirmed.lower() in ['true', '1', 'yes']
        
        result = api_client.update_booking(
            restaurant_name=restaurant_name,
            booking_reference=booking_reference,
            visit_date=visit_date,
            visit_time=visit_time,
            party_size=party_size,
            special_requests=special_requests,
            is_leave_time_confirmed=is_leave_time_confirmed
        )
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


@handle_api_error
def cancel_reservation_tool(params: dict) -> dict:
    """
    Cancel an existing booking.
    
    Args:
        params: Dictionary containing:
            - restaurant_name: Name of the restaurant
            - booking_reference: Unique booking reference
            - cancellation_reason_id: ID of cancellation reason (1-5)
    
    Returns:
        Dict containing cancellation information or error details
    """
    try:
        restaurant_name = params.get("restaurant_name")
        booking_reference = params.get("booking_reference")
        cancellation_reason_id = params.get("cancellation_reason_id")
        
        if not all([restaurant_name, booking_reference, cancellation_reason_id]):
            return {"error": "Missing required parameters: restaurant_name, booking_reference, cancellation_reason_id"}
        
        # Parse cancellation reason ID
        try:
            cancellation_reason_id = int(cancellation_reason_id)
            if not 1 <= cancellation_reason_id <= 5:
                return {"error": "Cancellation reason ID must be between 1 and 5"}
        except (ValueError, TypeError):
            return {"error": f"Invalid cancellation reason ID: {cancellation_reason_id}. Must be a number between 1-5"}
        
        result = api_client.cancel_booking(
            restaurant_name=restaurant_name,
            booking_reference=booking_reference,
            cancellation_reason_id=cancellation_reason_id
        )
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


# Define LangGraph Tools
check_availability = Tool(
    name="check_availability",
    func=check_availability_tool,
    description="Returns available slots given restaurant, date, party size, and channel."
)

book_reservation = Tool(
    name="book_reservation",
    func=book_reservation_tool,
    description="Creates a new restaurant booking with customer information and preferences."
)

get_reservation = Tool(
    name="get_reservation",
    func=get_reservation_tool,
    description="Retrieves complete booking information by booking reference."
)

update_reservation = Tool(
    name="update_reservation",
    func=update_reservation_tool,
    description="Modifies an existing booking with new date, time, party size, or special requests."
)

cancel_reservation = Tool(
    name="cancel_reservation",
    func=cancel_reservation_tool,
    description="Cancels an existing booking with a specified reason."
) 