"""
LangGraph Utils for Restaurant Booking Agent.

This module provides shared utilities for the LangGraph agent including
HTTP client setup, error handling decorators, and common validation logic.

Author: AI Assistant
"""

import functools
import requests
from typing import Dict, Any, Callable, Optional
from datetime import date, time


class HTTPClient:
    """
    Shared HTTP client for API requests with consistent configuration.
    
    This class provides a centralized way to make HTTP requests with
    proper authentication, error handling, and session management.
    """
    
    def __init__(self, base_url: str = "http://localhost:8547"):
        """
        Initialize the HTTP client.
        
        Args:
            base_url: Base URL for API requests
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
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response object
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response object
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a PATCH request to the API.
        
        Args:
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response object
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.patch(url, **kwargs)


def handle_api_error(func: Callable) -> Callable:
    """
    Decorator to handle API errors consistently.
    
    This decorator wraps API functions and catches network or HTTP errors,
    returning a consistent error format.
    
    Args:
        func: The function to wrap
        
    Returns:
        Wrapped function that returns {"error": "..."} on failure
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            # Handle HTTP/network errors
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get('detail', str(e))
                except (ValueError, KeyError):
                    error_detail = str(e)
                return {"error": f"API Error ({e.response.status_code}): {error_detail}"}
            else:
                return {"error": f"Network Error: {str(e)}"}
        except Exception as e:
            # Handle any other unexpected errors
            return {"error": f"Unexpected Error: {str(e)}"}
    
    return wrapper


def validate_date(date_str: str) -> Optional[date]:
    """
    Validate and parse a date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        date object if valid, None otherwise
    """
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


def validate_time(time_str: str) -> Optional[time]:
    """
    Validate and parse a time string.
    
    Args:
        time_str: Time string in HH:MM:SS format
        
    Returns:
        time object if valid, None otherwise
    """
    try:
        return time.fromisoformat(time_str)
    except ValueError:
        return None


def validate_party_size(party_size: Any) -> Optional[int]:
    """
    Validate and parse party size.
    
    Args:
        party_size: Party size value
        
    Returns:
        int if valid, None otherwise
    """
    try:
        size = int(party_size)
        if size > 0:
            return size
        return None
    except (ValueError, TypeError):
        return None


def validate_cancellation_reason(reason_id: Any) -> Optional[int]:
    """
    Validate cancellation reason ID.
    
    Args:
        reason_id: Cancellation reason ID
        
    Returns:
        int if valid (1-5), None otherwise
    """
    try:
        reason = int(reason_id)
        if 1 <= reason <= 5:
            return reason
        return None
    except (ValueError, TypeError):
        return None


def parse_boolean(value: Any) -> Optional[bool]:
    """
    Parse a boolean value from various formats.
    
    Args:
        value: Boolean value to parse
        
    Returns:
        bool if valid, None otherwise
    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value.lower() in ['true', '1', 'yes', 'on']
    elif isinstance(value, int):
        return bool(value)
    return None


def extract_customer_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract customer data from parameters.
    
    Args:
        params: Dictionary containing customer parameters
        
    Returns:
        Dictionary with customer data
    """
    customer_fields = [
        'Title', 'FirstName', 'Surname', 'MobileCountryCode', 'Mobile',
        'PhoneCountryCode', 'Phone', 'Email', 'ReceiveEmailMarketing',
        'ReceiveSmsMarketing', 'GroupEmailMarketingOptInText',
        'GroupSmsMarketingOptInText', 'ReceiveRestaurantEmailMarketing',
        'ReceiveRestaurantSmsMarketing', 'RestaurantEmailMarketingOptInText',
        'RestaurantSmsMarketingOptInText'
    ]
    
    customer_data = {}
    for field in customer_fields:
        if field in params:
            customer_data[field] = params[field]
    
    return customer_data


def format_error_response(error_message: str) -> Dict[str, str]:
    """
    Format an error response consistently.
    
    Args:
        error_message: Error message to format
        
    Returns:
        Formatted error response
    """
    return {"error": error_message}


def format_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a success response consistently.
    
    Args:
        data: Response data
        
    Returns:
        Formatted success response
    """
    return {"success": True, "data": data} 