# backend/agent/restaurant_langgraph/tools.py
"""
LangGraph tools for the Restaurant Booking API.

Each function is decorated with @tool so that create_react_agent will automatically
wrap it as a node in the agent’s graph.
"""

from datetime import date, time
from typing import Any, Dict, Optional

from langchain_core.tools import tool

from clients.restaurant_api import RestaurantAPI
from restaurant_langgraph.utils import handle_api_error

# initialize once
api_client = RestaurantAPI(base_url="http://localhost:8547")


@tool
@handle_api_error
def check_availability(
    restaurant_name: str,
    visit_date: str,
    party_size: int,
    channel_code: str = "ONLINE",
) -> Dict[str, Any]:
    """
    Returns available slots for a given restaurant_name on visit_date (YYYY-MM-DD),
    for party_size people. channel_code is optional.
    """
    try:
        d = date.fromisoformat(visit_date)
    except ValueError:
        return {"error": f"Invalid date: {visit_date}. Use YYYY-MM-DD."}

    return api_client.check_availability(
        restaurant_name=restaurant_name,
        visit_date=d,
        party_size=party_size,
        channel_code=channel_code,
    )


@tool
@handle_api_error
def book_reservation(
    restaurant_name: str,
    visit_date: str,
    visit_time: str,
    party_size: int,
    channel_code: str = "ONLINE",
    special_requests: Optional[str] = None,
    title: Optional[str] = None,
    first_name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    mobile: Optional[str] = None,
    phone: Optional[str] = None,
    mobile_country_code: Optional[str] = None,
    phone_country_code: Optional[str] = None,
    receive_email_marketing: Optional[bool] = None,
    receive_sms_marketing: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Creates a new booking. Requires restaurant_name, visit_date (YYYY-MM-DD),
    visit_time (HH:MM:SS), and party_size.
    Optional: special_requests and detailed customer fields.
    """
    # parse date/time
    try:
        d = date.fromisoformat(visit_date)
    except ValueError:
        return {"error": f"Invalid date: {visit_date}. Use YYYY-MM-DD."}
    try:
        t = time.fromisoformat(visit_time)
    except ValueError:
        return {"error": f"Invalid time: {visit_time}. Use HH:MM:SS."}

    # assemble customer_data in DB format
    customer_data: Dict[str, Any] = {}
    if title:
        customer_data["Title"] = title
    if first_name:
        customer_data["FirstName"] = first_name
    if surname:
        customer_data["Surname"] = surname
    if email:
        customer_data["Email"] = email
    if mobile:
        customer_data["Mobile"] = mobile
    if phone:
        customer_data["Phone"] = phone
    if mobile_country_code:
        customer_data["MobileCountryCode"] = mobile_country_code
    if phone_country_code:
        customer_data["PhoneCountryCode"] = phone_country_code
    if receive_email_marketing is not None:
        customer_data["ReceiveEmailMarketing"] = receive_email_marketing
    if receive_sms_marketing is not None:
        customer_data["ReceiveSmsMarketing"] = receive_sms_marketing

    return api_client.book_reservation(
        restaurant_name=restaurant_name,
        visit_date=d,
        visit_time=t,
        party_size=party_size,
        channel_code=channel_code,
        special_requests=special_requests,
        customer_data=customer_data,
    )

@tool
@handle_api_error
def get_reservation(
    restaurant_name: str,
    booking_reference: str,
) -> Dict[str, Any]:
    """
    Retrieves an existing booking by its booking_reference.
    """
    return api_client.get_booking(
        restaurant_name=restaurant_name,
        booking_reference=booking_reference,
    )


@tool
@handle_api_error
def update_reservation(
    restaurant_name: str,
    booking_reference: str,
    visit_date: Optional[str] = None,
    visit_time: Optional[str] = None,
    party_size: Optional[int] = None,
    special_requests: Optional[str] = None,
    is_leave_time_confirmed: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Updates an existing booking; only provided fields will change.
    """
    kwargs: Dict[str, Any] = {}

    if visit_date:
        try:
            kwargs["visit_date"] = date.fromisoformat(visit_date)
        except ValueError:
            return {"error": f"Invalid date: {visit_date}. Use YYYY-MM-DD."}

    if visit_time:
        try:
            kwargs["visit_time"] = time.fromisoformat(visit_time)
        except ValueError:
            return {"error": f"Invalid time: {visit_time}. Use HH:MM:SS."}

    if party_size is not None:
        kwargs["party_size"] = party_size
    if special_requests is not None:
        kwargs["special_requests"] = special_requests
    if is_leave_time_confirmed is not None:
        kwargs["is_leave_time_confirmed"] = is_leave_time_confirmed

    return api_client.update_booking(
        restaurant_name=restaurant_name,
        booking_reference=booking_reference,
        **kwargs,
    )


@tool
@handle_api_error
def cancel_reservation(
    restaurant_name: str,
    booking_reference: str,
    cancellation_reason_id: int,
) -> Dict[str, Any]:
    """
    Cancels a booking; cancellation_reason_id must be between 1 and 5.
    """
    if not (1 <= cancellation_reason_id <= 5):
        return {"error": "cancellation_reason_id must be between 1 and 5"}

    return api_client.cancel_booking(
        restaurant_name=restaurant_name,
        booking_reference=booking_reference,
        cancellation_reason_id=cancellation_reason_id,
    )
