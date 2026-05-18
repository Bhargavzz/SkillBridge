# SkillBridge AI

AI-powered career skill gap analysis and personalised learning roadmap generator.

## Architecture

```
./
├── backend/          # FastAPI + LangGraph + pgvector
├── frontend/         # Next.js App Router + shadcn/ui + Tailwind
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

## Stack Overview

| Layer | Tech |
|---|---|
| API | FastAPI + Uvicorn |
| AI Orchestration | LangGraph (supervisor pattern) |
| LLM | Groq — llama3-70b-8192 via LangChain |
| Vector Store | PostgreSQL 16 + pgvector |
| Frontend | Next.js App Router (RSC) |
| UI | shadcn/ui + Tailwind CSS |
| Language | Python 3.11 / TypeScript (strict) |
| Container | Docker + docker-compose |

## LangGraph Pipeline

```
profile → market → gap → roadmap → critic → END
```

Each node lives in its own file under `backend/agents/`. The vector DB is only touched through `backend/repositories/`. All LLM responses use `.with_structured_output()` (Pydantic v2).

## Quick Start (Docker — recommended)

> **Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
# 1. Clone
git clone <repo-url>
cd SkillBridge

# 2. Copy the example env and fill in your credentials
cp .env.example .env

# 3. Spin up all services (db + backend + frontend)
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| PostgreSQL | `localhost:5433` (DBeaver / psql) |

> **Tip:** All three services start in the correct order automatically — `db` → `backend` (runs migrations) → `frontend`.

## Running Services Individually (Local Dev)

- **Backend**: see [`backend/README.md`](./backend/README.md)
- **Frontend**: see [`frontend/README.md`](./frontend/README.md)
