# SkillBridge AI — Backend

FastAPI application with LangGraph orchestration, pgvector vector store, and structured LLM outputs via Groq.

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- LangGraph (`StateGraph`, supervisor pattern)
- LangChain + `langchain-groq` (llama3-70b-8192)
- SQLAlchemy 2.x + pgvector + Alembic
- Pydantic v2 + pydantic-settings
- Poetry for dependency management

## Project Structure

```
backend/
├── agents/
│   ├── state.py              # GraphState TypedDict
│   ├── graph.py              # build_graph() — wires all nodes
│   ├── profile_agent.py      # profile_node
│   ├── market_agent.py       # market_node (vector search + LLM fallback)
│   ├── gap_agent.py          # gap_node
│   ├── roadmap_agent.py      # roadmap_node
│   └── critic_agent.py       # critic_node
├── api/
│   ├── dependencies.py       # get_db_session, get_llm_client (Depends)
│   └── routers/
│       ├── analysis.py       # POST /api/v1/analysis/
│       └── health.py         # GET  /api/v1/health
├── core/
│   ├── config.py             # Pydantic Settings (.env)
│   └── exceptions.py         # Custom exception hierarchy
├── models/
│   └── schemas.py            # AnalysisRequest / AnalysisResponse
├── repositories/
│   └── vector_repo.py        # All pgvector queries (isolated from agents)
├── services/
│   └── orchestration.py      # OrchestrationService — business logic
├── alembic/                  # DB migrations
├── main.py                   # FastAPI app entrypoint
├── pyproject.toml
└── .env.example
```

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL 15+ with the [pgvector extension](https://github.com/pgvector/pgvector)
- A [Groq API key](https://console.groq.com/)

## Setup

### 1. Install dependencies

```bash
cd backend
poetry install
```

### 2. Environment variables

```bash
cp .env.example .env
```

Fill in `.env`:

```env
GROQ_API_KEY="gsk_..."
DATABASE_URL="postgresql://user:password@localhost:5432/skillbridge"
CHECKPOINT_DATABASE_URL="postgresql://user:password@localhost:5432/skillbridge"
```

> `CHECKPOINT_DATABASE_URL` is used by the LangGraph checkpointer. It can point to the same database as `DATABASE_URL`.

### 3. Create the database and enable pgvector

```bash
psql -U postgres -c "CREATE DATABASE skillbridge;"
psql -U postgres -d skillbridge -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 4. Run migrations

```bash
poetry run alembic upgrade head
```

### 5. Start the dev server

```bash
poetry run uvicorn main:app --reload --port 8000
```

| Endpoint | Description |
|---|---|
| `GET  /api/v1/health` | Health check |
| `POST /api/v1/analysis/` | Run full LangGraph pipeline |

Swagger UI: http://localhost:8000/docs

## Key Design Decisions

- **Repository Pattern** — `vector_repo.py` is the only place that touches pgvector. LangGraph nodes never query the DB directly.
- **Dependency Injection** — DB sessions and LLM clients are always injected via `Depends()`. Never instantiated globally inside route handlers.
- **Structured Outputs** — All LLM responses are enforced via Pydantic schemas using `.with_structured_output()`. No raw string parsing.
- **Strategy Pattern (Fallback)** — `market_node` falls back to a deterministic keyword query if the LLM embedding call fails, preventing graph crashes.
- **Node Isolation** — Each LangGraph node only writes its own state key (`profile_summary`, `gap_analysis`, `roadmap`, `critic_feedback`).
- **Custom Exceptions** — `LLMServiceError`, `VectorStoreError`, `GraphExecutionError`, `DatabaseConnectionError` all extend `SkillBridgeError`.
