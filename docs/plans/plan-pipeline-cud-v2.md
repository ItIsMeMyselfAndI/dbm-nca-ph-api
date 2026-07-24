# Implementation Plan: Pipeline-Only CUD Operations (v2)

## 1. Context & Objectives
* **User Intent:** The API currently serves read-only data. A local pipeline program ingests DBM NCA data and needs to write it into the database. These write operations must be restricted exclusively to that pipeline.
* **Goal:** Add Create, Update, and Delete (CUD) endpoints under `v2` that only the authorized pipeline can call. Read endpoints remain public.
* **Current Implementation:** v2 has read-only async endpoints (`GET` only) backed by PostgreSQL via SQLAlchemy. Repositories, use cases, interfaces, and routers all follow Clean Architecture.
* **Target Implementation:** A `/api/v2/pipeline/` router with `POST`, `PUT`, `DELETE` endpoints protected by an API key. The pipeline sends the key via `X-API-Key` header. All CUD logic follows the existing Clean Architecture layers.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| No write methods in v2 async repository interfaces | Add `create`, `update`, `delete` methods to `AsyncRecordRepository`, `AsyncAllocationRepository`, `AsyncReleaseRepository` Protocols | Protocol classes in `core/interfaces/` |
| No write methods in Postgres repositories | Implement `create`, `update`, `delete` in `PostgresRecordRepository`, `PostgresAllocationRepository`, `PostgresReleaseRepository` | Repos in `infrastructure/db/` |
| No CUD use cases | Create `core/use_cases/v2/pipeline/` with upsert/delete use cases for all 3 entities | Use cases mirror existing read patterns |
| No CUD endpoints | Create `presentation/api/v2/routers/pipeline.py` with `POST`, `PUT`, `DELETE` routes | All routes protected by API key dependency |
| No authentication mechanism | Shared secret via `PIPELINE_API_KEY` env var; validated by FastAPI `Depends` | Added to `Settings` + new `auth.py` dependency |
| Pipeline currently has no way to authenticate | Pipeline sends `X-API-Key: <secret>` on every request; API rejects if mismatch | 401 Unauthorized on mismatch |

## 3. Scope & File Modifications

### New Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `src/presentation/api/auth.py` | `require_pipeline_key()` dependency that reads `X-API-Key` header and compares against `Settings.PIPELINE_API_KEY` | Centralized auth for all write endpoints |
| `src/presentation/api/v2/routers/pipeline.py` | `APIRouter(prefix="/pipeline")` with all CUD endpoints | Keeps write routes separate from public read routes |
| `src/core/use_cases/v2/pipeline/upsert_release.py` | Use case: create or update a Release | Pipeline upserts by natural key (`id`) |
| `src/core/use_cases/v2/pipeline/delete_release.py` | Use case: delete a Release + cascade to records/allocations | Cascading delete |
| `src/core/use_cases/v2/pipeline/upsert_record.py` | Use case: create or update a Record | Pipeline upserts by natural key (`nca_number`) |
| `src/core/use_cases/v2/pipeline/delete_record.py` | Use case: delete a Record + cascade to allocations | Cascading delete |
| `src/core/use_cases/v2/pipeline/upsert_allocation.py` | Use case: create or update an Allocation | Pipeline upserts by composite key |
| `src/core/use_cases/v2/pipeline/delete_allocation.py` | Use case: delete an Allocation | Direct delete by ID |

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `src/infrastructure/config.py` | Add `PIPELINE_API_KEY: str` field | Config value for shared secret |
| `src/core/interfaces/async_release_repository.py` | Add `create`, `update`, `delete` method signatures | Protocol must declare CUD operations |
| `src/core/interfaces/async_record_repository.py` | Add `create`, `update`, `delete` method signatures | Protocol must declare CUD operations |
| `src/core/interfaces/async_allocation_repository.py` | Add `create`, `update`, `delete` method signatures | Protocol must declare CUD operations |
| `src/infrastructure/db/postgres_release_repository.py` | Implement `create`, `update`, `delete` | Actual DB write logic |
| `src/infrastructure/db/postgres_record_repository.py` | Implement `create`, `update`, `delete` | Actual DB write logic |
| `src/infrastructure/db/postgres_allocation_repository.py` | Implement `create`, `update`, `delete` | Actual DB write logic |
| `src/presentation/api/v2/__init__.py` | Import and include `pipeline_router` | Register new routes |
| `src/presentation/api/schemas.py` | Add request/response schemas for CUD operations | Pipeline input/output DTOs |
| `.env.sample` | Add `PIPELINE_API_KEY=your_secret_key` | Document new env var |
| `docs/api-documentation.md` | Add pipeline endpoint documentation | Keep docs in sync |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- | :--- |
| `main.py` | v2 router is auto-included via `__init__.py`; no changes needed |
| All v1 files | Scope is v2 only; v1 remains read-only |
| Existing v2 read use cases & routers | Unchanged; public read surface stays identical |
| `src/infrastructure/db/models.py` | ORM models already support all fields needed |
| `src/core/entities/*.py` | Entities are unchanged; CUD use cases reuse them |

