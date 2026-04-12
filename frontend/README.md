# SkillBridge AI — Frontend

Next.js 14 App Router application. Sends analysis requests to the FastAPI backend and renders the live LangGraph execution trace via Server-Sent Events (SSE).

## Tech Stack

- Next.js 14 (App Router)
- TypeScript (strict, no implicit `any`)
- shadcn/ui + Radix UI primitives
- Tailwind CSS
- Lucide React icons

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx            # Root layout (RSC)
│   ├── page.tsx              # Home page (RSC)
│   └── globals.css
├── components/
│   ├── ui/
│   │   └── Button.tsx        # shadcn/ui base components
│   └── features/
│       └── RoadmapDisplay.tsx # Atomic feature component
├── hooks/
│   └── useLangGraphStream.ts # SSE streaming hook for LangGraph events
├── lib/
│   ├── api.ts                # Typed API client (fetch wrappers)
│   └── utils.ts              # cn() and shared utilities
├── types/
│   └── api.ts                # AnalysisRequest / AnalysisResponse / AgentStreamEvent
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

## Prerequisites

- Node.js 18+
- npm 9+ (or pnpm / yarn)
- Backend running at `http://localhost:8000` (see `backend/README.md`)

## Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Environment variables

Create `.env.local` in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Adjust the port if the backend runs elsewhere.

### 3. Start the dev server

```bash
npm run dev
```

App available at http://localhost:3000

### Other scripts

| Command | Description |
|---|---|
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | ESLint |
| `npm run type-check` | TypeScript check (no emit) |

## Key Design Decisions

- **RSC by default** — All components are React Server Components unless interactivity, hooks, or browser APIs are required.
- **`'use client'` boundary** — Applied only at the lowest possible level in the component tree (e.g., `useLangGraphStream` consumers).
- **`useLangGraphStream` hook** — Encapsulates all SSE connection lifecycle, event parsing, and incremental state updates. Components receive clean `{ isStreaming, result, error, startStream, stopStream }`.
- **Typed API layer** — `lib/api.ts` wraps all `fetch` calls. Components never call `fetch` directly.
- **shadcn/ui only** — No custom CSS except where Tailwind utilities are insufficient.
- **Atomic components** — Complex views (roadmap, Gantt) broken into small presentational components under `components/features/`.
