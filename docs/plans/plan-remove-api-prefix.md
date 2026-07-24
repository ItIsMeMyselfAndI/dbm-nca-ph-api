# Implementation Plan: Remove `/api` Prefix from Routes

## 1. Context & Objectives
- **User Intent:** Routes currently require the `/api/` segment (e.g., `/api/v1/releases`). The user wants URLs to be shorter and cleaner, starting directly with the version: `/<version>/<route>`.
- **Goal:** Remove the `/api` prefix from all API routes so they are accessible at `/<version>/<route>` instead of `/api/<version>/<route>`.
- **Current Implementation:** `main.py` mounts both v1 and v2 routers with `prefix="/api"`. The routers themselves already define version/access prefixes internally (`/v1`, `/v2`, `/private`). The resulting URL hierarchy is:
  - `/api/v1/releases`
  - `/api/v2/releases`
  - `/api/v2/private/releases`
- **Target Implementation:** Routes served at:
  - `/v1/releases`
  - `/v2/releases`
  - `/v2/private/releases`

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| Routes are namespaced under `/api/` which adds unnecessary nesting | Remove the `prefix="/api"` argument from `app.include_router()` calls | Change `app.include_router(v1.router, prefix="/api")` to `app.include_router(v1.router)` (and same for v2) |

## 3. Scope & File Modifications

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `main.py:13-14` | Remove `prefix="/api"` from both `app.include_router(...)` calls | This is the sole location where the `/api` prefix is applied |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `src/presentation/api/v1/__init__.py` | `prefix="/v1"` stays — version prefix is correct as-is |
| `src/presentation/api/v2/__init__.py` | `prefix="/v2"` stays — version prefix is correct as-is |
| `src/presentation/api/v2/routers/private/__init__.py` | `prefix="/private"` stays — access-level prefix is correct as-is |
| `vercel.json` | Catch-all route `/(.*)` → `src/main.py` still works; no config change needed |
| `docs/api-documentation.md` | Should be updated but does not affect functionality — covered by separate docs task |
| `src/presentation/api/v1/routers/public/*.py` | Route definitions unchanged |
| `src/presentation/api/v2/routers/public/*.py` | Route definitions unchanged |
| `src/presentation/api/v2/routers/private/*.py` | Route definitions unchanged |

## 4. Execution Plan

### Phase Breakdown
- **Phase 1:** Update `main.py` — remove `prefix="/api"` from both `include_router` calls

### Phase Status & Checklist

**Phase 1: Update `main.py`** — Status: ⏳ Pending
- [ ] Edit `main.py` line 13: `app.include_router(v1.router, prefix="/api")` → `app.include_router(v1.router)`
- [ ] Edit `main.py` line 14: `app.include_router(v2.router, prefix="/api")` → `app.include_router(v2.router)`
- [ ] Run the application and verify routes via `/docs` (Swagger UI) or a test request to `/v1/releases`