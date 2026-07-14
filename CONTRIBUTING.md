# Contributing to EchoMesh AI

We welcome contributions from the founding team to build and scale EchoMesh AI! Follow these guidelines to maintain consistency and quality across the codebase.

---

## 🌿 Git & Branching Strategy

We follow a structured branch naming convention to keep our git history clean and readable:

```text
feature/    -> New feature developments (e.g., feature/memory-ingestion-api)
bugfix/     -> Resolving bugs or issues (e.g., bugfix/db-connection-leak)
docs/       -> Documentation changes (e.g., docs/update-api-spec)
refactor/   -> Code reorganization without behavior changes (e.g., refactor/graph-service-query)
test/       -> Adding or updating test configurations (e.g., test/memory-crud-endpoints)
```

### Development Workflow
1. Create your branch from the `main` branch.
2. Commit changes using descriptive, atomic commit messages.
3. Push your branch and open a Pull Request (PR) targeting `main`.
4. Ensure all automated tests build and pass before merging.

---

## 💻 Coding Style & Standards

Ensure you adhere to the project styles outlined in [PROJECT_RULES.md](file:///c:/Users/Lavannya%20Hedaoo/OneDrive/Documents/EchoMesh%20AI/PROJECT_RULES.md):

* **Python (Backend)**:
  - Adhere to **PEP 8** formatting style.
  - Run `black` or `ruff` formatting before committing code.
  - Keep type annotations complete for all functions.

* **TypeScript (Frontend)**:
  - Use `prettier` and `eslint` constraints configured in the workspace.
  - Keep client vs server component flags clean.
  - Do not use `any` types; define complete interface parameters.

---

## 🛠️ Local Environment Pull Requests Guidelines

* **Keep PRs Focused**: Avoid batching unrelated changes (e.g. updating schemas and fixing UI alignment in the same PR).
* **Verify Database Status**: If your changes include database schema additions, ensure you include Alembic migration files in the PR.
* **Write Unit Tests**: Include test scripts coverages for new service methods and core API configurations.
