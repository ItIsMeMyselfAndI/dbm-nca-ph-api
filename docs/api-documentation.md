# DBM NCA PH API — Documentation

## Overview

A FastAPI application that serves Philippine DBM (Department of Budget and Management) Notice of Cash Allocation (NCA) data. Built with Clean Architecture, it exposes both a synchronous (v1) and asynchronous (v2) API over identical read endpoint surfaces, plus a set of authenticated write endpoints.

## Architecture

```
main.py                          Application entry point
src/
  core/             Domain layer (entities, use cases, interfaces, exceptions)
  infrastructure/   Data layer (Supabase repos, PostgreSQL repos, ORM models)
  presentation/     Presentation layer (FastAPI routers, Pydantic schemas, DI)
    api/
      v1/
        routers/
          public/   Read-only endpoints (list, get-by-id, filter)
      v2/
        routers/
          public/   Read-only endpoints (async)
          private/  Write endpoints (create, update, delete) — auth at package level
```

**Dependency rule**: Presentation depends on Core. Infrastructure implements Core interfaces.

## Data Model

```
Release (1) ──has_many──> Record (1) ──has_many──> Allocation
```

### Release
| Field | Type | Notes |
|-------|------|-------|
| `id` | `string` (PK) | DBM release identifier |
| `title` | `string` | Release title |
| `url` | `string` | Link to source PDF |
| `filename` | `string` | PDF filename |
| `year` | `integer` | Release year |
| `page_count` | `integer` | Number of pages |
| `file_meta_created_at` | `datetime` | |
| `file_meta_modified_at` | `datetime` | |

### Record
| Field | Type | Notes |
|-------|------|-------|
| `id` | `UUID` (PK) | Auto-generated |
| `nca_number` | `string` (unique) | NCA identifier |
| `nca_type` | `string` | Type of NCA |
| `department` | `string` | Department name |
| `released_date` | `string` | Date of release |
| `purpose` | `text` | Purpose description |
| `release_id` | `string` (FK → Release) | Parent release |

### Allocation
| Field | Type | Notes |
|-------|------|-------|
| `id` | `UUID` (PK) | Auto-generated |
| `operating_unit` | `string` | Operating unit |
| `agency` | `string` | Agency name |
| `amount` | `float` | Allocated amount |
| `nca_number` | `string` (FK → Record) | Parent record |

## API Endpoints

### GET Endpoints

#### v1 — Synchronous (`/v1/`)
Backend: **Supabase REST API** via `supabase-py`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/releases` | List releases (cursor pagination) |
| `GET` | `/v1/releases/{id}` | Get release by ID |
| `GET` | `/v1/records` | List records (cursor pagination) |
| `GET` | `/v1/records/{id}` | Get record by ID |
| `GET` | `/v1/records/{filter_key}/{filter_value}` | List records by filter |
| `GET` | `/v1/allocations` | List allocations (cursor pagination) |
| `GET` | `/v1/allocations/{id}` | Get allocation by ID |
| `GET` | `/v1/allocations/{filter_key}/{filter_value}` | List allocations by filter |
| `GET` | `/v1/docs` | Swagger UI |

#### v2 — Asynchronous (`/v2/`)
Backend: **PostgreSQL** via SQLAlchemy + `asyncpg`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v2/releases` | List releases (cursor pagination) |
| `GET` | `/v2/releases/{id}` | Get release by ID |
| `GET` | `/v2/records` | List records (cursor pagination) |
| `GET` | `/v2/records/{id}` | Get record by ID |
| `GET` | `/v2/records/{filter_key}/{filter_value}` | List records by filter |
| `GET` | `/v2/allocations` | List allocations (cursor pagination) |
| `GET` | `/v2/allocations/{id}` | Get allocation by ID |
| `GET` | `/v2/allocations/{filter_key}/{filter_value}` | List allocations by filter |
| `GET` | `/v2/docs` | Swagger UI |

### POST Endpoints

#### v2 Private (Authenticated) — `/v2/private/`
Restricted write endpoints for automated data ingestion from trusted clients (local pipeline, LAN, or self-hosted). All endpoints require the `X-API-Key` header.

**Authentication**: `X-API-Key: <secret>` header validated against `PIPELINE_API_KEY` env var. Returns `401 Unauthorized` on missing or invalid key. Auth is applied once at the `private/` package level, not per-router.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v2/private/releases` | Upsert a release (by `id`) |
| `POST` | `/v2/private/records` | Upsert a record (by `nca_number`) |
| `POST` | `/v2/private/allocations` | Upsert an allocation (by composite key `nca_number` + `agency` + `operating_unit`) |

### DELETE Endpoints

#### v2 Private (Authenticated) — `/v2/private/`

| Method | Path | Description |
|--------|------|-------------|
| `DELETE` | `/v2/private/releases/{id}` | Delete a release and cascade records/allocations |
| `DELETE` | `/v2/private/records/{nca_number}` | Delete a record and cascade allocations |
| `DELETE` | `/v2/private/allocations/{id}` | Delete an allocation |

#### Health Check

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check → `{"message": "API is running", "docs": "/docs"}` |

## v1 vs v2 Differences

| Aspect | v1 | v2 |
|--------|----|----|
| **Concurrency** | Synchronous | Fully async (`async def` + `await`) |
| **Database** | Supabase REST API (`supabase-py`) | PostgreSQL (`SQLAlchemy` + `asyncpg`) |
| **Repository interfaces** | Sync Protocols (`RecordRepository` etc.) | Async Protocols (`AsyncRecordRepository` etc.) |
| **Error handling** | Generic `ValueError` / `Exception` | Structured `NotFoundError`, `ValidationError` |
| **Cursor validation** | Pre-validates cursor existence via `get_record_by_id` | Validates empty string only; no pre-fetch |
| **Next cursor** | Inline `records[-1].id` in each use case | Shared `compute_next_cursor(items)` utility |

Business logic, entity shapes, filter keys, and pagination mechanics are identical.

## Pagination

Keyset/cursor-based pagination with composite ordering:

- **Records / Allocations**: ordered by `(released_date ASC, id ASC)`
- **Releases**: ordered by `(id ASC)`

Query parameters:
- `limit` (integer, default 20): max items per page
- `cursor` (string): ID of the last item from the previous page

Allocations inherit sorting from their parent Record's `released_date` via a JOIN.

## Filtering

List endpoints support path-based filtering:

```
GET /v1/records/{filter_key}/{filter_value}
GET /v1/allocations/{filter_key}/{filter_value}
```

### Record filters (`RecordFilter`)
| Key | Value Type |
|-----|------------|
| `department` | string |
| `nca_type` | string |
| `release_id` | string |
| `released_date` | string |

### Allocation filters (`AllocationFilter`)
| Key | Value Type |
|-----|------------|
| `agency` | string |
| `nca_number` | string |
| `operating_unit` | string |

## Rate Limiting

Global: **1000 requests per hour** via `slowapi`.

## Error Responses

### v1
- `404`: Resource not found
- `500`: Internal error / invalid filter key

### v2
- `400`: `ValidationError` (e.g., empty cursor)
- `404`: `NotFoundError`
- `500`: Internal error / invalid filter key
