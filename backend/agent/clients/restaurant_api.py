"""
Restaurant API Client.

This module provides a client wrapper around the restaurant booking API endpoints,
handling authentication, request formatting, and response parsing.

Author: AI Assistant
"""

import requests
from datetime import date, time
from typing import Dict, Any, Optional


class RestaurantAPI:
    """
    Client for interacting with the restaurant booking API.
    
    This class provides methods to interact with all restaurant booking endpoints,
    handling authentication and request formatting automatically.
    """
    
    def __init__(self, base_url: str = "http://localhost:8547"):
        """
        Initialize the RestaurantAPI client.
        
        Args:
            base_url: Base URL for the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Fixed mock bearer token for authentication
        self.auth_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImFwcGVsbGErYXBpQHJlc2"
            "RpYXJ5LmNvbSIsIm5iZiI6MTc1NDQzMDgwNSwiZXhwIjoxNzU0NTE3MjA1LCJpYXQiOjE3NTQ0MzA4"
            "MDUsImlzcyI6IlNlbGYiLCJhdWQiOiJodHRwczovL2FwaS5yZXNkaWFyeS5jb20ifQ.g3yLsufdk8Fn"
            "2094SB3J3XW-KdBc0DY9a2Jiu_56ud8"
        )
        
        # Set default headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def check_availability(
        self, 
        restaurant_name: str, 
        visit_date: date, 
        party_size: int, 
        channel_code: str = "ONLINE"
    ) -> Dict[str, Any]:
        """
        Check availability for a restaurant on a specific date.
        
        Args:
            restaurant_name: Name of the restaurant
            visit_date: Date to check availability for
            party_size: Number of people in the party
            channel_code: Booking channel (default: "ONLINE")
            
        Returns:
            Dict containing availability information
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{restaurant_name}/AvailabilitySearch"
        
        data = {
            'VisitDate': visit_date.strftime('%Y-%m-%d'),
            'PartySize': party_size,
            'ChannelCode': channel_code
        }
        
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    
    def book_reservation(
        self,
        restaurant_name: str,
        visit_date: date,
        visit_time: time,
        party_size: int,
        channel_code: str = "ONLINE",
        special_requests: Optional[str] = None,
        is_leave_time_confirmed: Optional[bool] = None,
        room_number: Optional[str] = None,
        customer_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new restaurant booking.
        
        Args:
            restaurant_name: Name of the restaurant
            visit_date: Date of the visit
            visit_time: Time of the visit
            party_size: Number of people in the party
            channel_code: Booking channel (default: "ONLINE")
            special_requests: Special requests for the booking
            is_leave_time_confirmed: Whether leave time is confirmed
            room_number: Specific room/table number
            customer_data: Customer information dictionary
            
        Returns:
            Dict containing booking information
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{restaurant_name}/BookingWithStripeToken"
        
        data = {
            'VisitDate': visit_date.strftime('%Y-%m-%d'),
            'VisitTime': visit_time.strftime('%H:%M:%S'),
            'PartySize': party_size,
            'ChannelCode': channel_code
        }
        
        # Add optional fields
        if special_requests:
            data['SpecialRequests'] = special_requests
        if is_leave_time_confirmed is not None:
            data['IsLeaveTimeConfirmed'] = is_leave_time_confirmed
        if room_number:
            data['RoomNumber'] = room_number
            
        # Add customer data if provided
        if customer_data:
            for key, value in customer_data.items():
                if value is not None:
                    data[f'Customer[{key}]'] = value
        
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    
    def get_booking(
        self, 
        restaurant_name: str, 
        booking_reference: str
    ) -> Dict[str, Any]:
        """
        Get details of an existing booking.
        
        Args:
            restaurant_name: Name of the restaurant
            booking_reference: Unique booking reference
            
        Returns:
            Dict containing booking details
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def update_booking(
        self,
        restaurant_name: str,
        booking_reference: str,
        visit_date: Optional[date] = None,
        visit_time: Optional[time] = None,
        party_size: Optional[int] = None,
        special_requests: Optional[str] = None,
        is_leave_time_confirmed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update an existing booking.
        
        Args:
            restaurant_name: Name of the restaurant
            booking_reference: Unique booking reference
            visit_date: New visit date
            visit_time: New visit time
            party_size: New party size
            special_requests: Updated special requests
            is_leave_time_confirmed: Updated leave time confirmation
            
        Returns:
            Dict containing update information
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}"
        
        data = {}
        
        # Add only provided fields
        if visit_date:
            data['VisitDate'] = visit_date.strftime('%Y-%m-%d')
        if visit_time:
            data['VisitTime'] = visit_time.strftime('%H:%M:%S')
        if party_size:
            data['PartySize'] = party_size
        if special_requests:
            data['SpecialRequests'] = special_requests
        if is_leave_time_confirmed is not None:
            data['IsLeaveTimeConfirmed'] = is_leave_time_confirmed
        
        response = self.session.patch(url, data=data)
        response.raise_for_status()
        return response.json()
    
    def cancel_booking(
        self, 
        restaurant_name: str, 
        booking_reference: str, 
        cancellation_reason_id: int
    ) -> Dict[str, Any]:
        """
        Cancel an existing booking.
        
        Args:
            restaurant_name: Name of the restaurant
            booking_reference: Unique booking reference
            cancellation_reason_id: ID of the cancellation reason (1-5)
            
        Returns:
            Dict containing cancellation information
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/api/ConsumerApi/v1/Restaurant/{restaurant_name}/Booking/{booking_reference}/Cancel"
        
        data = {
            'micrositeName': restaurant_name,
            'bookingReference': booking_reference,
            'cancellationReasonId': cancellation_reason_id
        }
        
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json() 