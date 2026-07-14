# EchoMesh AI Project Tasks

Track the progress of EchoMesh AI features. Update this file as items transition through their lifecycles.

---

## 📋 Kanban Board

| 📥 Backlog | 📋 Todo | 🚀 In Progress | 🎯 Done |
| :--- | :--- | :--- | :--- |
| - Alembic DB migration system | - Database Schema Definition | - Project Initialization | - implementation_plan.md |
| - Signed S3 upload URLs | - FastAPI Core CRUD APIs | | - project foundation files |
| - Vector retrieval wrapper | - Bedrock Claude integration | | |
| - Reciprocal Rank Fusion | - Bedrock Titan embedding generator | | |
| - Graph node edge visualization | - Adjacency list CTE pathfinder | | |
| - Automated graph generator engine| - Frontend Dashboard shell | | |
| - Chatbot answering interface | - Dynamic visual Graph Canvas | | |

---

## 📝 Task Details & Checklists

### Phase 1: Foundations & Initialization
* [x] Project workspace configurations (`package.json`, `.gitignore`, `.env.example`, `docker-compose.yml`)
* [x] System and Developer Documentation (`README.md`, `PROJECT_PLAN.md`, `PROJECT_RULES.md`, `CONTRIBUTING.md`, `LICENSE`)
* [ ] Initial file scaffolds for Backend & Frontend directories

### Phase 2: Core Relational Database & CRUD
* [ ] Spin up CockroachDB instance with Docker Compose
* [ ] Write database models (`models/user.py`, `models/memory.py`, `models/team.py`, etc.)
* [ ] Configure Alembic for database schema migrations
* [ ] Implement secure authentication endpoints (JWT based)
* [ ] Implement CRUD REST APIs for memories, projects, and teams

### Phase 3: AI Service Integration
* [ ] Establish AWS IAM / Credentials connection pipeline
* [ ] Build Amazon S3 upload service for raw documents and audios
* [ ] Configure Amazon Bedrock client (Claude 3.5 & Titan v2)
* [ ] Create text extractor & chunking utility service
* [ ] Write vector creation pipeline (translating content into vector database embeddings)

### Phase 4: Graph Traversals & Search Logic
* [ ] Code SQL query templates containing recursive CTEs for graph traversals
* [ ] Build semantic cosine similarity query functions in database adapters
* [ ] Develop automated linking engine: evaluating memory context match and link classification via LLM
* [ ] Program prompt builder mapping keywords, vector outcomes, and graph traces into Claude context prompts

### Phase 5: Client Interface & Visualization
* [ ] Develop Next.js application framework with Tailwind
* [ ] Implement layout framework (Sidebar, header, workspace switcher)
* [ ] Construct Memory Explorer grid and detailed view cards
* [ ] Build interactive React component displaying memories network utilizing D3 or force-graph canvas
* [ ] Build RAG search-and-answer workspace panel
