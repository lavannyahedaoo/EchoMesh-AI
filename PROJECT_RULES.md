# Project Rules & Coding Standards

This document establishes the architecture directives, engineering guidelines, and code quality expectations for the EchoMesh AI codebase.

---

## 🏛️ Architectural Principles

### 1. Clean Architecture
We enforce separation of concerns across distinct layers to maintain high testability and keep the system decoupled:
* **Entities / Models**: Pure database representation containing schema fields and relationships (e.g. `backend/app/models`).
* **Schemas / DTOs**: Input/output serialization schemas (Pydantic / TypeScript types) validating network boundaries.
* **Services / Business Logic**: Pure business workflow processing (e.g. AI extraction, graph traversals). No direct dependence on HTTP request contexts.
* **API Controllers / Routes**: Handle routing, security middleware, and HTTP response mapping.

### 2. SOLID Principles
* **Single Responsibility**: Each module, service, class, or React component must have a single reason to change. Separate AI prompt building from API route orchestration.
* **Open/Closed**: Service definitions must be open for extension but closed for modification. Implement adapters for changing external tools (e.g., Bedrock vs. OpenAI API).
* **Liskov Substitution**: Inherited classes must be substitutable for their base forms without breaking behavior.
* **Interface Segregation**: Clients must not depend on interface methods they do not use. Keep schema boundaries narrow.
* **Dependency Inversion**: Higher-level services must not import concrete lower-level modules directly; they rely on abstractions or dependency injection (e.g., FastAPI's `Depends` for db sessions or credentials).

### 3. Modular Design
We organize the project by domain rather than function where possible. Avoid generic "utils" folders; place utilities in their specific domains (e.g. chunking helpers in `services/memory_service.py`).

---

## 🐍 Backend Guidelines (FastAPI & Python)

* **Asynchronous I/O**: Use `async def` for I/O bound endpoints, database access, and network requests. Use standard `def` only for cpu-bound computation or synchronous libraries.
* **Type Annotations**: Strict typing is required across all Python declarations. Run type checkers (like `mypy` or `pyright`) to enforce validity.
* **Database Session Management**: Use SQLAlchemy's `AsyncSession` with context managers or FastAPI `Depends` to guarantee proper connection closing and transaction rollbacks on failure.
* **Environment Variables**: Read configurations strictly via Pydantic Settings base classes (`backend/app/core/config.py`). Do not call `os.getenv` directly in business logic.
* **Logging Framework**: Use structural JSON logging for production. Log relevant identifiers (e.g., `user_id`, `memory_id`) and avoid logging sensitive user passwords.
  ```python
  import logging
  logger = logging.getLogger("echomesh")
  logger.info("Successfully ingested memory", extra={"memory_id": memory.id})
  ```
* **Error Handling**: Use custom application exceptions that map to specific HTTP statuses via exception handlers, avoiding generic `try-except Exception` blocks unless re-raising structured details.
  ```python
  class MemoryNotFoundError(Exception):
      def __init__(self, memory_id: UUID):
          self.memory_id = memory_id
  ```

---

## ⚛️ Frontend Guidelines (Next.js & Tailwind CSS)

* **App Router**: Use Next.js App Router folders (`app/`). Leverage React Server Components (RSC) for initial page loads and search engine metadata representation.
* **Client Components**: Mark files with `'use client'` only when they contain client states, event listeners, or require browser APIs (e.g. interactive graph canvas, query controls).
* **Styling & Aesthetics**:
  - Use Tailwind CSS with organized variables (declared in `frontend/tailwind.config.ts` and `frontend/src/app/globals.css`).
  - Rely on harmonious color scales (dark/neutral bases combined with soft colored accents) instead of high-contrast generic colors.
  - Implement smooth transitions (`transition-all duration-300`) and subtle hover offsets to provide a premium feel.
* **Component Design**: Build reusable components inside `components/ui/` (e.g. Buttons, Modals, Cards) and separate them from layout templates.
* **Data Fetching & State**: Use React Query (TanStack Query) to manage API interactions, query caching, loading animations, and automatic retries.

---

## 🧪 Testing Strategy

* **Unit Tests**:
  - Backend: Use `pytest` and `httpx.AsyncClient` to mock API requests. Mock Bedrock/LLM payloads to ensure tests run offline.
  - Frontend: Use Jest and React Testing Library to test key component interactions.
* **Integration Tests**:
  - Test database integrations using a Docker CockroachDB test database. Clean database states before and after each test case.
* **Testing Command standard**:
  - Python tests: `pytest -v` inside `backend/` directory.
  - Frontend tests: `npm test` inside `frontend/` directory.

---

## 📖 Documentation Standards

* **Docstrings**: Document every class, public service function, and API path using Google-style Python docstrings.
* **Self-Documenting API**: Declare request parameters, response models, validation bounds, and description metadata directly in FastAPI routes to generate clear OpenAPI Swagger documentation.
* **Code Comments**: Add comments explaining complex algorithms or reasoning (e.g., explaining custom cosine distance calculations in SQL or graph edge classification prompts).
