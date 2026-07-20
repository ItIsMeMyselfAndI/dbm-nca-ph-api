# Implementation Plan: Restructure & Expand Tests for Route Hierarchy

## 1. Context & Objectives
* **User Intent:** Tests should mirror the new `public/` + `private/` route structure, with full coverage of the private write endpoints (upsert/delete) and their edge cases.
* **Goal:** Refactor existing router test directories to match `public/private` hierarchy; add comprehensive test suites for all 6 private endpoints.
* **Current Implementation:** Router tests live flat under `tests/v1|v2/presentation/api/routers/{entity}/` — no `public/` or `private/` subdirectories. No tests exist for the private write endpoints (CUD).
* **Target Implementation:**
  - `tests/v1/presentation/api/routers/public/{entity}/` — existing read tests (moved)
  - `tests/v2/presentation/api/routers/public/{entity}/` — existing async read tests (moved)
  - `tests/v2/presentation/api/routers/private/{entity}/` — new write tests
  - Async mock repositories gain CUD methods to support private endpoint tests

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| Router test dirs don't reflect `public/private` split | Move existing test dirs into `public/` subdirectory | `tests/v1|v2/presentation/api/routers/{entity}/` → `.../public/{entity}/` |
| Async mock repos lack create/update/delete methods | Add CUD methods to all 3 async mock repos | `create_release`, `update_release`, `delete_release`, etc. |
| No tests for private write endpoints | Create test files under `private/{entity}/` per entity | One test file per operation (upsert, delete) + auth tests |
| Private endpoints require API key auth | Add `require_pipeline_key` override and auth header | Inject `PIPELINE_API_KEY` into settings, add header to requests |
| No tests for auth failure (missing/invalid key) | Add auth-specific test file | `test_auth.py` in `private/` root or in each entity dir |

## 3. Scope & File Modifications

### Modified Files (mock repos — add CUD methods)
| File Path | Changes | Reason |
| :--- | :--- | :--- |
| `tests/mock/repositories_async/mock_async_release_repository.py` | Add `create_release`, `update_release`, `delete_release`, `get_release_by_id` (already has `get_release_by_id`) | Required by UpsertRelease/DeleteRelease use cases |
| `tests/mock/repositories_async/mock_async_record_repository.py` | Add `create_record`, `update_record`, `delete_record` | Required by UpsertRecord/DeleteRecord use cases |
| `tests/mock/repositories_async/mock_async_allocation_repository.py` | Add `create_allocation`, `update_allocation`, `delete_allocation` | Required by UpsertAllocation/DeleteAllocation use cases |

### Modified Files (conftest — add auth override)
| File Path | Changes | Reason |
| :--- | :--- | :--- |
| `tests/v2/conftest.py` | Override `require_pipeline_key` dependency to accept a known test key | Private routes use `Depends(require_pipeline_key)`; tests need to bypass or satisfy it |

### Modified Files (moved — read router tests into public/)
| File Path (old) | File Path (new) |
| :--- | :--- |
| `tests/v1/presentation/api/routers/release/` | `tests/v1/presentation/api/routers/public/release/` |
| `tests/v1/presentation/api/routers/record/` | `tests/v1/presentation/api/routers/public/record/` |
| `tests/v1/presentation/api/routers/allocation/` | `tests/v1/presentation/api/routers/public/allocation/` |
| `tests/v2/presentation/api/routers/release/` | `tests/v2/presentation/api/routers/public/release/` |
| `tests/v2/presentation/api/routers/record/` | `tests/v2/presentation/api/routers/public/record/` |
| `tests/v2/presentation/api/routers/allocation/` | `tests/v2/presentation/api/routers/public/allocation/` |

### Created Files (private endpoint tests)
| File Path | Contents |
| :--- | :--- |
| `tests/v2/presentation/api/routers/private/__init__.py` | Empty |
| `tests/v2/presentation/api/routers/private/release/test_upsert_release.py` | POST /private/releases (create + update + invalid body) |
| `tests/v2/presentation/api/routers/private/release/test_delete_release.py` | DELETE /private/releases/{id} (existing + not found) |
| `tests/v2/presentation/api/routers/private/record/test_upsert_record.py` | POST /private/records (create + update + invalid body) |
| `tests/v2/presentation/api/routers/private/record/test_delete_record.py` | DELETE /private/records/{nca_number} (existing + not found) |
| `tests/v2/presentation/api/routers/private/allocation/test_upsert_allocation.py` | POST /private/allocations (create + update + invalid body) |
| `tests/v2/presentation/api/routers/private/allocation/test_delete_allocation.py` | DELETE /private/allocations/{id} (existing + not found) |
| `tests/v2/presentation/api/routers/private/test_auth.py` | Missing key → 401, invalid key → 401 |

