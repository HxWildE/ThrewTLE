# ThrewTLE ⚡
> **Deterministic, edge-case test case generator and validation suite for LeetCode problems to expose algorithmic edge failures before submission.**

---

## 🎯 Overview
**ThrewTLE** helps software engineers, competitive programmers, and technical interview candidates rigorously stress-test their LeetCode solutions *before* submitting to official judges. Standard LeetCode example test cases frequently miss subtle boundary conditions, alternating sign transitions, empty structures, integer overflow thresholds ($2^{31}-1$, $-2^{31}$), and quadratic worst-case inputs ($O(N^2)$ vs. $O(N)$ or $O(N \log N)$).

ThrewTLE bridges this gap by generating problem-specific, deduplicated, and constraint-verified edge test cases formatted in exact **LeetCode Raw Input** format ready for direct pasting into the custom testcase box.

---

## 🏗️ Architecture & Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.14+) with asynchronous endpoints, dependency injection, and Pydantic v2 schemas.
- **Database & Persistence**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) declarative models with [Alembic](https://alembic.sqlalchemy.org/) migrations. Supports PostgreSQL in production and `sqlite+aiosqlite` for lightweight local development and automated testing.
- **Test Generation Engine**: Multi-tiered heuristic and property-based synthesis using [Hypothesis](https://hypothesis.readthedocs.io/) and deterministic boundary generators across array, string, numeric, and matrix domains.
- **Deduplication & Validation**: SHA-256 canonical structural fingerprinting with strict constraint and schema validation.
- **Frontend**: Reactive, high-performance [React](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) web application built with [Vite](https://vitejs.dev/) and custom modern UI design.
- **Visuals & Education**: 13 comprehensive Mermaid architecture diagrams in `diagrams/` and 16 deep educational guides in `learning/`.

---

## 📂 Repository Structure

```text
ThrewTLE/
├── .github/
│   └── workflows/
│       ├── test.yml                   # CI automated test workflow
│       └── scheduled_commits.yml      # Automated commit workflow
├── backend/
│   ├── app/
│   │   ├── api/                       # Versioned REST routers & dependencies
│   │   ├── core/                      # Configuration, error handlers, logging
│   │   ├── db/                        # Database sessions, base models & fixtures
│   │   ├── engine/                    # Generation strategies, formatters, validation
│   │   ├── integrations/              # Hugging Face, LeetCode client, optional LLM
│   │   ├── jobs/                      # Catalogue synchronization background job
│   │   ├── models/                    # SQLAlchemy 2.0 declarative models
│   │   ├── repositories/              # Database data access layer
│   │   ├── schemas/                   # Pydantic v2 request/response schemas
│   │   ├── services/                  # Business logic orchestrators
│   │   └── main.py                    # FastAPI application factory
│   ├── alembic/                       # Database migrations
│   ├── scripts/                       # Sample ingestion & seed utilities
│   ├── tests/                         # Pytest test suites (unit, engine, API)
│   ├── alembic.ini                    # Alembic configuration
│   ├── pyproject.toml                 # Backend build metadata
│   └── requirements.txt               # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── api/                       # Type-safe backend HTTP client
│   │   ├── components/                # React modular UI components
│   │   ├── hooks/                     # Custom data-fetching hooks
│   │   ├── types/                     # Shared TypeScript interfaces
│   │   ├── App.tsx                    # Root UI application
│   │   ├── index.css                  # Custom modern design system
│   │   └── main.tsx                   # React DOM entry point
│   ├── package.json                   # Frontend npm dependencies & scripts
│   ├── tsconfig.json                  # TypeScript configuration
│   └── vite.config.ts                 # Vite bundler configuration
├── diagrams/                          # 13 version-controlled Mermaid (.mmd) diagrams
│   └── README.md
├── learning/                          # 16 private educational guides (gitignored)
├── scripts/
│   └── timed_commit_worker.py         # Autonomous timed commit manager
├── .env.example                       # Environment configuration template
├── .gitignore                         # Project-wide ignore rules
└── README.md                          # Project documentation
```

---

## ⚡ Quick Start

### 1. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed initial problems (LeetCode 1, 1968, 125, 53)
python scripts/seed_initial_problems.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Running Automated Tests
```bash
cd backend
pytest tests/ -v
```

---

## 📊 Architecture Diagrams & Learning Documents
- View comprehensive system flowcharts and sequence diagrams in [`diagrams/README.md`](diagrams/README.md).
- Dive deep into FastAPI, ASGI, SQLAlchemy, and Property-based generation in the companion educational materials in `learning/`.
