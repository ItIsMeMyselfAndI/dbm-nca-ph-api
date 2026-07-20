# Test Documentation

## Overview

The project has **two test tiers**:

| Tier | Directory | Backend | Tests |
|------|-----------|---------|-------|
| v1 | `tests/v1/` | Mock repositories (in-memory) | Unit tests for Supabase-backed endpoints |
| v2 | `tests/v2/` | Real PostgreSQL (temp DB) | Integration + unit tests for PostgreSQL-backed endpoints |

**Total v2 tests:** 135 (82 integration + 53 unit)

---

## v2 Test Structure

```
tests/v2/
├── conftest.py                        # DB lifecycle, seed fixtures, auth fixture
├── core/
│   └── use_cases/
│       ├── allocation/
│       │   ├── test_get_allocation_by_id.py
│       │   ├── test_list_allocations.py
│       │   └── test_list_allocations_by_filter.py
│       ├── record/
│       │   ├── test_get_record_by_id.py
│       │   ├── test_list_records.py
│       │   └── test_list_records_by_filter.py
│       └── release/
│           ├── test_get_release_by_id.py
│           └── test_list_releases.py
└── presentation/
    └── api/
        └── routers/
            ├── private/               # Write endpoints (require X-API-Key)
            │   ├── test_auth.py
            │   ├── allocation/
            │   │   ├── test_upsert_allocation.py
            │   │   └── test_delete_allocation.py
            │   ├── record/
            │   │   ├── test_upsert_record.py
            │   │   └── test_delete_record.py
            │   └── release/
            │       ├── test_upsert_release.py
            │       └── test_delete_release.py
            └── public/                # Read endpoints (no auth)
                ├── allocation/
                │   ├── test_get_allocation_by_id.py
                │   ├── test_list_allocations.py
                │   └── test_list_allocations_by_filter.py
                ├── record/
                │   ├── test_get_record_by_id.py
                │   ├── test_list_records.py
                │   └── test_list_records_by_filter.py
                └── release/
                    ├── test_get_release_by_id.py
                    └── test_list_releases.py
```

---

## How v2 Tests Work

### Database Lifecycle (`tests/v2/conftest.py`)

| Phase | Fixture | Scope | What it does |
|-------|---------|-------|-------------|
| Setup | `db_lifecycle` | Session | Connects to `postgres` DB, **drops** `dbm_nca_ph_test` if exists, creates fresh `dbm_nca_ph_test`, creates `release`, `record`, `allocation` tables |
| Per-test cleanup | `clean_db` | Function | Deletes all rows from all 3 tables (keeps schema) |
| Seed | `seed_releases` | Function | Inserts 3 test releases |
| Seed | `seed_records` | Function | Inserts 3 test records (depends on `seed_releases`) |
| Seed | `seed_allocations` | Function | Inserts 3 test allocations (depends on `seed_records`) |
| Teardown | `db_lifecycle` | Session | Drops all tables, **drops** `dbm_nca_ph_test` |

### Auth for Write Endpoints

- Write endpoints are mounted under `/api/v2/private/`
- The private router has `dependencies=[Depends(require_pipeline_key)]`
- The test client sends `X-API-Key: test-api-key-123` via the `auth_header` fixture
- Auth is set via `PIPELINE_API_KEY` env var (defaults to `test-api-key-123` in conftest)

---

## Running Tests

```bash
# All v2 tests
pytest tests/v2/

# Specific module
pytest tests/v2/presentation/api/routers/public/release/

# Specific test file
pytest tests/v2/presentation/api/routers/private/release/test_upsert_release.py

# With verbose output
pytest tests/v2/ -v

# Stop on first failure
pytest tests/v2/ -x

# Run both v1 and v2
pytest
```

---

## Prerequisites

### PostgreSQL

A running **local PostgreSQL** instance is required. The test suite:

