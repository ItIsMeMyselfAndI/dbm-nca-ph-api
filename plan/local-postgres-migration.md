# Plan: Local PostgreSQL via API Versioning (v1 Supabase ↔ v2 Postgres)

## Overview

Add a local PostgreSQL backend via **API versioning** — v1 continues with Supabase untouched, v2 introduces async Postgres via SQLAlchemy. Both share entities and interfaces. No breaking changes.

---

## 1. Problem / Solution / Impact / Goal

| Problem | Solution | Impact | Goal |
|---------|----------|--------|------|
| Database is cloud-only (Supabase); every dev session needs network + API keys | Add `DATABASE_URL`-based local Postgres as v2; v1 Supabase stays fully functional | Developers can run offline via v2; CI uses v2 with ephemeral Postgres; v1 remains for prod compatibility | Coexistence: `GET /api/v1/releases` hits Supabase, `GET /api/v2/releases` hits local Postgres |
| Supabase SDK is REST-based — no connection pooling, prepared statements, or raw SQL | v2 uses SQLAlchemy 2.0 async + asyncpg — pooling, prepared statements, full SQL | 10-100x faster local queries; production still uses Supabase REST via v1 | v2 queries run at sub-5ms locally vs 50-200ms Supabase REST |
| Repository implementations are hard-coupled to Supabase `.eq()/.gt()` builder | New `Postgres*Repository` classes implement the same Protocols | Zero changes to entities, interfaces, or v1 code | Both v1 and v2 satisfy identical Protocol contracts |
| No migration tooling — schema managed manually | Alembic for v2 schema versioning | Auditable, reversible, automated schema changes | `alembic upgrade head` creates the full schema |
| No local dev bootstrap — every new dev needs Supabase account | Local Postgres + seed script | One-time Postgres setup + `alembic upgrade head` + `python scripts/seed.py` | Clone → 3 commands → working API |

---

## 2. Architecture

```
Request
  ├── /api/v1/*  →  v1 routes (sync)            →  v1 use cases (sync)   →  Supabase repos  →  Supabase PG
  └── /api/v2/*  →  v2 routes (async, FastAPI)   →  v2 use cases (async)  →  Postgres repos   →  SQLAlchemy → Local PG
    
Shared: core/entities/, core/interfaces/, presentation/api/schemas.py
```

---

## 3. Directory Structure (After)

```
src/
├── core/
│   ├── entities/                       # UNCHANGED
│   ├── exceptions.py                   # NEW: NotFoundError, ValidationError
│   ├── interfaces/                     # UNCHANGED (sync Protocols) + NEW async Protocols
│   └── use_cases/
│       ├── v1/                         # MOVED originals here
│       │   ├── release/
│       │   ├── record/
│       │   └── allocation/
│       └── v2/                         # NEW async use cases
│           ├── _cursor.py              # NEW: shared compute_next_cursor helper
│           ├── release/
│           ├── record/
│           └── allocation/
├── infrastructure/
│   └── db/
│       ├── supabase_client.py          # UNTOUCHED
│       ├── supabase_release_repo.py    # UNTOUCHED
│       ├── supabase_record_repo.py     # UNTOUCHED
│       ├── supabase_allocation_repo.py # UNTOUCHED
│       ├── database.py                 # NEW: async engine + session
│       ├── models.py                   # NEW: SQLAlchemy ORM models
│       ├── postgres_release_repo.py    # NEW
│       ├── postgres_record_repo.py     # NEW
│       └── postgres_allocation_repo.py # NEW
├── presentation/
│   └── api/
│       ├── schemas.py                  # UNCHANGED (shared)
│       ├── dependencies.py             # UNCHANGED (v1 still uses this)
│       ├── dependencies_v2.py          # NEW: DI for v2
│       ├── v1/                         # UNTOUCHED (import paths only)
│       │   └── routers/
│       │       ├── releases.py
│       │       ├── records.py
│       │       └── allocations.py
│       └── v2/                         # NEW async routes
│           └── routers/
│               ├── releases.py
│               ├── records.py
│               └── allocations.py
```

---

## 4. Implementation Checklist (14 items)

- [x] **PH1**: Restructure use cases - move v1 to `core/use_cases/v1/`, update all imports, delete originals
- [x] **PH2**: Create v2 async use cases in `core/use_cases/v2/` with improvements
- [x] **PH3**: Add dependencies (`sqlalchemy`, `asyncpg`) + `DATABASE_URL` config
- [x] **PH4**: Create `database.py` (async engine + session factory)
- [x] **PH5**: Create SQLAlchemy `models.py`
- [x] **PH6**: Create `PostgresReleaseRepository`
- [x] **PH7**: Create `PostgresRecordRepository`
- [x] **PH8**: Create `PostgresAllocationRepository`
- [x] **PH9**: Create `dependencies_v2.py`
- [x] **PH10**: Create v2 routes (`presentation/api/v2/routers/`)
- [x] **PH11**: Register v2 router in `main.py`
- [x] **PH12**: Local PostgreSQL setup (one-time) + Alembic initialization
- [x] **PH13**: Seed script (`scripts/seed.py`)
- [ ] **PH14**: Run tests + verify no regressions

