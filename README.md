# About

This project demonstrates a conversational booking assistant built with LangGraph and React. The core components are:

- **LangGraph Agent**  
  A stateful, tool-augmented AI agent powered by Google’s Gemini model. It uses a collection of custom tools to orchestrate restaurant booking workflows:
  - `check_availability`  
  - `book_reservation`  
  - `get_reservation`  
  - `update_reservation`  
  - `cancel_reservation`

- **Mock API Server**  
  A FastAPI application simulating a restaurant booking backend, complete with SQLite persistence and endpoints for availability search and full CRUD on bookings. The agent’s tools call this server at `http://localhost:8547/api/ConsumerApi/v1`.

- **React Frontend**  
  A chat interface that sends user messages (along with a session ID) to the FastAPI agent at `http://localhost:8000/chat`, then renders tool-driven responses in a conversational UI.

Together, these pieces showcase how to build a tool‐enabled AI assistant that can:
1. Prompt for and validate user inputs  
2. Dynamically call backend services via well-defined tool APIs  
3. Maintain conversational context and slot-fill missing information  
4. Deliver a seamless “chatbot + API” experience end-to-end.  


# Project directory
restaurant-booking-project/
├── backend/
│   ├── app/
│   │  ├── __main__.py
│   │  ├── main.py                # FastAPI app entrypoint
│   │  ├── database.py
│   │  ├── models.py
│   │  ├── init_db.py
│   │  └── routers/
│   │      ├── availability.py
│   │      └── booking.py
│   └── agent/                    # LangGraph agent wrapping API endpoints as tools
│       ├── agent.py              # Boots LangGraph agent, can expose REST endpoint
│       ├── langgraph/
│       │   ├── tools.py          # Tool definitions for each endpoint
│       │   └── utils.py          # HTTP client helpers, auth handling
│       ├── clients/
│       │   └── restaurant_api.py # Thin wrapper around API server endpoints
└── test_tools.py              
└── test_restaurant_api.py              
└── requirements.txt              # Dependencies (langgraph, requests, fastapi)
├── frontend/                     # React SPA showing a chatbot UI centered on screen
│   ├── README.md
│   ├── package.json
│   ├── public/
│   │   └── index.html            # Root HTML with a div#root
│   └── src/
│       ├── index.jsx             # React entrypoint
│       ├── App.jsx               # Renders ChatWindow in center
│       ├── components/
│       │   ├── ChatWindow.jsx    # Scrollable message list + input box
│       │   └── MessageBubble.jsx # Individual chat bubbles
│       ├── api/
│       │   └── agentApi.js       # HTTP client to call /chat endpoint on agent
│       └── styles/
│           └── App.css           # Center layout and basic styling
└── README.md                     # Project overview and setup instructions


# Instructions to run app
### Run the backend - Mock server (app directory) and agent server (agent directory)
Instructions to run is in the README file of each directory

### Run the frontend server - React
Instructions to run is in the README file of the frontend directory


## Design Rationale
### Frameworks & Tools

* LangGraph: Easy tool integration and simple planning loop.

* FastAPI: Fast setup for the mock booking API with built-in validation and docs.

* HTTPX: Reliable HTTP client for API calls.

* React.js: Interactive chat UI, easy state management.

* Gemini LLM: Strong language understanding for planning and conversations.

## Key Decisions & Trade-offs

* Sessions stored in memory (simple but lost on restart).

* Explicit tool parameters (helps accuracy but more code).

* Mock server for offline dev (not production-ready in auth or scale).

## Scaling Up

* Move session store to Redis or a database.

* Replace SQLite with Postgres for concurrency.

* Containerize the API behind a load balancer.

* Cache or batch LLM calls to reduce costs.

## Limitations & Next Steps

* Error messages are basic—could be more user-friendly.

* Frontend needs better input checks (e.g., date pickers).

* Add a tool to list bookings by email/phone.

* Improve UI with typing indicators, timestamps, and accessibility.

## Security Notes

* Rate-limit the chat endpoint to prevent abuse.

* Validate all inputs to avoid injection attacks.

```