## 4. Execution Plan

### Phase Breakdown
* **Phase 1:** Authentication — Add `PIPELINE_API_KEY` config + `require_pipeline_key()` dependency
* **Phase 2:** Repository CUD methods — Add write method signatures to async protocols + implementations to Postgres repos
* **Phase 3:** Use cases — Create pipeline use cases for upsert & delete per entity
* **Phase 4:** Schemas — Add Pydantic request/response models for CUD
* **Phase 5:** Router — Create the protected pipeline router + register in v2
* **Phase 6:** Documentation — Update docs + `.env.sample`

### Phase Elaboration
* **Phase 1:** `PIPELINE_API_KEY` is loaded from `.env` via `Settings`. FastAPI dependency `require_pipeline_key` reads the `X-API-Key` header, raises `HTTPException(401)` on mismatch. This dependency is applied to every route in the pipeline router (not per-route, to keep it DRY).
* **Phase 2:** The async Protocols get new method stubs. For upsert semantics: `create(entity)` inserts, `update(id, entity)` patches, `delete(id)` removes. Postgres repos use SQLAlchemy async `session.merge()` for upsert and `session.delete()` for delete. Cascade deletes are handled explicitly: delete allocations before record, records before release.
* **Phase 3:** Upsert use cases accept an entity dict/PD, call `repo.create()` or `repo.update()` after checking existence. Delete use cases validate existence first, then delete with cascade awareness.
* **Phase 4:** Request schemas (`ReleaseCreate`, `RecordCreate`, `AllocationCreate`) exclude `id`/`created_at`/`updated_at` — these are generated server-side. Response schemas return the full created/updated entity.
* **Phase 5:** `pipeline.py` router has routes like `POST /releases`, `PUT /releases/{id}`, `DELETE /releases/{id}`, and corresponding routes for records/allocations. The auth dependency is applied to the entire router via `dependencies=[Depends(require_pipeline_key)]`.
* **Phase 6:** `docs/api-documentation.md` gets a new section documenting pipeline endpoints. `.env.sample` gets `PIPELINE_API_KEY`.

### Phase Status & Checklist

**Phase 1: Authentication** — Status: ⏳ Pending
- [ ] Add `PIPELINE_API_KEY: str` to `Settings` in `src/infrastructure/config.py`
- [ ] Create `src/presentation/api/auth.py` with `require_pipeline_key()` dependency
- [ ] Add `PIPELINE_API_KEY=dev-secret` to `.env` and `PIPELINE_API_KEY=your_secret_key` to `.env.sample`

**Phase 2: Repository CUD Methods** — Status: ⏳ Pending
- [ ] Add `create`, `update`, `delete` method signatures to `AsyncReleaseRepository` Protocol
- [ ] Add `create`, `update`, `delete` method signatures to `AsyncRecordRepository` Protocol
- [ ] Add `create`, `update`, `delete` method signatures to `AsyncAllocationRepository` Protocol
- [ ] Implement `create`, `update`, `delete` in `PostgresReleaseRepository`
- [ ] Implement `create`, `update`, `delete` in `PostgresRecordRepository`
- [ ] Implement `create`, `update`, `delete` in `PostgresAllocationRepository`

**Phase 3: Use Cases** — Status: ⏳ Pending
- [ ] Create `src/core/use_cases/v2/pipeline/__init__.py`
- [ ] Create `upsert_release.py` — upsert Release by `id`
- [ ] Create `delete_release.py` — delete Release + cascade
- [ ] Create `upsert_record.py` — upsert Record by `nca_number`
- [ ] Create `delete_record.py` — delete Record + cascade
- [ ] Create `upsert_allocation.py` — upsert Allocation by composite key
- [ ] Create `delete_allocation.py` — delete Allocation by `id`

**Phase 4: Schemas** — Status: ⏳ Pending
- [ ] Add `ReleaseCreate`, `RecordCreate`, `AllocationCreate` request schemas to `src/presentation/api/schemas.py`
- [ ] Add response schemas for each if different from existing

**Phase 5: Router** — Status: ⏳ Pending
- [ ] Create `src/presentation/api/v2/routers/pipeline.py` with all CUD routes
- [ ] Import and include `pipeline_router` in `src/presentation/api/v2/__init__.py`

**Phase 6: Documentation** — Status: ⏳ Pending
- [ ] Update `docs/api-documentation.md` with pipeline endpoints section
- [ ] Update `.env.sample` with `PIPELINE_API_KEY`