---

## 5. Phase 1 Detail — Move v1 Use Cases

### Files to Create (12)

| File | Source |
|------|--------|
| `core/use_cases/v1/__init__.py` | Empty |
| `core/use_cases/v1/release/__init__.py` | Empty |
| `core/use_cases/v1/release/list_releases.py` | Copy of `core/use_cases/release/list_releases.py` |
| `core/use_cases/v1/release/get_release_by_id.py` | Copy of original |
| `core/use_cases/v1/record/__init__.py` | Empty |
| `core/use_cases/v1/record/list_records.py` | Copy of original |
| `core/use_cases/v1/record/get_record_by_id.py` | Copy of original |
| `core/use_cases/v1/record/list_records_by_filter.py` | Copy of original |
| `core/use_cases/v1/allocation/__init__.py` | Empty |
| `core/use_cases/v1/allocation/list_allocations.py` | Copy of original |
| `core/use_cases/v1/allocation/get_allocation_by_id.py` | Copy of original |
| `core/use_cases/v1/allocation/list_allocations_by_filter.py` | Copy of original |

### Files to Update Imports (10)

| File | Import change |
|------|--------------|
| `presentation/api/v1/routers/releases.py` | `v1.release.` prefix (2 lines) |
| `presentation/api/v1/routers/records.py` | `v1.record.` prefix (3 lines) |
| `presentation/api/v1/routers/allocations.py` | `v1.allocation.` prefix (3 lines) |
| `tests/core/use_cases/release/test_list_releases.py` | `v1.release.` prefix |
| `tests/core/use_cases/release/test_get_release_by_id.py` | `v1.release.` prefix |
| `tests/core/use_cases/record/test_list_records.py` | `v1.record.` prefix |
| `tests/core/use_cases/record/test_get_record_by_id.py` | `v1.record.` prefix |
| `tests/core/use_cases/record/test_list_records_by_filter.py` | `v1.record.` prefix |
| `tests/core/use_cases/allocation/test_list_allocations.py` | `v1.allocation.` prefix |
| `tests/core/use_cases/allocation/test_get_allocation_by_id.py` | `v1.allocation.` prefix |
| `tests/core/use_cases/allocation/test_list_allocations_by_filter.py` | `v1.allocation.` prefix |

### Files to Delete (8)

- `core/use_cases/release/list_releases.py`
- `core/use_cases/release/get_release_by_id.py`
- `core/use_cases/record/list_records.py`
- `core/use_cases/record/get_record_by_id.py`
- `core/use_cases/record/list_records_by_filter.py`
- `core/use_cases/allocation/list_allocations.py`
- `core/use_cases/allocation/get_allocation_by_id.py`
- `core/use_cases/allocation/list_allocations_by_filter.py`

### Files Left Untouched (critical)

- `core/entities/*.py` — domain models shared by v1 + v2
- `core/interfaces/*.py` — repository Protocols shared by v1 + v2
- `core/entities/record_filter.py`, `allocation_filter.py` — filter enums
- `infrastructure/db/supabase_*` — v1 continues using these
- `presentation/api/schemas.py` — response schemas shared
- `presentation/api/dependencies.py` — v1 continues using this
- `tests/conftest.py` — still overrides v1 DI functions
- `tests/mock/` — mock repos still implement v1 Protocols
- `infrastructure/config.py` — unchanged in Phase 1
- `main.py` — unchanged in Phase 1

---

## 6. Phase 2 Detail — v2 Async Use Cases

### Improvements over v1 (you chose "improve while porting")

1. **Validation-first**: Validate cursor format and bounds *before* any async repo call. v1 calls `get_by_id` to verify cursor exists — wasteful double call.
2. **Custom exceptions**: `NotFoundError`, `ValidationError` instead of bare `ValueError`.
3. **Shared cursor helper**: `_compute_next_cursor(items)` extracted once, not inlined 6 times.
4. **Typed return**: Same `Tuple[List[Entity], str | None]` signature for backward compat.

### What's the same

- Same constructor injection pattern (Protocol in constructor)
- Same `execute(...)` method name and return types
- Same validation rules (limit > 0, cursor not empty)

---

## 7. Phases 3-5 Detail — Infrastructure

### Dependencies

```
sqlalchemy>=2.0.30
asyncpg>=0.29.0
alembic>=1.13.0
```

### `config.py` addition

```python
DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dbm_nca_ph"
```

### Models (3 SQLAlchemy tables)

