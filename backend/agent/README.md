# Restaurant Booking Agent

This directory contains the LangGraph agent implementation for the restaurant booking system.

## Overview

The Restaurant Booking Agent is a conversational AI assistant that helps customers interact with a restaurant booking system. It provides a natural language interface for checking availability, making reservations, viewing booking details, and modifying or canceling bookings.

### Key Features

- **Natural Language Processing**: Understands conversational requests about restaurant bookings
- **Multi-turn Conversations**: Maintains context across conversation turns
- **Error Handling**: Graceful handling of API errors and invalid requests
- **Parameter Validation**: Ensures all booking parameters are valid before API calls
- **RESTful API**: Clean HTTP interface for integration with web applications

### Supported Operations

1. **Check Availability**: Find available time slots for specific dates and party sizes
2. **Create Bookings**: Make new reservations with customer information
3. **View Bookings**: Retrieve booking details using booking references
4. **Update Bookings**: Modify existing reservations (date, time, party size, special requests)
5. **Cancel Bookings**: Cancel reservations with appropriate reasons

## Structure

```
agent/
├── clients/
│   ├── __init__.py
│   └── restaurant_api.py      # API client wrapper
├── langgraph/
│   ├── __init__.py
│   ├── tools.py              # LangGraph Tool definitions
│   └── utils.py              # HTTP client and error handling utilities
├── agent.py                  # Main agent with HTTP server mode
├── requirements.txt          # Python dependencies
├── test_tools.py            # Test script for tools
├── test_agent.py            # Test script for agent functionality
├── example_usage.py         # Example usage script
└── README.md                # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Google API key:
```bash
export GOOGLE_API_KEY="your-google-api-key-here"
```

   To get a Google API key:
   1. Go to [Google AI Studio](https://aistudio.google.com/)
   2. Create a new API key
   3. Copy the key and set it as an environment variable

3. Ensure the restaurant booking API server is running:
```bash
cd ../app-server
python -m app
```

## Tools

The agent provides the following LangGraph tools:

### 1. check_availability
- **Function**: `check_availability_tool(params: dict) -> dict`
- **Description**: Returns available slots given restaurant, date, party size, and channel.
- **Required Parameters**:
  - `restaurant_name`: Name of the restaurant
  - `visit_date`: Date in YYYY-MM-DD format
  - `party_size`: Number of people
- **Optional Parameters**:
  - `channel_code`: Booking channel (defaults to "ONLINE")

### 2. book_reservation
- **Function**: `book_reservation_tool(params: dict) -> dict`
- **Description**: Creates a new restaurant booking with customer information and preferences.
- **Required Parameters**:
  - `restaurant_name`: Name of the restaurant
  - `visit_date`: Date in YYYY-MM-DD format
  - `visit_time`: Time in HH:MM:SS format
  - `party_size`: Number of people
- **Optional Parameters**:
  - `channel_code`: Booking channel (defaults to "ONLINE")
  - `special_requests`: Special requests for the booking
  - `is_leave_time_confirmed`: Boolean for time confirmation
  - `room_number`: Room/table number
  - `customer_data`: Dictionary of customer information

### 3. get_reservation
- **Function**: `get_reservation_tool(params: dict) -> dict`
- **Description**: Retrieves complete booking information by booking reference.
- **Required Parameters**:
  - `restaurant_name`: Name of the restaurant
  - `booking_reference`: Unique booking reference

### 4. update_reservation
- **Function**: `update_reservation_tool(params: dict) -> dict`
- **Description**: Modifies an existing booking with new date, time, party size, or special requests.
- **Required Parameters**:
  - `restaurant_name`: Name of the restaurant
  - `booking_reference`: Unique booking reference
- **Optional Parameters**:
  - `visit_date`: New date in YYYY-MM-DD format
  - `visit_time`: New time in HH:MM:SS format
  - `party_size`: New party size
  - `special_requests`: Updated special requests
  - `is_leave_time_confirmed`: Updated time confirmation

### 5. cancel_reservation
- **Function**: `cancel_reservation_tool(params: dict) -> dict`
- **Description**: Cancels an existing booking with a specified reason.
- **Required Parameters**:
  - `restaurant_name`: Name of the restaurant
  - `booking_reference`: Unique booking reference
  - `cancellation_reason_id`: ID of cancellation reason (1-5)

## Running the Agent

The agent runs as a FastAPI server:

```bash
python agent.py --port 8000
```

This starts a FastAPI server with:
- `/chat` POST endpoint for chat interactions
- `/health` GET endpoint for health checks
- `/docs` for API documentation

### Example Usage

```bash
# Start with default port (8000)
python agent.py

# Start server on custom port
python agent.py --port 9000

# Use custom Google API key
python agent.py --google-api-key "your-key"
```

## Testing

Run the test scripts to verify everything works correctly:

```bash
# Test the tools
python test_tools.py

