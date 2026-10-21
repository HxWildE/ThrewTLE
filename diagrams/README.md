# ThrewTLE Architecture Diagrams

This directory contains 13 version-controlled Mermaid (`.mmd`) diagrams reflecting the concrete system architecture and runtime workflows of the **ThrewTLE** application.

---

## 📋 Directory Sitemap

| Diagram File | Description | Focus Area |
| :--- | :--- | :--- |
| [`system-architecture.mmd`](system-architecture.mmd) | End-to-end full stack architecture | Browser, Vite, FastAPI, Engine, DB, Integrations |
| [`request-lifecycle.mmd`](request-lifecycle.mmd) | Problem search & test generation lifecycle | API request path, loading states, error barriers |
| [`generation-pipeline.mmd`](generation-pipeline.mmd) | Multi-layered testcase synthesis pipeline | Curated, Heuristic, Property, Validation, Deduplication |
| [`backend-module-dependencies.mmd`](backend-module-dependencies.mmd) | Python package & module dependency topology | Layered clean architecture separation |
| [`api-route-flow.mmd`](api-route-flow.mmd) | FastAPI routers, dependencies, and controllers | Route handlers, request/response schemas, DB calls |
| [`database-er.mmd`](database-er.mmd) | Relational entity-relationship schema | Tables, primary keys, foreign keys, indexes |
| [`dataset-ingestion.mmd`](dataset-ingestion.mmd) | Hugging Face corpus ETL pipeline | Extraction, schema normalization, safe upserts |
| [`daily-sync.mmd`](daily-sync.mmd) | Catalogue synchronization background worker | Idempotency, rate limiting, partial failures |
| [`test-case-validation.mmd`](test-case-validation.mmd) | Input validation vs. Oracle verification | Constraint boundary checking & expected output contracts |
| [`deployment-architecture.mmd`](deployment-architecture.mmd) | Production cloud topology | Vercel, Render, Managed PostgreSQL, Secrets |
| [`error-handling-flow.mmd`](error-handling-flow.mmd) | Defensive error boundaries & exception mappings | 404, 422, 500, unsupported formats, DB disconnects |
| [`frontend-component-flow.mmd`](frontend-component-flow.mmd) | React component hierarchy & reactive state | State transitions, custom hooks, clipboard actions |
| [`fastapi-request-internals.mmd`](fastapi-request-internals.mmd) | ASGI / Starlette / Uvicorn request internals | Byte stream, middleware stack, DI `Depends`, Pydantic |

---

## 🔍 How to View and Render These Diagrams

### Option 1: VS Code / IDE Preview
Install the **Markdown Preview Mermaid Support** or **Mermaid Chart** extension in VS Code/Cursor. Open any `.mmd` file and click the preview icon.

### Option 2: Mermaid Live Editor
Copy the content of any `.mmd` file and paste it into [Mermaid Live Editor](https://mermaid.live).

### Option 3: Command Line (Mermaid CLI)
Install `@mermaid-js/mermaid-cli`:
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagrams/system-architecture.mmd -o diagrams/system-architecture.svg
```