1. Creates a temporary `dbm_nca_ph_test` database
2. Runs all tests
3. Drops the database

### Database Credentials

The test suite uses `asyncpg` to manage the test database directly (not SQLAlchemy). The credentials are derived from the `DATABASE_URL` environment variable:

- **Host:** extracted from `DATABASE_URL` (default: `localhost`)
- **Port:** extracted from `DATABASE_URL` (default: `5432`)
- **User:** extracted from `DATABASE_URL` (default: `postgres`)
- **Password:** extracted from `DATABASE_URL` (default: empty)

Make sure the PostgreSQL role used in `DATABASE_URL` has `CREATEDB` privileges (superuser recommended), since the test suite creates and drops databases.

### Troubleshooting Connection Failures

**Symptom:** Tests fail immediately with connection errors like:
```
asyncpg.exceptions.InvalidAuthorizationSpecificationError
```
or
```
asyncpg.exceptions.ConnectionDoesNotExistError
```

**Common causes:**

| Cause | Fix |
|-------|-----|
| PostgreSQL not running | `sudo systemctl start postgresql` |
| Wrong credentials in `DATABASE_URL` | Check your `.env` — test suite reads from this variable |
| `peer` auth on Unix socket | Add `host all all 127.0.0.1/32 trust` to `pg_hba.conf` and restart PostgreSQL |
| Role lacks `CREATEDB` | `sudo -iu postgres psql -c "ALTER ROLE <user> CREATEDB;"` |
| Test database name conflict | The suite drops/recreates `dbm_nca_ph_test` — ensure no important DB has this name |

### Verify Setup

```bash
# Test that asyncpg can connect
python -c "
import asyncpg, asyncio
async def check():
    conn = await asyncpg.connect('postgresql://postgres@localhost:5432/postgres')
    print('OK:', await conn.fetchval('SELECT version()'))
    await conn.close()
asyncio.run(check())
"
```

---

## Test Coverage

### Integration Tests (82)

Test the full stack: HTTP request → router → use case → real PostgreSQL → response.

| Area | Tests | What's covered |
|------|-------|----------------|
| Auth guard | 4 | Missing key, invalid key, empty key, authenticated delete |
| Public reads | 56 | Pagination (limit, cursor, edge cases), filtering, not-found, whitespace/case handling |
| Private writes | 22 | Create, update (upsert), delete, missing fields, invalid types, empty body, FK violations |

### Unit Tests (53)

Test use case logic with mock repositories (no DB).

| Area | Tests | What's covered |
|------|-------|----------------|
| List use cases | 27 | Pagination, cursor encoding/decoding, limits, edge cases, no results |
| Get-by-ID use cases | 15 | Found, not-found, empty string, uppercase, spaces |
| Filter use cases | 11 | Filtering by various fields, no match, invalid filter key, cursor pagination |

### Known Gaps

| Gap | Severity | Details |
|-----|----------|---------|
| No unit tests for pipeline write use cases | Medium | `tests/v2/core/use_cases/pipeline/` exists but has no test files. The business logic of UpsertRelease, DeleteRelease, UpsertRecord, DeleteRecord, UpsertAllocation, and DeleteAllocation is only tested via integration tests. |
| No unit tests for cursor utility | Low | `src/core/use_cases/v2/_cursor.py` has no dedicated tests |
| No rate limit tests | Low | Rate limiting (`1000/hour` via slowapi) is untested |

---

## Environment Variables Used by Tests

| Variable | Default | Used by | Purpose |
|----------|---------|---------|---------|
| `DATABASE_URL` | — | v2 tests | PostgreSQL connection string for test DB management |
| `PIPELINE_API_KEY` | `test-api-key-123` | v2 private tests | API key for write endpoint auth |
| `SUPABASE_URL` | `http://test.local` | v1 tests | (v1 only) |
| `SUPABASE_ANON_KEY` | `test-anon-key` | v1 tests | (v1 only) |