### Deleted Files (after migration)
| File Path | Reason |
| :--- | :--- |
| `tests/v1/presentation/api/routers/release/` (dir + contents) | Moved to `public/release/` |
| `tests/v1/presentation/api/routers/record/` (dir + contents) | Moved to `public/record/` |
| `tests/v1/presentation/api/routers/allocation/` (dir + contents) | Moved to `public/allocation/` |
| `tests/v2/presentation/api/routers/release/` (dir + contents) | Moved to `public/release/` |
| `tests/v2/presentation/api/routers/record/` (dir + contents) | Moved to `public/record/` |
| `tests/v2/presentation/api/routers/allocation/` (dir + contents) | Moved to `public/allocation/` |

### Excluded Files (analyzed but untouched)
| File Path | Reason |
| :--- | :--- |
| `tests/v2/core/use_cases/pipeline/` | Pipeline use case tests should be in core/, but they were deleted. Adding them is out of scope for this route-testing task. |
| `tests/v2/infrastructure/db/` | Already empty; no repo impl tests exist for v2 |
| `tests/mock/data/*.json` | Existing test data is sufficient for read tests; write tests create/modify in-memory data only |
| `tests/mock/repositories/*` (sync repos) | v1 has no private endpoints; sync repos unchanged |
| `tests/v1/conftest.py` | v1 has no private endpoints; no changes needed |
| `src/` (any file) | Only test infrastructure changes; no production code changes |

## 4. Execution Plan

### Phase Breakdown
* **Phase 1:** Add CUD methods to async mock repositories
* **Phase 2:** Update v2 conftest for auth override
* **Phase 3:** Move existing read router tests into `public/` (both v1 and v2)
* **Phase 4:** Create private endpoint tests (6 entity files + auth)
* **Phase 5:** Run tests and fix any issues

### Phase Status & Checklist

**Phase 1: Add CUD methods to async mock repos** — Status: ⏳ Pending
- [ ] `mock_async_release_repository.py`: add `create_release`, `update_release`, `delete_release`
- [ ] `mock_async_record_repository.py`: add `create_record`, `update_record`, `delete_record`
- [ ] `mock_async_allocation_repository.py`: add `create_allocation`, `update_allocation`, `delete_allocation`

**Phase 2: Update v2 conftest for auth** — Status: ⏳ Pending
- [ ] Override `require_pipeline_key` in `tests/v2/conftest.py` to accept a known test key (or simply no-op it)
- [ ] Set `PIPELINE_API_KEY` environment variable in test session

**Phase 3: Move read tests into `public/`** — Status: ⏳ Pending
- [ ] Create `tests/v1/presentation/api/routers/public/__init__.py`
- [ ] Move `tests/v1/presentation/api/routers/release/` → `tests/v1/presentation/api/routers/public/release/`
- [ ] Move `tests/v1/presentation/api/routers/record/` → `tests/v1/presentation/api/routers/public/record/`
- [ ] Move `tests/v1/presentation/api/routers/allocation/` → `tests/v1/presentation/api/routers/public/allocation/`
- [ ] Create `tests/v2/presentation/api/routers/public/__init__.py`
- [ ] Move `tests/v2/presentation/api/routers/release/` → `tests/v2/presentation/api/routers/public/release/`
- [ ] Move `tests/v2/presentation/api/routers/record/` → `tests/v2/presentation/api/routers/public/record/`
- [ ] Move `tests/v2/presentation/api/routers/allocation/` → `tests/v2/presentation/api/routers/public/allocation/`
- [ ] Delete old flat directories

**Phase 4: Create private endpoint tests** — Status: ⏳ Pending
- [ ] Create `tests/v2/presentation/api/routers/private/__init__.py`
- [ ] Create `tests/v2/presentation/api/routers/private/test_auth.py` (missing key, invalid key)
- [ ] Create `tests/v2/presentation/api/routers/private/release/__init__.py`
- [ ] Create `tests/v2/presentation/api/routers/private/release/test_upsert_release.py`
- [ ] Create `tests/v2/presentation/api/routers/private/release/test_delete_release.py`
- [ ] Create `tests/v2/presentation/api/routers/private/record/__init__.py`
- [ ] Create `tests/v2/presentation/api/routers/private/record/test_upsert_record.py`
- [ ] Create `tests/v2/presentation/api/routers/private/record/test_delete_record.py`
- [ ] Create `tests/v2/presentation/api/routers/private/allocation/__init__.py`
- [ ] Create `tests/v2/presentation/api/routers/private/allocation/test_upsert_allocation.py`
- [ ] Create `tests/v2/presentation/api/routers/private/allocation/test_delete_allocation.py`

