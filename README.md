# EchoMesh AI

> The AI Memory Operating System for teams. EchoMesh AI captures, indexes, links, and navigates organizational knowledge across conversations, architecture changes, decisions, and tasks.

---

## 🌟 Vision

EchoMesh AI is built for software engineering and product teams to prevent knowledge decay and eliminate context fragmentation. Rather than a transactional chat assistant, EchoMesh AI creates an interconnected **graph of organizational memories**, allowing any member of the team to query the deep "why" behind decisions, reject options, past meeting discussions, and historical milestones.

---

## 🛠️ Technology Stack

* **Frontend**: Next.js 14+ (App Router, TypeScript), Tailwind CSS, React Query
* **Backend**: FastAPI (Python 3.11+), SQLModel / SQLAlchemy
* **Database**: CockroachDB (distributed relational & vector storage)
* **AI Layer**: Amazon Bedrock (Anthropic Claude 3.5 Sonnet & Amazon Titan Text Embeddings)
* **Infrastructure / Cloud**: AWS S3 (Document/Audio uploads), Docker Compose

---

## 📂 Directory Layout

```text
.
├── backend/                  # FastAPI Backend API service
│   ├── app/                  # Main backend codebase
│   │   ├── api/              # API router endpoints
│   │   ├── core/             # DB setups, configs, logging, security
│   │   ├── models/           # SQLAlchemy DB schema entities
│   │   ├── schemas/          # Pydantic data schemas
│   │   ├── services/         # Business logic (AI pipelines, graphs)
│   │   └── main.py           # API Entry Point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Next.js Frontend SPA UI
│   ├── src/
│   │   ├── app/              # Next.js Page components & routing
│   │   ├── components/       # Layout structures and UI nodes
│   │   ├── hooks/            # API integration query hooks
│   │   ├── lib/              # Client API connection config
│   │   └── types/            # Type bindings
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml        # Orchestration (DB, API, SPA)
├── .env.example              # Environments template
└── package.json              # Monorepo NPM workspace config
```

---

## 🚀 Quick Start Guide

### Prerequisites
* Docker & Docker Compose
* Python 3.11+ (for local backend development)
* Node.js 18+ (for local frontend development)

### Step 1: Clone and Configure Environments
```bash
# Copy env example
cp .env.example .env
```
Update the keys inside `.env` with your AWS and CockroachDB secrets.

### Step 2: Build & Start Services
```bash
# Start all services with Docker Compose
docker-compose up --build
```
This launches:
* **CockroachDB**: SQL endpoint at `localhost:26257` and DB Admin dashboard at `localhost:8080`.
* **FastAPI Backend**: API routes running at `localhost:8000`.
* **Next.js Frontend**: Portal UI running at `localhost:3000`.

---

## 📝 Planning Documents

Refer to our dedicated project management guides for architecture decisions and guides:
* [PROJECT_PLAN.md](file:///c:/Users/Lavannya%20Hedaoo/OneDrive/Documents/EchoMesh%20AI/PROJECT_PLAN.md) — Timelines, milestones, and deliverables.
* [PROJECT_RULES.md](file:///c:/Users/Lavannya%20Hedaoo/OneDrive/Documents/EchoMesh%20AI/PROJECT_RULES.md) — Coding rules, guidelines, clean architecture standards.
* [TASKS.md](file:///c:/Users/Lavannya%20Hedaoo/OneDrive/Documents/EchoMesh%20AI/TASKS.md) — Action items board (Backlog/Todo/Progress).
* [CONTRIBUTING.md](file:///c:/Users/Lavannya%20Hedaoo/OneDrive/Documents/EchoMesh%20AI/CONTRIBUTING.md) — Branch naming, PR policies, setup rules.