- `ReleaseModel` → `release` table: `id` (text PK), `title`, `filename`, `url`, `year`, `page_count`, timestamps
- `RecordModel` → `record` table: `id` (uuid PK), `nca_number` (unique), `nca_type`, `department`, `released_date`, `purpose`, `release_id` (FK → release)
- `AllocationModel` → `allocation` table: `id` (uuid PK), `operating_unit`, `agency`, `amount`, `nca_number` (FK → record)

All with `DateTime(timezone=True)` timestamps, UUID defaults via `gen_random_uuid()`.

### Postgres Repositories (3 files)

Each implements the corresponding Protocol from `core/interfaces/` but with `async def` methods.
Same cursor-based pagination as Supabase repos.

### Dependency Injection (`dependencies_v2.py`)

```python
def get_release_repository() -> PostgresReleaseRepository:
    return PostgresReleaseRepository()
```
(Separate from v1's `dependencies.py` — no collision)

### v2 Routes

`async def` handlers calling v2 async use cases. Same request/response schemas as v1.
Registered at `/api/v2/*` in `main.py`.

---

## 8. Files Untouched (Entire Project)

| Directory/File | Reason |
|----------------|--------|
| `core/entities/*.py` | Domain models — database agnostic, shared by v1+v2 |
| `core/interfaces/async_*_repository.py` | NEW async protocols for v2 repos |
| `core/interfaces/*.py` (sync) | Protocol contracts — implemented by Supabase repos |
| `core/entities/record_filter.py` | Shared enum |
| `core/entities/allocation_filter.py` | Shared enum |
| `presentation/api/schemas.py` | Response schemas — shared by v1+v2 routes |
| `presentation/api/dependencies.py` | v1 DI — untouched |
| `presentation/api/v1/` (routers, not imports) | v1 route logic — untouched, only import paths change |
| `infrastructure/db/supabase_client.py` | v1 still uses this |
| `infrastructure/db/supabase_*_repository.py` | v1 still uses these |
| `core/exceptions.py` | NEW custom exceptions (NotFoundError, ValidationError) |
| `infrastructure/config.py` | Untouched in Phase 1; `DATABASE_URL` added in Phase 3 |
| `tests/conftest.py` | Overrides v1 DI — untouched |
| `tests/mock/` | Mock repos implement v1 Protocols — untouched |
| `main.py` | Untouched until Phase 11 when v2 is registered |
| `vercel.json` | Deployment config — no change |
| `requirements.txt` | Untouched until Phase 3 |

---

## 10. Local PostgreSQL Setup Guide (One-Time)

### Prerequisites

PostgreSQL must be installed and running on your machine.

**Arch Linux:**
```bash
sudo pacman -S postgresql
sudo -iu postgres initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Debian/Ubuntu:**
```bash
sudo apt update && sudo apt install postgresql postgresql-client
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 1: Create the database user and database

```bash
sudo -iu postgres createuser --superuser eger
sudo -iu postgres createdb -O eger dbm_nca_ph
```

If you want to use the default `postgres` user instead (matching `DATABASE_URL` in config):

```bash
sudo -iu postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -iu postgres createdb -O postgres dbm_nca_ph
```

### Step 2: Verify connection

```bash
psql -U postgres -h localhost -d dbm_nca_ph -c "SELECT 1;"
```

If you get `Peer authentication failed`, edit `pg_hba.conf`:

```bash
sudo -iu postgres psql -c "SHOW hba_file;"
# Edit the file, change "peer" to "md5" for 127.0.0.1/32 and ::1/128 lines
sudo systemctl restart postgresql
```

### Step 3: Update `.env`

Add or update your `.env` file:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/dbm_nca_ph
```

### Step 4: Initialize Alembic and create tables

```bash
alembic init alembic
# Configure alembic.ini with the DATABASE_URL
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

Or use the models directly to create tables (simpler):

```python
# scripts/create_tables.py
import asyncio
from src.infrastructure.db.database import engine
from src.infrastructure.db.models import Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


asyncio.run(main())
```

### Step 5: Verify tables

```bash
psql -U postgres -h localhost -d dbm_nca_ph -c "\dt"
```

Should show: `release`, `record`, `allocation`.

---

## 9. Syncing to Server (Target: `eger@100.105.114.70`)

### Remote Setup (one-time)

```bash
ssh eger@100.105.114.70
rm -rf /home/eger/projects/dbm-nca-ph-api /home/eger/local-repos/dbm-nca-ph-api.git
mkdir -p /home/eger/local-repos/dbm-nca-ph-api.git
cd /home/eger/local-repos/dbm-nca-ph-api.git
git init --bare
exit

# On Arch dev machine
git remote add debian ssh://eger@100.105.114.70/home/eger/local-repos/dbm-nca-ph-api.git
```

### After every commit

```bash
git push debian main
```

### On server (for active work)

```bash
ssh eger@100.105.114.70
cd /home/eger/projects
git clone /home/eger/local-repos/dbm-nca-ph-api.git
# Subsequent updates:
cd /home/eger/projects/dbm-nca-ph-api
git pull origin main
```
