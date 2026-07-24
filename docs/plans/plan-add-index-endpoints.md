# Implementation Plan: Add Root Index Endpoints

## 1. Context & Objectives
- **User Intent:** Hitting `/v1`, `/v2`, or `/` should return useful information listing available public endpoints — not 404. This is standard professional API practice (e.g., GitHub API's `/` returns endpoint listings).
- **Goal:** Add GET handlers to `/`, `/v1/`, and `/v2/` that return structured metadata about available routes, similar to how professional APIs present their endpoint directories.
- **Current Implementation:** `GET /` returns a bare `{"message": "API is running", "docs": "/docs"}`. `GET /v1/` and `GET /v2/` return 404 because neither router has a root handler. `GET /v2/private/` also 404s but is auth-protected — its root should list available private endpoints only when authenticated.
- **Target Implementation:** Each index endpoint returns a JSON response containing: API name/version, description, available endpoints (method + path + short description), a link to full docs, and the Swagger UI path.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| `GET /` returns a bare message — not informative | Expand root handler to return endpoint directory | Add fields: `title`, `versions`, `endpoints`, `docs_url` |
| `GET /v1/` returns 404 | Add a `@router.get("/")` in `v1/__init__.py` | Return v1-specific index with all public GET endpoints |
| `GET /v2/` returns 404 | Add a `@router.get("/")` in `v2/__init__.py` | Return v2-specific index with public GET + note about private endpoints |
| `GET /v2/private/` returns 404 | Add a `@router.get("/")` in `v2/routers/private/__init__.py` | Return private index listing POST/DELETE endpoints (auth-protected — returns 401 if no key) |
| No Pydantic schema for index responses | Create `IndexResponse` schema | Model with `title`, `version`, `description`, `endpoints` list, `docs_url` |

## 3. Scope & File Modifications

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `main.py:31-33` | Expand the `GET /` handler to return a full index with version listing | Root should show what versions and endpoints are available |
| `src/presentation/api/v1/__init__.py` | Add `@router.get("/")` returning v1 index listing all public endpoints | `/v1/` should not 404 |
| `src/presentation/api/v2/__init__.py` | Add `@router.get("/")` returning v2 index listing public endpoints + noting private endpoints require auth | `/v2/` should not 404 |
| `src/presentation/api/v2/routers/private/__init__.py` | Add `@router.get("/")` returning private index listing POST/DELETE endpoints | `/v2/private/` should return directory when authenticated |
| `src/presentation/api/schemas.py` | Add `EndpointInfo` and `IndexResponse` Pydantic models | Typed response schemas |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `src/presentation/api/v1/routers/public/*.py` | Route definitions unchanged |
| `src/presentation/api/v2/routers/public/*.py` | Route definitions unchanged |
| `src/presentation/api/v2/routers/private/*.py` (entity files) | Endpoint definitions unchanged |
| `docs/api-documentation.md` | Can be updated later as a follow-up; not blocking |

## 4. Execution Plan

### Phase Breakdown
- **Phase 1:** Create Pydantic schemas (`EndpointInfo`, `IndexResponse`) in `schemas.py`
- **Phase 2:** Add index handlers to v1 and v2 root routers
- **Phase 3:** Add index handler to v2 private router
- **Phase 4:** Expand root `/` handler in `main.py`

### Phase Status & Checklist

**Phase 1: Create Pydantic Schemas** — Status: ⏳ Pending
- [ ] Add `EndpointInfo` model (`method: str`, `path: str`, `description: str`)
- [ ] Add `IndexResponse` model (`title: str`, `version: str`, `description: str`, `endpoints: list[EndpointInfo]`, `docs_url: str`)
- [ ] Verify imports compile

**Phase 2: Add Index Handlers to v1 and v2** — Status: ⏳ Pending
- [ ] Add `@router.get("/")` in `v1/__init__.py` returning `IndexResponse` with all v1 GET endpoints
- [ ] Add `@router.get("/")` in `v2/__init__.py` returning `IndexResponse` with all v2 GET endpoints + note about `/v2/private/`
- [ ] Verify routes appear in `/docs`

**Phase 3: Add Index Handler to v2 Private** — Status: ⏳ Pending
- [ ] Add `@router.get("/")` in `v2/routers/private/__init__.py` returning `IndexResponse` listing all POST/DELETE endpoints
- [ ] Confirm it returns 401 when no `X-API-Key` header (inherits auth from parent router)
- [ ] Verify routes appear in `/docs`

**Phase 4: Expand Root Handler** — Status: ⏳ Pending
- [ ] Expand `GET /` in `main.py` to return a top-level index with version links, available endpoints, and docs URL
- [ ] Verify route appears in `/docs`