```
restaurant-booking-project/
├── backend/
│   ├── api-server/               # Existing mock FastAPI restaurant booking server
│   │   ├── app/
│   │   │   ├── __main__.py
│   │   │   ├── main.py           # FastAPI app entrypoint
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   ├── init_db.py
│   │   │   └── routers/
│   │   │       ├── availability.py
│   │   │       └── booking.py
│   │   ├── requirements.txt      # Dependencies for API server
│   └── agent/                    # LangGraph agent wrapping API endpoints as tools
│       ├── agent.py              # Boots LangGraph agent, can expose REST endpoint
│       ├── langgraph/
│       │   ├── tools.py          # Tool definitions for each endpoint
│       │   └── utils.py          # HTTP client helpers, auth handling
│       ├── clients/
│       │   └── restaurant_api.py # Thin wrapper around API server endpoints
│       └── requirements.txt      # Dependencies (langgraph, requests, fastapi)
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
├── tests/                        # End-to-end and unit tests
│   ├── backend_tests/
│   │   └── test_agent.py
│   └── frontend_tests/
│       └── ChatWindow.test.jsx
├── docker-compose.yml            # Orchestrate API server, agent, and frontend
└── README.md                     # Project overview and setup instructions
```
