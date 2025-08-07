import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangGraph agent
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Your existing tools
from restaurant_langgraph.tools import (
    check_availability,
    book_reservation,
    get_reservation,
    update_reservation,
    cancel_reservation
)

# Load environment
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# System prompt
SYSTEM_PROMPT = """
You are a polite and professional chatbot agent for restaurant booking operations. 
The only restaurant available is “TheHungryUnicorn.” 

For each user request, guide them step-by-step and always confirm you have all necessary information:

• To Check Availability, ask for:
  – visit date, assume it's this year user doesn't provide
  – party size  

• To Make A Reservation, ask for:
  – visit date, assume it's this year user doesn't provide
  – visit time 
  – party size  
  – (Optional) any special requests  
  - (Optional) Whether they’d like to provide the following customer details (so we can store them and send the booking reference later): 
    Explicitly ask for name, email, phone number. Don't ask for additional information unless given.
    + Title (Mr/Mrs/Ms/Dr)
    + First name
    + Surname
    + Email address
    + Mobile number
    + Phone (landline)
    + Mobile country code
    + Phone country code
    + Marketing opt-ins (email and/or SMS)

• To Retrieve a Booking, ask for:
  – booking reference  
  – If they don’t know their reference, ask for the email or phone number they used, then look up matching reservations  

• To Update a Booking, ask for:
  – booking reference (or email/phone to look it up)  
  – which fields they want to change (date, time, party size, special requests)
  - provide the new times available in that particular date 
  – the new values for those fields  

• To Cancel a Booking, ask for:
  – booking reference (or email/phone to look it up)  
  – a cancellation reason (1–5; for example “1” = Customer Request)  

Make sure final response to user is formatted properly. Call tools as many times as needed, before structuring a response execute a chain of thought of what functions need to be called. Relevant information is also stored in the chat/sessions so be aware of those information.
"""


# Instantiate agent
agent = create_react_agent(
    model=llm,
    tools=[
        check_availability,
        book_reservation,
        get_reservation,
        update_reservation,
        cancel_reservation
    ],
    system_prompt=SYSTEM_PROMPT
)

# In-memory session history: messages list per session
sessions: dict[str, list[dict]] = {}

# FastAPI setup
app = FastAPI(title="LangGraph Booking Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.debug(f"Session {request.session_id} | User: {request.message!r}")
    try:
        # Initialize or retrieve history
        history = sessions.setdefault(
            request.session_id,
            [{"role": "system", "content": SYSTEM_PROMPT}]
        )
        # Append user turn
        history.append({"role": "user", "content": request.message})
        logger.debug(f"History sent to agent: {history}")

        # Invoke agent with history
        payload = {"messages": history}
        reply = agent.invoke(payload)
        logger.debug(f"Agent reply raw: {reply!r}")

        # Normalize reply messages
        msgs = reply.get("messages", reply.messages if hasattr(reply, "messages") else [reply])
        # Extract last assistant content
        assistant_content = None
        for msg in reversed(msgs):
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                assistant_content = msg.get("content")
                break
            if hasattr(msg, 'content') and getattr(msg, 'role', None) != 'user':
                assistant_content = msg.content
                break
        if assistant_content is None:
            assistant_content = str(msgs[-1])

        # Append assistant turn locally
        history.append({"role": "assistant", "content": assistant_content})
        logger.debug(f"Updated history: {history}")

        return ChatResponse(response=assistant_content)

    except Exception:
        logger.exception("Error during chat handling")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8000, reload=True)
