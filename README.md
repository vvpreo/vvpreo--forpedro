# Contract Risk Analyzer API

A minimal working prototype of an API that analyzes legal risks in contracts using an LLM.

## Original Task
```
You have access to a structured LLM API that reliably returns JSON and can reason step-by-step.

Build a minimal working prototype of: "A contract risk analyzer API"

The system should:

Accept raw contract text

Extract key clauses into structured JSON

Identify potential risks (e.g. termination, liability, payment terms)

Return a structured response

Requirements:

Use an LLM

Expose either a simple API endpoint OR minimal UI

Handle at least one edge case

Make reasonable architectural decisions
```

## Why This Is a Good Solution

### Structured output, guaranteed
The core challenge of any LLM-based API is output reliability. This project solves it by combining the **[Instructor](https://github.com/jxnl/instructor)** library with **Pydantic** models. Instead of hoping the LLM returns valid JSON, the system *enforces* a strict schema (`AnalyzeResponse`) including nested `Party` objects, each with field-level validators. If the LLM drifts, Instructor retries until the response conforms — or raises a clean error. The result is a typed, validated object before the first line of the handler runs.

### Edge-case handling at every layer
- **Non-contract text** — The schema includes an `is_contract` boolean, so the system gracefully classifies random text instead of crashing.
- **Empty / oversized input** — Both the frontend (character counter, 50 000-char cap) and the backend (`AnalyzeRequest` validator + explicit checks in the endpoint) reject bad input with clear error messages.
- **LLM failure** — The endpoint catches exceptions and returns a structured `500` instead of leaking a traceback.

### Clean separation of concerns
| Layer | File | Responsibility |
|---|---|---|
| API | `src/main.py` | FastAPI app, routing, input validation, error mapping |
| Agent | `src/legal_agent.py` | LLM call via OpenRouter, schema enforcement |
| Schemas | `src/schemas.py` | Pydantic models + custom validators |
| UI | `static/index.html` | Self-contained SPA; no build step |

The architecture is deliberately flat — four files, zero abstraction layers that don't earn their keep.

### Fully containerized
A production-ready `Dockerfile` (Python 3.11-slim, non-root, no `.pyc`) and `docker-compose.yml` make deployment a one-liner:
```bash
docker compose up --build
```
Scripts in `scripts/` handle cross-platform x86 builds and GHCR pushes with commit-hash tagging.

### Async from top to bottom
FastAPI + `AsyncOpenAI` + `async/await` throughout. The server can handle concurrent requests without blocking on LLM latency.

### Test strategy that actually tests the LLM
Instead of mocking the model, the test suite calls the real LLM against a bank of 12 generated fixtures (6 contracts, 6 non-contracts). A separate generator (`tst/run_test_data_generator.py`) creates new test data on demand, so the suite can be expanded in seconds. Each test asserts classification correctness and serializes the full YAML output for manual review.

### Minimal but functional UI
The single-page frontend fits in one HTML file — no framework, no build toolchain. It renders the analysis as structured cards (classification, summary, clauses, parties, risks) and dumps the full response as syntax-highlighted YAML for transparency.

## Quick Start

```bash
# 1 · Clone & configure
cp .env.example .env          # add your OPENROUTER_APIKEY

# 2 · Run with Docker
docker compose up --build

# 3 · Open the UI
open http://localhost:8000
```

## API

### `POST /api/analyze`
Accepts `{ "text": "<contract text>" }`, returns:
```json
{
  "is_contract": true,
  "about": "Summary of the contract...",
  "key_clauses": ["Termination clause", "..."],
  "parties": [
    {
      "role": "Buyer",
      "potential_risks": ["Unlimited liability", "..."]
    }
  ]
}
```

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| LLM | GPT-4o-mini via OpenRouter |
| Schema enforcement | Instructor + Pydantic v2 |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | Docker, Docker Compose, GHCR |
| Tests | pytest + pytest-asyncio |
