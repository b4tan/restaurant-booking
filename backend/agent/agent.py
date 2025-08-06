"""
LangGraph Restaurant Booking Agent.

This module provides a conversational interface for checking availability, creating,
retrieving, updating, and canceling restaurant bookings by dynamically dispatching
to the corresponding API tools.

The agent runs as a FastAPI server exposing a /chat endpoint for HTTP interactions.

Author: AI Assistant
"""

import os
import sys
import asyncio
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage

# Import our tools and utilities
from langgraph.tools import (
    check_availability, book_reservation, get_reservation, 
    update_reservation, cancel_reservation
)
from langgraph.utils import handle_api_error


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    success: bool
    error: Optional[str] = None


class RestaurantBookingAgent:
    """
    LangGraph-powered chatbot agent for restaurant booking operations.
    
    This agent provides a conversational interface that can:
    - Check restaurant availability
    - Create new bookings
    - Retrieve booking details
    - Update existing bookings
    - Cancel bookings
    """
    
    def __init__(self):
        """
        Initialize the restaurant booking agent.
        
        Args:
            google_api_key: Google API key (will try to get from env if not provided)
        """
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass it to the constructor.")
        
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=self.google_api_key
        )
        
        # Define the tools
        self.tools = [
            check_availability,
            book_reservation,
            get_reservation,
            update_reservation,
            cancel_reservation
        ]
        
        # Create the agent
        self.agent_executor = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """
        Create the LangChain agent with our tools.
        
        Returns:
            AgentExecutor instance
        """
        # System prompt for the agent
        system_prompt = """You are a helpful restaurant booking assistant powered by Google Gemini. You can help users:

1. Check restaurant availability for specific dates and party sizes
2. Create new restaurant bookings with customer information
3. Retrieve booking details using booking references
4. Update existing bookings (date, time, party size, special requests)
5. Cancel bookings with appropriate reasons

When users ask about restaurant bookings, use the appropriate tools to help them. Be conversational and helpful, but always use the tools to perform actual operations.

For booking creation, make sure to collect all necessary information:
- Restaurant name
- Date (YYYY-MM-DD format)
- Time (HH:MM:SS format)
- Party size
- Customer information (name, email, phone)

For cancellations, you'll need:
- Restaurant name
- Booking reference
- Cancellation reason (1-5, where 1=Customer Request, 2=Restaurant Closure, 3=Weather, 4=Emergency, 5=No Show)

IMPORTANT GUIDELINES:
- Always be polite and professional
- If you encounter errors, explain them clearly and suggest alternatives
- For availability checks, suggest alternative dates if the requested date is unavailable
- When booking, confirm all details before proceeding
- For modifications, verify the booking exists first
- Provide helpful suggestions when users are unclear about requirements

RESTAURANT INFORMATION:
- Restaurant name: TheHungryUnicorn
- Available times: Lunch (12:00-13:30) and Dinner (19:00-20:30)
- Maximum party size: 8 people per table
- Booking window: 30 days in advance"""

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    async def chat(self, message: str, chat_history: Optional[list] = None) -> str:
        """
        Process a chat message and return the agent's response.
        
        Args:
            message: User's message
            chat_history: Optional chat history for context
            
        Returns:
            Agent's response as a string
        """
        try:
            # Prepare the input for the agent
            input_data = {
                "input": message,
                "chat_history": chat_history or []
            }
            
            # Run the agent
            result = await self.agent_executor.ainvoke(input_data)
            
            return result.get("output", "I'm sorry, I couldn't process your request.")
            
        except Exception as e:
            return f"I encountered an error while processing your request: {str(e)}"
    



def create_fastapi_app(agent: RestaurantBookingAgent) -> FastAPI:
    """
    Create a FastAPI app with the chat endpoint.
    
    Args:
        agent: RestaurantBookingAgent instance
        
    Returns:
        FastAPI app instance
    """
    app = FastAPI(
        title="Restaurant Booking Agent API",
        description="LangGraph-powered chatbot for restaurant booking operations",
        version="1.0.0"
    )
    
    @app.post("/chat", response_model=ChatResponse)
    async def chat_endpoint(request: ChatRequest):
        """
        Chat endpoint for restaurant booking agent.
        
        Args:
            request: ChatRequest containing the user's message
            
        Returns:
            ChatResponse with the agent's response
        """
        try:
            response = await agent.chat(request.message)
            return ChatResponse(
                response=response,
                success=True
            )
        except Exception as e:
            return ChatResponse(
                response="",
                success=False,
                error=str(e)
            )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        try:
            # Check if the restaurant API server is running
            import requests
            response = requests.get("http://localhost:8547/", timeout=5)
            api_status = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            api_status = "unreachable"
        
        return {
            "status": "healthy", 
            "service": "restaurant-booking-agent",
            "restaurant_api": api_status
        }
    
    return app





def main():
    """
    Main entry point for the agent.
    
    Starts the HTTP server mode by default.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Restaurant Booking Agent")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for HTTP server (default: 8000)"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--google-api-key",
        help="Google API key (or set GOOGLE_API_KEY environment variable)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize the agent
        agent = RestaurantBookingAgent(google_api_key=args.google_api_key)
        
        # Run in server mode
        import uvicorn
        app = create_fastapi_app(agent)
        
        print(f"🚀 Starting Restaurant Booking Agent server on {args.host}:{args.port}")
        print(f"📝 API documentation available at http://{args.host}:{args.port}/docs")
        print("Press Ctrl+C to stop the server")
        
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="info"
        )
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main() 