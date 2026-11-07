# ThrewTLE ⚡
> **Deterministic, edge-case test case generator and validation suite for LeetCode problems to expose algorithmic edge failures before submission.**

---

## 🎯 Overview
**ThrewTLE** helps software engineers, competitive programmers, and technical interview candidates rigorously stress-test their LeetCode solutions *before* submitting to official judges. Standard LeetCode example test cases frequently miss subtle boundary conditions, alternating sign transitions, empty structures, integer overflow thresholds ($2^{31}-1$, $-2^{31}$), and quadratic worst-case inputs ($O(N^2)$ vs. $O(N)$ or $O(N \log N)$).

ThrewTLE bridges this gap by generating problem-specific, deduplicated, and constraint-verified edge test cases formatted in exact **LeetCode Raw Input** format ready for direct pasting into the custom testcase box.

---

## 🚀 Core Generation Engine & Validation

```text
┌────────────────┐      ┌─────────────────────────┐      ┌──────────────────────┐
│  Client / UI   ├─────►│ FastAPI Engine Pipeline ├─────►│  LeetCode Raw Output │
└────────────────┘      └───────────┬─────────────┘      └──────────────────────┘
                                    │
       ┌────────────────────────────┼───────────────────────────┐
       ▼                            ▼                           ▼
┌──────────────┐             ┌──────────────┐            ┌──────────────┐
│  Strategies  │             │  Validation  │            │ Deduplication│
│ (Boundaries, │             │ (AST Schema, │            │ (SHA-256     │
│  Extremes,   │             │  Reference   │            │  Structural  │
│  Stress)     │             │  Oracle)     │            │  Fingerprint)│
└──────────────┘             └──────────────┘            └──────────────┘
```

ThrewTLE incorporates a multi-tiered test generation pipeline combining property-based synthesis with targeted deterministic edge-case strategies:

- 🧱 **Boundary Strategy**: Evaluates lower/upper length limits, empty or single-element inputs, exact target zero crossings, and minimum/maximum allowable integers.
- 💥 **Extremes & Overflow Strategy**: Targets full 32-bit integer boundaries ($[-2^{31}, 2^{31}-1]$), identical element floods, and extreme dynamic range values.
- 🔥 **Stress & Worst-Case Complexity**: Crafted inputs that provoke worst-case performance pitfalls (e.g. anti-quicksort ordering, sorted/reverse-sorted arrays, hash collision patterns, and deep recursion trees).
- 🧩 **Structural Strategy**: Systematic distribution patterns including alternating signs, sparse arrays, palindrome structures, and repeated substring/array sequences.
- 🛡️ **Schema & Constraint Validator**: Strict AST-like and JSON schema parsing guaranteeing that all generated inputs adhere to individual LeetCode problem constraints.
- ⚖️ **Oracle Reference Verification**: In-memory execution against reference oracles to verify that generated edge cases have valid computable solutions.
- 🌐 **Hugging Face Normalizer**: Direct integration and normalization of LeetCode dataset problem catalogues.

---

## 🌐 API Reference

The backend exposes a clean, typed REST API under `/api/v1`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and database connectivity check |
| `GET` | `/api/v1/problems` | Search and filter indexed problems with pagination |
| `GET` | `/api/v1/problems/{slug}` | Retrieve problem metadata, constraints, and input schemas |
| `POST` | `/api/v1/problems/{slug}/generate` | Generate edge-case suite (boundary, structural, extremes, stress) |

Interactive OpenAPI documentation is hosted at `http://localhost:8000/docs`.

### Example Generation Request
```http
POST /api/v1/problems/two-sum/generate HTTP/1.1
Content-Type: application/json

{
  "count": 10,
  "categories": ["boundary", "extremes", "stress", "structural"],
  "seed": 42
}
```

The response returns canonical LeetCode raw input strings ready for one-click copy and paste:
```text
[0,0]
0
[-1000000000,1000000000]
0
[2147483647,-2147483648]
-1
```

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
│   │   │   └── v1/endpoints/          # generate, problems, health endpoints
│   │   ├── core/                      # Configuration, error handlers, logging
│   │   ├── db/                        # Database sessions, base models & fixtures
│   │   ├── engine/                    # Generation strategies, formatters, validation
│   │   │   ├── strategies/            # Boundary, extremes, stress, structural generators
│   │   │   └── validation/            # Schema validator & oracle execution engine
│   │   ├── integrations/              # Hugging Face normalizer, LeetCode client
│   │   ├── jobs/                      # Catalogue synchronization background job
│   │   ├── models/                    # SQLAlchemy 2.0 declarative models
│   │   ├── repositories/              # Database data access layer
│   │   ├── schemas/                   # Pydantic v2 request/response schemas
│   │   ├── services/                  # Problem & test generation service orchestrators
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

### 1. Environment Configuration
Copy the template and adjust environment variables if necessary:
```bash
cp .env.example .env
```

### 2. Backend Setup
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

### 3. Frontend Setup
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
python -m pytest tests/ -v
```

---

## 📊 Architecture Diagrams & Learning Documents
- View comprehensive system flowcharts and sequence diagrams in [`diagrams/README.md`](diagrams/README.md).
- Dive deep into FastAPI, ASGI, SQLAlchemy, and Property-based generation in the companion educational materials in `learning/`.
