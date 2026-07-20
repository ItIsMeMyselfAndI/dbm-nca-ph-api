# Implementation Plan: Real-DB Integration Tests for v2 Routes

## 1. Context & Objectives
* **User Intent:** Router tests should hit a real PostgreSQL database (auto-created/destroyed) and the real FastAPI application.
* **Goal:** Replace async mock repos with a test database that is created per test session, seeded with `test_`-prefixed data, and destroyed after.
* **Current State:** All router test source files were previously deleted. Only `__pycache__` bytecode remnants exist.
* **Target Implementation:** Create `public/` and `private/` test dirs under `tests/v2/presentation/api/routers/`. All tests use a real PostgreSQL database (`dbm_nca_ph_test`) that is auto-created at session start and dropped at session end.

## 2. Key Requirements

1. **Auto-create/destroy test DB** — `CREATE DATABASE dbm_nca_ph_test` at session start, `DROP DATABASE` at end
2. **`test_` prefix** — All seed data values prefixed with `test_` (e.g., `test_release_2024`, `test_nca_001`)
3. **Real DB for all endpoint tests** — No mocks. Router tests exercise the full stack: HTTP → router → use case → repo → PostgreSQL
4. **Auth tested real** — `require_pipeline_key` reads from real env var; tests send `X-API-Key` header

## 3. Scope

### Modified Files
| File | Changes |
| :--- | :--- |
| `tests/v2/conftest.py` | Full rewrite: DB lifecycle (create/drop), engine, table creation, cleanup, client, seed helpers |
| `tests/v2/presentation/api/routers/__init__.py` | Keep as-is |
| Delete: `allocation/`, `record/`, `release/` dirs (empty, leftover) | Clean up old structure |

### Created Files
| File | Purpose |
| :--- | :--- |
| `tests/v2/presentation/api/routers/public/__init__.py` | Package marker |
| `tests/v2/presentation/api/routers/public/release/__init__.py` + `test_list_releases.py` + `test_get_release_by_id.py` | Public read tests for releases |
| `tests/v2/presentation/api/routers/public/record/__init__.py` + `test_list_records.py` + `test_get_record_by_id.py` + `test_list_records_by_filter.py` | Public read tests for records |
| `tests/v2/presentation/api/routers/public/allocation/__init__.py` + `test_list_allocations.py` + `test_get_allocation_by_id.py` + `test_list_allocations_by_filter.py` | Public read tests for allocations |
| `tests/v2/presentation/api/routers/private/__init__.py` | Package marker |
| `tests/v2/presentation/api/routers/private/test_auth.py` | Auth failure tests |
| `tests/v2/presentation/api/routers/private/release/test_upsert_release.py` + `test_delete_release.py` | Private write tests for releases |
| `tests/v2/presentation/api/routers/private/record/test_upsert_record.py` + `test_delete_record.py` | Private write tests for records |
| `tests/v2/presentation/api/routers/private/allocation/test_upsert_allocation.py` + `test_delete_allocation.py` | Private write tests for allocations |

## 4. Data Design

All seed values use `test_` prefix:

| Entity | Key Field | Example Values |
| :--- | :--- | :--- |
| Release | `id` | `test_release_a`, `test_release_b`, `test_release_c` (sort-safe for cursor pagination) |
| Record | `nca_number` | `test_nca_001`, `test_nca_002`, `test_nca_003` |
| Record | `release_id` | `test_release_a` (FK to Release) |
| Allocation | `nca_number` | `test_nca_001` (FK to Record) |
| Allocation | `agency` | `test_agency_one`, `test_agency_two` |
| Allocation | `operating_unit` | `test_ou_north`, `test_ou_south` |

## 5. Execution Plan

**Phase 1: conftest.py** — DB lifecycle, engine, cleanup, client, seed fixtures
**Phase 2: Public read tests** — 8 test files for releases, records, allocations
**Phase 3: Private write tests** — 7 test files (6 entity + 1 auth)
**Phase 4: Cleanup** — Remove old empty dirs and `__pycache__`
**Phase 5: Run** — `pytest tests/v2/ -v`, fix failures
