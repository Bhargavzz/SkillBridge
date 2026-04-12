# SkillBridge AI

AI-powered career skill gap analysis and personalized learning roadmap generator.

## Architecture

```
jd_agent/
├── backend/          # FastAPI + LangGraph + pgvector
└── frontend/         # Next.js 14 App Router + shadcn/ui + Tailwind
```

## Stack Overview

| Layer | Tech |
|---|---|
| API | FastAPI + Uvicorn |
| AI Orchestration | LangGraph (supervisor pattern) |
| LLM | Groq — llama3-70b-8192 via LangChain |
| Vector Store | PostgreSQL + pgvector |
| Frontend | Next.js 14 App Router (RSC) |
| UI | shadcn/ui + Tailwind CSS |
| Language | Python 3.11+ / TypeScript (strict) |

## LangGraph Pipeline

```
profile → market → gap → roadmap → critic → END
```

Each node lives in its own file under `backend/agents/`. The vector DB is only touched through `backend/repositories/`. All LLM responses use `.with_structured_output()` (Pydantic v2).

## Setup

- **Backend**: see [`backend/README.md`](./backend/README.md)
- **Frontend**: see [`frontend/README.md`](./frontend/README.md)
