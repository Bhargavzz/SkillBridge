# SkillBridge AI — Backend

FastAPI application with LangGraph orchestration, pgvector vector store, and structured LLM outputs via Groq.

## Tech Stack

- Python 3.11
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
│   ├── dependencies.py       # get_db_session, get_current_user (Depends)
│   └── routers/
│       ├── auth.py           # POST /api/v1/auth/signup, /login
│       ├── analysis.py       # POST /api/v1/analysis/
│       └── health.py         # GET  /api/v1/health
├── core/
│   ├── config.py             # Pydantic Settings (.env)
│   ├── security.py           # JWT creation & password hashing
│   └── exceptions.py         # Custom exception hierarchy
├── models/
│   ├── orm.py                # SQLAlchemy ORM models
│   └── schemas.py            # Pydantic request/response schemas
├── repositories/
│   ├── user_repo.py          # User CRUD
│   └── vector_repo.py        # All pgvector queries
├── services/
│   └── orchestration.py      # OrchestrationService — business logic
├── alembic/                  # DB migrations (run automatically in Docker)
├── main.py                   # FastAPI app entrypoint
└── pyproject.toml
```

> **Note:** `.env` and `.env.example` now live at the **project root** (`SkillBridge/`), not inside `backend/`.

## Environment Variables

Copy the example from the **project root** and fill in your values:

```bash
# From project root (SkillBridge/)
cp .env.example .env
```

`.env` reference:

```env
# Groq Cloud LLM
GROQ_API_KEY="gsk_..."

# PostgreSQL credentials — used by both local dev URLs and docker-compose db service
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=skillbridge

# Local dev URLs (Docker overrides these to point to the 'db' container)
DATABASE_URL="postgresql://postgres:your_password@localhost:5433/skillbridge"
CHECKPOINT_DATABASE_URL="postgresql://postgres:your_password@localhost:5433/skillbridge"

# JWT Auth
SECRET_KEY="generate-a-long-random-hex-string"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **`CHECKPOINT_DATABASE_URL`** is used by the LangGraph checkpointer. It can point to the same database as `DATABASE_URL`.

---

## Running via Docker (recommended)

From the **project root** (`SkillBridge/`):

```bash
docker compose up --build
```

This will:
1. Start a **PostgreSQL 16 + pgvector** container on `localhost:5433`
2. Build and start the **FastAPI backend** — migrations run automatically on startup
3. Build and start the **Next.js frontend**

| URL | Description |
|---|---|
| http://localhost:8000 | API root |
| http://localhost:8000/docs | Swagger UI |
| `localhost:5433` | PostgreSQL (DBeaver / psql) |

---

## Running Locally (without Docker)

### Prerequisites

- Python 3.11
- [Poetry](https://python-poetry.org/docs/#installation)
- PostgreSQL 16 with the [pgvector extension](https://github.com/pgvector/pgvector) installed
- A [Groq API key](https://console.groq.com/)

### 1. Install dependencies

```bash
cd backend
poetry install
```

### 2. Run migrations

```bash
poetry run alembic upgrade head
```

### 3. Start the dev server

```bash
poetry run uvicorn main:app --reload --port 8000
```

| Endpoint | Description |
|---|---|
| `GET  /api/v1/health` | Health check |
| `POST /api/v1/auth/signup` | Register a new user |
| `POST /api/v1/auth/login` | Obtain a JWT token |
| `POST /api/v1/analysis/` | Run full LangGraph pipeline |

Swagger UI: http://localhost:8000/docs

---

## Key Design Decisions

- **Repository Pattern** — `vector_repo.py` is the only place that touches pgvector. LangGraph nodes never query the DB directly.
- **Dependency Injection** — DB sessions and LLM clients are always injected via `Depends()`. Never instantiated globally inside route handlers.
- **Structured Outputs** — All LLM responses are enforced via Pydantic schemas using `.with_structured_output()`. No raw string parsing.
- **Strategy Pattern (Fallback)** — `market_node` falls back to a deterministic keyword query if the LLM embedding call fails, preventing graph crashes.
- **Node Isolation** — Each LangGraph node only writes its own state key (`profile_summary`, `gap_analysis`, `roadmap`, `critic_feedback`).
- **Custom Exceptions** — `LLMServiceError`, `VectorStoreError`, `GraphExecutionError`, `DatabaseConnectionError` all extend `SkillBridgeAPIException`.