# Test the agent functionality
python test_agent.py
```

These will test all tools and agent functionality with sample data.

## Agent Features

The agent provides a conversational interface that can:

- **Check Availability**: Find available time slots for restaurants
- **Create Bookings**: Make new reservations with customer information
- **View Bookings**: Retrieve booking details using references
- **Update Bookings**: Modify existing reservations
- **Cancel Bookings**: Cancel reservations with reasons

### Example Conversations

```
User: "I'd like to check availability for TheHungryUnicorn on January 15th for 4 people"
Agent: "I'll check the availability for you. Let me search for available slots..."

User: "Can you book a table for 6 people at 7:30 PM on January 15th?"
Agent: "I'd be happy to help you book a table. I'll need some additional information..."

User: "What's the status of my booking ABC1234?"
Agent: "Let me retrieve the details for your booking ABC1234..."
```

## Usage Example

```python
from agent import RestaurantBookingAgent

# Initialize the agent
agent = RestaurantBookingAgent()

# Chat with the agent
response = agent.chat_sync("Check availability for TheHungryUnicorn on 2025-01-15 for 4 people")
print(response)
```

## Error Handling

All tools include comprehensive error handling:

- **Parameter Validation**: Checks for required parameters and validates data types
- **Date/Time Parsing**: Validates date and time formats
- **API Errors**: Catches and returns HTTP errors from the API server
- **General Exceptions**: Catches any unexpected errors and returns them in a consistent format

Error responses follow the format:
```json
{
  "error": "Error description"
}
```

## Utilities

### HTTP Client and Error Handling

The `utils.py` module provides:

- **HTTPClient**: Shared HTTP client with authentication and session management
- **handle_api_error**: Decorator for consistent error handling across all tools
- **Validation Functions**: Helper functions for date, time, and parameter validation
- **Response Formatting**: Consistent error and success response formatting

### Error Handling

All tools include comprehensive error handling:

- **Parameter Validation**: Checks for required parameters and validates data types
- **Date/Time Parsing**: Validates date and time formats
- **API Errors**: Catches and returns HTTP errors from the API server
- **General Exceptions**: Catches any unexpected errors and returns them in a consistent format

Error responses follow the format:
```json
{
  "error": "Error description"
}
```

## API Client

The `RestaurantAPI` client in `clients/restaurant_api.py` handles:

- **Authentication**: Uses the mock bearer token
- **Request Formatting**: Converts parameters to the correct format for the API
- **Response Parsing**: Handles JSON responses from the API server
- **Error Handling**: Raises appropriate exceptions for HTTP errors

The client is configured to connect to `http://localhost:8547` by default, which is where the mock API server runs.

## Design Rationale

### Framework Selection

**LangGraph/LangChain**: Chosen for its robust agent framework capabilities:
- **Tool Integration**: Seamless integration with external APIs through tool definitions
- **Conversation Management**: Built-in support for multi-turn conversations with chat history
- **Error Handling**: Comprehensive error handling and recovery mechanisms
- **Production Ready**: Mature framework with extensive documentation and community support

**Google Gemini 2.0 Flash**: Selected for the LLM component:
- **Cost Effective**: Free tier available for development and testing
- **Performance**: Fast response times suitable for real-time chat applications
- **Reliability**: Google's infrastructure ensures high availability
- **Function Calling**: Excellent support for structured tool calling

### Design Decisions and Trade-offs

**HTTP Server vs CLI Interface**:
- **Decision**: HTTP server with `/chat` endpoint
- **Rationale**: Enables easy integration with web frontends and mobile applications
- **Trade-off**: Slightly more complex than CLI but much more flexible

**Async Architecture**:
- **Decision**: Async/await pattern throughout
- **Rationale**: Better performance for handling multiple concurrent requests
- **Trade-off**: More complex than synchronous code but essential for production

**Error Handling Strategy**:
- **Decision**: Consistent error format with detailed messages
- **Rationale**: Helps users understand and resolve issues quickly
- **Trade-off**: More verbose responses but better user experience

### Production Scalability

**Horizontal Scaling**:
- Stateless design allows multiple instances behind a load balancer
- Database connections can be pooled and shared
- Redis or similar for session management in multi-instance deployments

**Performance Optimization**:
- Connection pooling for HTTP requests to the restaurant API
- Caching of frequently accessed data (availability, restaurant info)
- Rate limiting to prevent abuse

**Monitoring and Observability**:
- Health check endpoints for service monitoring
- Structured logging for debugging and analytics
- Metrics collection for performance monitoring

### Security Considerations

**API Key Management**:
- Environment variable configuration for sensitive data
- Secure key rotation mechanisms
- API key validation and monitoring

**Input Validation**:
- Comprehensive parameter validation before API calls
- SQL injection prevention through parameterized queries
- XSS protection through proper output encoding

**Rate Limiting**:
- Request rate limiting to prevent abuse
- IP-based blocking for malicious requests
- DDoS protection through cloud services

### Limitations and Improvements

**Current Limitations**:
- Single restaurant support (TheHungryUnicorn only)
- No user authentication or session management
- Limited conversation context (no long-term memory)
- No integration with payment systems

**Potential Improvements**:
- Multi-restaurant support with restaurant discovery
- User authentication and booking history
- Integration with calendar systems
- Payment processing integration
- Multi-language support
- Voice interface capabilities
- Advanced analytics and reporting 