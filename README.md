# Multi-Agent Travel Planner

TripMate AI is an AI-powered travel planning application built with LangGraph. It combines flight information retrieval, hotel research, itinerary generation, and response synthesis into a single workflow, helping users organize their travel plans from a natural-language request.

The application provides a conversational interface built with Streamlit, a FastAPI backend, and PostgreSQL-based checkpointing for LangGraph.

## Features

- **Flight Information:** Retrieves flight-related information through the AviationStack API and resolves locations to airport codes.
- **Hotel Research:** Uses Tavily Search to retrieve relevant hotel information and recommendations.
- **AI-Generated Itineraries:** Generates practical, day-by-day travel itineraries using a Groq-hosted language model.
- **Consolidated Travel Plans:** Combines flight information, hotel research, and itinerary details into a structured response.
- **Conversational Interface:** Provides a Streamlit chat interface for submitting travel requests and viewing results.
- **REST API:** Exposes a FastAPI endpoint for processing travel planning requests.
- **Persistent Checkpointing:** Uses PostgreSQL with LangGraph's `PostgresSaver` to persist graph execution checkpoints by thread ID.

## Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Agent orchestration | LangGraph |
| LLM integration | LangChain and ChatGroq |
| Language model | `openai/gpt-oss-20b` |
| Flight information | AviationStack API |
| Web search | Tavily |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database and checkpointing | PostgreSQL, Psycopg, LangGraph Postgres Checkpointer |
| Environment configuration | python-dotenv |
| SSL certificates | Certifi |

## Architecture

The application uses a sequential LangGraph workflow in which each node performs a specific stage of travel planning.

```text
User
 |
 v
Streamlit Interface
 |
 v
FastAPI Backend
 |
 v
LangGraph Workflow
 |
 v
Flight Agent
 |  AviationStack API
 v
Hotel Agent
 |  Tavily Search
 v
Itinerary Agent
 |  Groq LLM
 v
Final Response Agent
 |  Groq LLM
 v
Structured Travel Plan
```

PostgreSQL checkpointing is configured to persist graph state associated with a conversation thread.

### Workflow Components

| Component | Responsibility |
|---|---|
| Flight Agent | Retrieves flight-related information using the flight search tool. |
| Hotel Agent | Searches for relevant hotel information using Tavily. |
| Itinerary Agent | Generates a day-by-day itinerary using the user's request and the collected flight and hotel information. |
| Final Response Agent | Synthesizes the available information into a structured travel planning response. |

The current implementation follows a predefined execution sequence. Each stage passes its results through the shared LangGraph state to subsequent stages.

## Project Structure

```text
multi-agent-travel-planner-/
|
├── tools/
│   ├── flight_tool.py       # Flight information retrieval
│   └── tavily_tool.py       # Web search for hotel information
|
├── app.py                   # FastAPI application and API endpoints
├── backend.py               # LangGraph workflow and agent logic
├── ui.py                    # Streamlit chat interface
├── test.py                  # Command-line testing entry point
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

Before running the application, ensure you have:

- Python 3.10 or later
- Access to a PostgreSQL database
- A Groq API key
- A Tavily API key
- An AviationStack API key

### 1. Clone the Repository

```bash
git clone https://github.com/Nashra-Syeda/multi-agent-travel-planner-.git
cd multi-agent-travel-planner-
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory and configure the required credentials:

```dotenv
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=your_postgresql_connection_string

# Optional: default origin airport IATA code
DEFAULT_ORIGIN_IATA=DAC
```

Replace the placeholder values with your own credentials and PostgreSQL connection string.

`DEFAULT_ORIGIN_IATA` is optional. The current flight tool uses `DAC` as its default when this variable is not set.

**Security:** Never commit your `.env` file or expose API keys and database credentials in source code, logs, screenshots, or public repositories.

## Running the Application

The application consists of a FastAPI backend and a Streamlit frontend. Run them in separate terminal sessions from the project root.

### 1. Start the FastAPI Backend

```bash
python app.py
```

The API starts at:

`http://127.0.0.1:8000`

API documentation is available at:

`http://127.0.0.1:8000/docs`

### 2. Start the Streamlit Frontend

Open another terminal, activate the same virtual environment, and run:

```bash
streamlit run ui.py
```

Open the local URL printed by Streamlit, usually:

`http://localhost:8501`

### 3. Submit a Travel Request

Enter a natural-language travel request in the chat interface. For example:

- Plan a three-day trip to Goa from Delhi within a budget of INR 20,000.
- Suggest hotels and prepare a five-day itinerary for Tokyo.
- Help me plan a trip with flight information, accommodation suggestions, and a day-by-day schedule.

The application processes the request through the LangGraph workflow and displays the consolidated response. The interface also provides separate tabs for flight results, hotel results, and the generated itinerary.

## API Reference

### `POST /api/travel`

Processes a travel planning request.

Example request:

```json
{
  "message": "Plan a three-day trip to Goa from Delhi within INR 20000"
}
```

An optional `thread_id` can be supplied to associate the request with an existing LangGraph checkpoint thread.

Example request with a thread ID:

```json
{
  "message": "Suggest more hotels for this trip",
  "thread_id": "your-existing-thread-id"
}
```

The response includes the generated answer, thread ID, flight results, hotel results, itinerary, and an execution counter.

### `GET /health`

Checks whether the FastAPI application is running.

Example response:

```json
{
  "status": "ok",
  "message": "AI Travel Planner API is running"
}
```

## Implementation Notes and Limitations

- The graph currently executes its nodes in a fixed sequence; it does not dynamically select which agents to invoke.
- Flight information depends on the AviationStack API response and its available data. Ticket prices may not be available.
- Hotel information is retrieved through web search and should be independently verified before booking.
- The itinerary and budget estimates are AI-generated suggestions and may not reflect current prices or actual availability.
- The application assists with travel research and planning. It does not complete flight or hotel bookings or process payments.
- PostgreSQL checkpointing persists graph execution state by thread ID; it does not by itself guarantee that earlier conversation messages are included in every new LLM prompt.
- API access, database connectivity, and external service limits depend on the corresponding provider configurations and credentials.

Always verify travel schedules, accommodation details, prices, and booking conditions with the relevant providers before making travel arrangements.

## Future Improvements

Potential enhancements include:

- Conditional routing to invoke only the agents required by a request.
- Parallel flight and hotel searches to reduce response time.
- Improved error handling, retries, and external API timeouts.
- More accurate budget estimation with explicit currency handling.
- Stronger validation of travel dates, destinations, and user constraints.
- Automated tests for the graph workflow and API endpoints.
- Deployment configuration for a hosted application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
