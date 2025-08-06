"""
Test script for the Restaurant Booking Agent.

This script tests the agent functionality to ensure it works correctly
with the restaurant booking API.

Author: AI Assistant
"""

import os
import sys
import asyncio
from agent import RestaurantBookingAgent


def test_agent_initialization():
    """Test that the agent can be initialized properly."""
    print("Testing agent initialization...")
    
    # Set a dummy API key for testing
    os.environ["GOOGLE_API_KEY"] = "test-key"
    
    try:
        agent = RestaurantBookingAgent()
        print("✅ Agent initialized successfully")
        return agent
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return None


def test_agent_chat():
    """Test the agent's chat functionality."""
    print("\nTesting agent chat functionality...")
    
    agent = test_agent_initialization()
    if not agent:
        return
    
    # Test messages
    test_messages = [
        "Hello, can you help me with restaurant bookings?",
        "What can you do?",
        "I'd like to check availability for TheHungryUnicorn on 2025-01-15 for 4 people"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        try:
            response = asyncio.run(agent.chat(message))
            print(f"Agent: {response}")
        except Exception as e:
            print(f"❌ Chat failed: {e}")


def test_server_mode():
    """Test the FastAPI server creation."""
    print("\nTesting server mode...")
    
    agent = test_agent_initialization()
    if not agent:
        return
    
    try:
        from agent import create_fastapi_app
        app = create_fastapi_app(agent)
        print("✅ FastAPI app created successfully")
        
        # Test that the app has the expected endpoints
        routes = [route.path for route in app.routes]
        expected_routes = ["/chat", "/health", "/docs", "/openapi.json"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Found route: {route}")
            else:
                print(f"❌ Missing route: {route}")
                
    except Exception as e:
        print(f"❌ Server mode test failed: {e}")


def main():
    """Run all tests."""
    print("🧪 Testing Restaurant Booking Agent")
    print("=" * 50)
    
    # Check if Google API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not set. Using dummy key for testing.")
        print("   Set GOOGLE_API_KEY environment variable for full functionality.")
    
    # Run tests
    test_agent_initialization()
    test_agent_chat()
    test_server_mode()
    
    print("\n" + "=" * 50)
    print("Testing complete!")
    print("\nTo run the agent:")
    print("  python agent.py --port 8000")
    print("\nNote: Set GOOGLE_API_KEY environment variable for full functionality.")


if __name__ == "__main__":
    main() 