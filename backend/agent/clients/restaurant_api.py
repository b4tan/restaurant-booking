import os
import httpx
from datetime import date, time
from typing import Any, Dict, Optional


class RestaurantAPI:
    """
    HTTP client for interacting with the Restaurant Booking API.
    Wraps the mock server endpoints under /api/ConsumerApi/v1.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        token: Optional[str] = None,
    ):
        # Normalize base_url, strip trailing slash
        self.base_url = base_url.rstrip('/')
        # Use provided token, env var, or fallback mock token
        token = token or os.getenv("RESTAURANT_API_TOKEN") or (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1bmlxdWVfbmFtZSI6ImFwcGVsbGErYXBpQHJlc2RpYXJ5LmNvbSIsIm5iZiI6MTc1NDQzMDgwNSwiZXhwIjoxNzU0NTE3MjA1LCJpYXQiOjE3NTQ0MzA4MDUsImlzcyI6IlNlbGYiLCJhdWQiOiJodHRwczovL2FwaS5yZXNkaWFyeS5jb20ifQ."
            "g3yLsufdk8Fn2094SB3J3XW-KdBc0DY9a2Jiu_56ud8"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=headers,
        )

    def check_availability(
        self,
        restaurant_name: str,
        visit_date: date,
        party_size: int,
        channel_code: str = 'ONLINE',
    ) -> Dict[str, Any]:
        """
        POST /api/ConsumerApi/v1/Restaurant/{restaurant_name}/AvailabilitySearch

        Returns available time slots for a given date and party size.
        """
        endpoint = (
            f"/api/ConsumerApi/v1/Restaurant/{restaurant_name}"
            "/AvailabilitySearch"
        )
        form_data = {
            'VisitDate': visit_date.isoformat(),
            'PartySize': party_size,
            'ChannelCode': channel_code,
        }
        resp = self.client.post(endpoint, data=form_data)
        resp.raise_for_status()
        return resp.json()

    def book_reservation(
        self,
        restaurant_name: str,
        visit_date: date,
        visit_time: time,
        party_size: int,
        channel_code: str = 'ONLINE',
        special_requests: Optional[str] = None,
        is_leave_time_confirmed: Optional[bool] = None,
        room_number: Optional[str] = None,
        customer_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        POST /api/ConsumerApi/v1/Restaurant/{restaurant_name}/BookingWithStripeToken

        Creates a new booking and returns confirmation details.
        """
        endpoint = (
            f"/api/ConsumerApi/v1/Restaurant/{restaurant_name}"
            "/BookingWithStripeToken"
        )
        form_data: Dict[str, Any] = {
            'VisitDate': visit_date.isoformat(),
            'VisitTime': visit_time.isoformat(),
            'PartySize': party_size,
            'ChannelCode': channel_code,
        }
        if special_requests is not None:
            form_data['SpecialRequests'] = special_requests
        if is_leave_time_confirmed is not None:
            form_data['IsLeaveTimeConfirmed'] = str(is_leave_time_confirmed)
        if room_number is not None:
            form_data['RoomNumber'] = room_number
        if customer_data:
            for key, val in customer_data.items():
                form_data[f"Customer[{key}]"] = val

        resp = self.client.post(endpoint, data=form_data)
        resp.raise_for_status()
        return resp.json()

    def get_booking(
        self,
        restaurant_name: str,
        booking_reference: str,
    ) -> Dict[str, Any]:
        """
        GET /api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}

        Retrieves existing booking details.
        """
        endpoint = (
            f"/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/"
            f"{booking_reference}"
        )
        resp = self.client.get(endpoint)
        resp.raise_for_status()
        return resp.json()

    def update_booking(
        self,
        restaurant_name: str,
        booking_reference: str,
        visit_date: Optional[date] = None,
        visit_time: Optional[time] = None,
        party_size: Optional[int] = None,
        special_requests: Optional[str] = None,
        is_leave_time_confirmed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        PATCH /api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}

        Updates fields on an existing booking.
        """
        endpoint = (
            f"/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/"
            f"{booking_reference}"
        )
        form_data: Dict[str, Any] = {}
        if visit_date:
            form_data['VisitDate'] = visit_date.isoformat()
        if visit_time:
            form_data['VisitTime'] = visit_time.isoformat()
        if party_size is not None:
            form_data['PartySize'] = party_size
        if special_requests is not None:
            form_data['SpecialRequests'] = special_requests
        if is_leave_time_confirmed is not None:
            form_data['IsLeaveTimeConfirmed'] = str(is_leave_time_confirmed)

        resp = self.client.patch(endpoint, data=form_data)
        resp.raise_for_status()
        return resp.json()

    def cancel_booking(
        self,
        restaurant_name: str,
        booking_reference: str,
        cancellation_reason_id: int,
    ) -> Dict[str, Any]:
        """
        POST /api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}/Cancel

        Cancels an existing booking with a specific reason.
        """
        endpoint = (
            f"/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/"
            f"{booking_reference}/Cancel"
        )
        form_data = {
            'micrositeName': restaurant_name,
            'bookingReference': booking_reference,
            'cancellationReasonId': cancellation_reason_id,
        }
        resp = self.client.post(endpoint, data=form_data)
        resp.raise_for_status()
        return resp.json()