**Phase 5: Run & verify** — Status: ⏳ Pending
- [ ] Run `pytest tests/` and fix any failures
- [ ] Verify all tests pass

## 5. Edge Case Matrix for Private Endpoints

### POST /private/releases (upsert)
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_release_creates_new` | POST with unique `id` | `201 Created`, returns new release |
| `test_upsert_release_updates_existing` | POST with existing `id` | `201 Created`, returns updated fields |
| `test_upsert_release_missing_required_field` | POST without `id` | `422 Unprocessable Entity` (Pydantic validation) |
| `test_upsert_release_invalid_type` | POST with `year` as string | `422 Unprocessable Entity` |
| `test_upsert_release_empty_body` | POST with empty JSON | `422 Unprocessable Entity` |

### DELETE /private/releases/{id}
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_release_existing` | DELETE existing release by id | `204 No Content` |
| `test_delete_release_non_existent` | DELETE non-existent id | `404 Not Found` |
| `test_delete_release_cascades_records` | DELETE release with child records | `204 No Content`, records removed |

### POST /private/records (upsert)
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_record_creates_new` | POST with unique `nca_number` | `201 Created`, returns new record |
| `test_upsert_record_updates_existing` | POST with existing `nca_number` | `201 Created`, returns updated fields |
| `test_upsert_record_missing_required_field` | POST without `nca_number` | `422 Unprocessable Entity` |
| `test_upsert_record_invalid_type` | POST with `amount` as string on nested? | `422 Unprocessable Entity` |
| `test_upsert_record_empty_body` | POST with empty JSON | `422 Unprocessable Entity` |

### DELETE /private/records/{nca_number}
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_record_existing` | DELETE existing record by nca_number | `204 No Content` |
| `test_delete_record_non_existent` | DELETE non-existent nca_number | `404 Not Found` |

### POST /private/allocations (upsert)
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_allocation_creates_new` | POST with unique composite key | `201 Created`, returns new allocation |
| `test_upsert_allocation_updates_existing` | POST with matching `nca_number`+`agency`+`operating_unit` | `201 Created`, returns updated fields |
| `test_upsert_allocation_missing_required_field` | POST without `nca_number` | `422 Unprocessable Entity` |
| `test_upsert_allocation_empty_body` | POST with empty JSON | `422 Unprocessable Entity` |

### DELETE /private/allocations/{id}
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_allocation_existing` | DELETE existing allocation by id | `204 No Content` |
| `test_delete_allocation_non_existent` | DELETE non-existent id | `404 Not Found` |

### Auth (applies to all private endpoints)
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_private_endpoint_missing_api_key` | POST/DELETE without `X-API-Key` | `401 Unauthorized` |
| `test_private_endpoint_invalid_api_key` | POST/DELETE with wrong `X-API-Key` | `401 Unauthorized` |

## 6. Mock Repo CUD Implementation Detail

Each CUD method on the async mock repos modifies the in-memory list (`self.releases`, `self.records`, `self.allocations`):

- **`create_*(entity)`**: Appends to list. Returns the entity. If entity with same key exists, raises or returns `None` (choose: let use case handle dedup; mock should be simple).
- **`update_*(id, entity)`**: Finds by id, replaces in list. Returns updated entity, or `None` if not found.
- **`delete_*(id)`**: Removes from list by id. Returns `True` if found, `False` if not.

No persistence across test invocations — each test gets a fresh mock repo instance via `conftest.py` fixture.

**Important**: The mock repos already use `id.strip().lower()` matching for reads. CUD methods must use the same normalization for consistency.

### Method Signatures to Add

```
async def create_release(self, release: Release) -> Release
async def update_release(self, id: str, release: Release) -> Release | None
async def delete_release(self, id: str) -> bool

async def create_record(self, record: Record) -> Record
async def update_record(self, id: str, record: Record) -> Record | None
async def delete_record(self, id: str) -> bool

async def create_allocation(self, allocation: Allocation) -> Allocation
async def update_allocation(self, id: str, allocation: Allocation) -> Allocation | None
async def delete_allocation(self, id: str) -> bool
```

## 7. Auth Override Strategy

The private router applies `Depends(require_pipeline_key)` globally. The dependency reads `settings.PIPELINE_API_KEY` from config. For tests, two options:

**Option A: Override the dependency** — Replace `require_pipeline_key` in `app.dependency_overrides` with a no-op or mock that accepts a known test key.

**Option B: Set environment variable** — Set `PIPELINE_API_KEY` in `pytest` session or conftest. The test client then sends a matching `X-API-Key` header.

**Recommendation**: Option B is simpler and tests the real auth path. Set `PIPELINE_API_KEY=test-api-key-123` in the v2 conftest (e.g., via `monkeypatch` or `os.environ`). Positive tests send this key; negative tests omit or send a wrong key.
