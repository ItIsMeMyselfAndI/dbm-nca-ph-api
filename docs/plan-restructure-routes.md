# Implementation Plan: Restructure v2 Routes (public/ + private/)

## 1. Context & Objectives
* **User Intent:** Replace the cross-cutting `pipeline.py` router with a clean entity-per-file structure, separating public read endpoints from authenticated write endpoints.
* **Goal:** Restructure `v2/routers/` so that access level (public vs authenticated) is reflected in the directory hierarchy, and each entity has its own file.
* **Current Implementation:** A single `v2/routers/pipeline.py` groups all write operations across three entities. Read endpoints are in separate entity files (`releases.py`, `records.py`, `allocations.py`).
* **Target Implementation:** Two subdirectories — `public/` (read-only, no auth) and `private/` (write-only, `require_pipeline_key` applied at the package level). Each entity has its own file in both directories.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| `pipeline.py` is a process, not an entity — breaks entity-per-file pattern | Split into per-entity files under `private/` | `private/releases.py`, `private/records.py`, `private/allocations.py` |
| Auth dependency is applied at the router level in one place | Apply `require_pipeline_key` globally in `private/__init__.py` | All routes under `private/` inherit auth; entity files are auth-unaware |
| Read and write routes are in different organizational schemes | Move read routes into `public/` subdirectory | `public/releases.py`, `public/records.py`, `public/allocations.py` |
| URL path `/v2/pipeline/` reflects a process name, not access level | Rename to `/v2/private/` | More descriptive of access restriction; works for any client (local, LAN, self-hosted) |

## 3. Scope & File Modifications

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `src/presentation/api/v2/__init__.py` | Replace direct imports from `v2.routers.*` with imports from `v2.routers.public.*` and `v2.routers.private` | Wire up new directory structure |
| `docs/api-documentation.md` | Rename "Pipeline" section to "v2 Private", update paths from `/v2/pipeline/` to `/v2/private/` | Keep docs in sync |

### Created Files
| File Path | Contents | Reason |
| :--- | :--- | :--- |
| `src/presentation/api/v2/routers/public/__init__.py` | Empty (or `from .releases import router`, `from .records import router`, etc.) | Make `public` a package |
| `src/presentation/api/v2/routers/public/releases.py` | Copied from `v2/routers/releases.py` | Entity read routes under public/ |
| `src/presentation/api/v2/routers/public/records.py` | Copied from `v2/routers/records.py` | Entity read routes under public/ |
| `src/presentation/api/v2/routers/public/allocations.py` | Copied from `v2/routers/allocations.py` | Entity read routes under public/ |
| `src/presentation/api/v2/routers/private/__init__.py` | `APIRouter(prefix="/private", dependencies=[Depends(require_pipeline_key)])` + include entity routers | Apply auth at package level, mount under `/private` |
| `src/presentation/api/v2/routers/private/releases.py` | Extracted from `pipeline.py` — POST/DELETE `/releases` | Entity write routes under private/ |
| `src/presentation/api/v2/routers/private/records.py` | Extracted from `pipeline.py` — POST/DELETE `/records` | Entity write routes under private/ |
| `src/presentation/api/v2/routers/private/allocations.py` | Extracted from `pipeline.py` — POST/DELETE `/allocations` | Entity write routes under private/ |

### Deleted Files
| File Path | Reason |
| :--- | :--- |
| `src/presentation/api/v2/routers/pipeline.py` | Content split into `private/releases.py`, `private/records.py`, `private/allocations.py` |
| `src/presentation/api/v2/routers/releases.py` | Moved to `public/releases.py` |
| `src/presentation/api/v2/routers/records.py` | Moved to `public/records.py` |
| `src/presentation/api/v2/routers/allocations.py` | Moved to `public/allocations.py` |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `src/presentation/api/auth.py` | `require_pipeline_key` stays as-is; just its import location changes |
| `src/presentation/api/schemas.py` | Schemas are unchanged |
| `src/core/use_cases/v2/pipeline/*` | Use cases are unchanged; only the presentation layer (routers) is restructured |
| `src/presentation/api/v1/*` | v1 is unchanged |
| `src/infrastructure/config.py` | `PIPELINE_API_KEY` config key unchanged |
| `src/presentation/api/dependencies_v2.py` | DI functions unchanged |

## 4. Execution Plan

### Phase Breakdown
* **Phase 1:** Create `public/` directory, move existing read route files
* **Phase 2:** Create `private/` directory, extract write routes from `pipeline.py` into per-entity files
* **Phase 3:** Update `v2/__init__.py` to wire up new structure
* **Phase 4:** Update docs and clean up old files

### Phase Status & Checklist

**Phase 1: Create `public/` directory & move read routes** - Status: ⏳ Pending
- [ ] Create `src/presentation/api/v2/routers/public/__init__.py` (empty)
- [ ] Create `src/presentation/api/v2/routers/public/releases.py` (copy from `v2/routers/releases.py`)
- [ ] Create `src/presentation/api/v2/routers/public/records.py` (copy from `v2/routers/records.py`)
- [ ] Create `src/presentation/api/v2/routers/public/allocations.py` (copy from `v2/routers/allocations.py`)

**Phase 2: Create `private/` directory & extract write routes** - Status: ⏳ Pending
- [ ] Create `src/presentation/api/v2/routers/private/__init__.py` (auth-scoped parent router)
- [ ] Create `src/presentation/api/v2/routers/private/releases.py` (POST/DELETE from `pipeline.py`)
- [ ] Create `src/presentation/api/v2/routers/private/records.py` (POST/DELETE from `pipeline.py`)
- [ ] Create `src/presentation/api/v2/routers/private/allocations.py` (POST/DELETE from `pipeline.py`)

**Phase 3: Wire up `v2/__init__.py`** - Status: ⏳ Pending
- [ ] Update `src/presentation/api/v2/__init__.py` to import from `public.*` and `private`

**Phase 4: Clean up & docs** - Status: ⏳ Pending
- [ ] Delete `v2/routers/pipeline.py`, `v2/routers/releases.py`, `v2/routers/records.py`, `v2/routers/allocations.py`
- [ ] Update `docs/api-documentation.md` — rename section, update paths
- [ ] Run recompile/type check to verify
