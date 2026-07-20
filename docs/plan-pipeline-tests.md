# Implementation Plan: Pipeline CUD Tests

## 1. Context & Objectives
* **User Intent:** Ensure the 6 new pipeline CUD endpoints (upsert/delete for Release, Record, Allocation) are thoroughly tested before deployment to catch regressions and edge cases.
* **Goal:** Create a complete test suite mirroring the existing test structure — CUD tests live under **v2** only (since pipeline is v2-only), while **v1** gets empty pipeline folders as placeholders. Mock CUD methods belong to the v2 async mocks only.
* **Current Implementation:** Mock async repositories (`MockAsync*Repository`) under `tests/mock/repositories_async/` only implement read methods. v1 sync mocks under `tests/mock/repositories/` are read-only. No CUD or pipeline tests exist in either version.
* **Target Implementation:** 
  - CUD methods (`create_*`, `update_*`, `delete_*`) added to `tests/mock/repositories_async/` (v2 only). v1 mocks remain read-only.
  - v2 gets full test suite at use-case and router layers.
  - v1 gets empty `pipeline/` directories (just `__init__.py`) as placeholders.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| Mocks lack CUD methods | Add `create_*`, `update_*`, `delete_*` to all 3 `MockAsync*Repository` classes | Only in `tests/mock/repositories_async/` (v2). v1 `tests/mock/repositories/` left read-only |
| Pipeline router requires `X-API-Key` | Override `require_pipeline_key` dep in `tests/v2/conftest.py` to a no-op | Keep auth tests separate; router tests don't need key |
| Router tests share mutable mock state | Each test file that mutates state overrides its own fresh mock repos via `app.dependency_overrides` | Follow FastAPI pattern — avoid cross-test pollution |
| UpsertRecord uses `list_records_by_filter(NCA_NUMBER)` | Mock must support `NCA_NUMBER` filter | Already supported in the `RecordFilter` enum |
| UpsertAllocation uses composite key (agency+ou) | Mock must filter by both fields after NCA_NUMBER filter | Implement by iterating existing results |
| DeleteRelease must find records by release_id | Mock must support `RELEASE_ID` filter | Already supported in `RecordFilter` enum |
| v1 has no pipeline tests | Create empty `pipeline/` directories under `tests/v1/` | Placeholder `__init__.py` only |

## 3. Scope & File Modifications

### Modified Files (v2 mocks — CUD methods added)
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `tests/mock/repositories_async/mock_async_release_repository.py` | Add `create_release`, `update_release`, `delete_release` methods | Mock CUD for pipeline use-case tests |
| `tests/mock/repositories_async/mock_async_record_repository.py` | Add `create_record`, `update_record`, `delete_record` methods | Mock CUD for pipeline use-case tests |
| `tests/mock/repositories_async/mock_async_allocation_repository.py` | Add `create_allocation`, `update_allocation`, `delete_allocation` methods | Mock CUD for pipeline use-case tests |
| `tests/v2/conftest.py` | Add override for `require_pipeline_key` (no-op) | Allow router tests without API key |
| `tests/mock/repositories/mock_async_release_repository.py` | **Untouched** | v1 remains read-only |

### New Files — v2 Core/Use Case Tests (unit)
| File Path | What It Tests |
| :--- | :--- |
| `tests/v2/core/use_cases/pipeline/__init__.py` | Empty package init |
| `tests/v2/core/use_cases/pipeline/test_upsert_release.py` | UpsertRelease: create new, update existing, edge cases |
| `tests/v2/core/use_cases/pipeline/test_delete_release.py` | DeleteRelease: found, not found, cascade behavior |
| `tests/v2/core/use_cases/pipeline/test_upsert_record.py` | UpsertRecord: create new, update by nca_number, edge cases |
| `tests/v2/core/use_cases/pipeline/test_delete_record.py` | DeleteRecord: found, not found |
| `tests/v2/core/use_cases/pipeline/test_upsert_allocation.py` | UpsertAllocation: create new, update by composite key (agency+ou), multiple nca_allocations |
| `tests/v2/core/use_cases/pipeline/test_delete_allocation.py` | DeleteAllocation: found, not found |

### New Files — v2 Presentation/Router Tests (integration)
| File Path | What It Tests |
| :--- | :--- |
| `tests/v2/presentation/api/routers/pipeline/__init__.py` | Empty package init |
| `tests/v2/presentation/api/routers/pipeline/test_auth.py` | Missing key, invalid key, valid key, empty key |
| `tests/v2/presentation/api/routers/pipeline/test_upsert_release.py` | POST `/pipeline/releases` — 201 create, 200 update, 422 validation |
| `tests/v2/presentation/api/routers/pipeline/test_delete_release.py` | DELETE `/pipeline/releases/{id}` — 204 success, 404 not found |
| `tests/v2/presentation/api/routers/pipeline/test_upsert_record.py` | POST `/pipeline/records` — 201 create, 200 update, 422 validation |
| `tests/v2/presentation/api/routers/pipeline/test_delete_record.py` | DELETE `/pipeline/records/{nca_number}` — 204 success, 404 not found |
| `tests/v2/presentation/api/routers/pipeline/test_upsert_allocation.py` | POST `/pipeline/allocations` — 201 create, 200 update, 422 validation |
| `tests/v2/presentation/api/routers/pipeline/test_delete_allocation.py` | DELETE `/pipeline/allocations/{id}` — 204 success, 404 not found |

### New Files — v1 Placeholders (empty)
| File Path | Content |
| :--- | :--- |
| `tests/v1/core/use_cases/pipeline/__init__.py` | Empty (v1 has no pipeline CUD) |
| `tests/v1/presentation/api/routers/pipeline/__init__.py` | Empty (v1 has no pipeline CUD) |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `tests/v2/core/use_cases/{allocation,record,release}/*` | Existing read tests — unrelated |
| `tests/v2/presentation/api/routers/{allocation,record,release}/*` | Existing read tests — unrelated |
| `tests/v1/` (all existing read tests) | v1 is read-only; no pipeline changes |
| `tests/mock/repositories/` (v1 sync mocks) | Read-only — no CUD added to v1 mocks |
| `src/core/use_cases/v2/pipeline/*` | Production code — tested, not modified |
| `src/presentation/api/v2/routers/pipeline.py` | Production code — tested, not modified |
| `tests/mock/data/*.json` | Test data unchanged |

## 4. Execution Plan

### Version Architecture

```
tests/
├── mock/
│   ├── repositories/              ← v1 (sync, read-only — NO CUD methods)
│   │   ├── mock_release_repository.py
│   │   ├── mock_record_repository.py
│   │   └── mock_allocation_repository.py
│   ├── repositories_async/        ← v2 (async — has CUD methods for pipeline)
│   │   ├── mock_async_release_repository.py
│   │   ├── mock_async_record_repository.py
│   │   └── mock_async_allocation_repository.py
│   └── data/
├── v1/
│   ├── core/use_cases/
│   │   ├── allocation/            ← read tests only
│   │   ├── record/                ← read tests only
│   │   ├── release/               ← read tests only
│   │   └── pipeline/              ← EMPTY (v1 has no pipeline)
│   ├── presentation/api/routers/
│   │   ├── allocation/            ← read tests only
│   │   ├── record/                ← read tests only
│   │   ├── release/               ← read tests only
│   │   └── pipeline/              ← EMPTY (v1 has no pipeline)
│   └── ...
└── v2/
    ├── core/use_cases/
    │   ├── allocation/            ← read tests only
    │   ├── record/                ← read tests only
    │   ├── release/               ← read tests only
    │   └── pipeline/              ← CUD tests (6 files)
    ├── presentation/api/routers/
    │   ├── allocation/            ← read tests only
    │   ├── record/                ← read tests only
    │   ├── release/               ← read tests only
    │   └── pipeline/              ← CUD + auth tests (7 files)
    └── ...
```

### Phase Breakdown
* **Phase 1:** Add CUD methods to v2 mock async repos + conftest auth bypass + create v1 empty pipeline dirs
* **Phase 2:** Create v2 core/use-case pipeline tests (6 test files)
* **Phase 3:** Create v2 presentation/router pipeline tests (8 test files: 1 auth + 6 endpoint + 1 __init__)
* **Phase 4:** Run full test suite and fix any failures

### Phase Elaboration
* **Phase 1:** Each v2 mock repo gets mutable `create_*`, `update_*`, `delete_*` methods. v1 mocks stay read-only. The v2 conftest gets an override for `require_pipeline_key`. Two empty v1 pipeline folders are created as placeholders.
* **Phase 2:** 6 use-case test files following the exact pattern of existing read-side tests: `@pytest.mark.asyncio`, per-file `repo`/`use_case` fixtures, `pytest.raises(NotFoundError)`.
* **Phase 3:** 7 router test files + 1 `__init__.py` following the exact pattern of existing read-side router tests: `client` fixture injection, HTTP status assertions, JSON body assertions.
* **Phase 4:** Run `pytest tests/v2/ -v` and fix any failing tests. Verify no existing tests break.

### Phase Status & Checklist

**Phase 1: Mock CUD + Conftest + v1 Placeholders** — Status: ✅ Done
- [x] Add `create_release`, `update_release`, `delete_release` to `MockAsyncReleaseRepository` (v2 only)
- [x] Add `create_record`, `update_record`, `delete_record` to `MockAsyncRecordRepository` (v2 only)
- [x] Add `create_allocation`, `update_allocation`, `delete_allocation` to `MockAsyncAllocationRepository` (v2 only)
- [x] Add `require_pipeline_key` override to `tests/v2/conftest.py`
- [x] Create `tests/v1/core/use_cases/pipeline/__init__.py` (empty)
- [x] Create `tests/v1/presentation/api/routers/pipeline/__init__.py` (empty)

**Phase 2: v2 Core/Use Case Pipeline Tests** — Status: ✅ Done
- [x] Create `tests/v2/core/use_cases/pipeline/__init__.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_upsert_release.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_delete_release.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_upsert_record.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_delete_record.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_upsert_allocation.py`
- [x] Create `tests/v2/core/use_cases/pipeline/test_delete_allocation.py`

**Phase 3: v2 Presentation/Router Pipeline Tests** — Status: ✅ Done
- [x] Create `tests/v2/presentation/api/routers/pipeline/__init__.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_auth.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_release.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_delete_release.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_record.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_delete_record.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_allocation.py`
- [x] Create `tests/v2/presentation/api/routers/pipeline/test_delete_allocation.py`

**Phase 4: Verification** — Status: ✅ Done
- [x] Run `pytest tests/v2/ -v` — 180 passed
- [x] Fix all failures (12 issues fixed: auth header, status codes, mock update id, missing awaits)
- [x] Update `test_record_filter` for new `NCA_NUMBER` enum member
- [x] Confirm v1 tests unchanged (28 pre-existing failures unrelated)```


### Core Use Case Tests

**UpsertRelease**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_release_create` | Execute with new release id (not in mock data) | Returns created Release; repo size+1 |
| `test_upsert_release_update` | Execute with existing release id (e.g., `id_2024`) | Returns updated Release with new values; repo size unchanged |
| `test_upsert_release_update_all_fields` | Update all fields of existing release | All fields match new values |
| `test_upsert_release_id_normalization` | Upsert with whitespace/case variant of existing id | Finds existing and updates (match mock's strip+lower) |

**DeleteRelease**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_release` | Delete existing release (`id_2024`) | Release removed; records with release_id deleted |
| `test_delete_release_not_found` | Delete nonexistent id | `NotFoundError` raised |
| `test_delete_release_no_associated_records` | Delete release with no records | Release removed successfully |
| `test_delete_release_id_normalization` | Delete with whitespace/case variant | Works if mock normalizes; otherwise fails as expected |

**UpsertRecord**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_record_create` | Execute with new nca_number | Creates record; repo size+1 |
| `test_upsert_record_update` | Execute with existing nca_number | Updates record; repo size unchanged |
| `test_upsert_record_update_all_fields` | Update all fields of existing record | All fields match new values |
| `test_upsert_record_multiple_nca_calls` | Upsert with same nca_number twice | First creates, second updates |

**DeleteRecord**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_record` | Delete existing record by nca_number | Record removed |
| `test_delete_record_not_found` | Delete nonexistent nca_number | `NotFoundError` raised |
| `test_delete_record_with_allocations` | (Caveat) Delete record that has child allocations | Record deleted (note: bug — allocations not deleted by this use case) |

**UpsertAllocation**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_allocation_create` | Execute with new (nca_number, agency, ou) combo | Creates allocation; repo size+1 |
| `test_upsert_allocation_update` | Execute with existing (nca_number, agency, ou) combo | Updates allocation; repo size unchanged |
| `test_upsert_allocation_same_nca_diff_agency` | Same nca_number, different agency+ou | Creates new (distinct composite key) |
| `test_upsert_allocation_same_nca_diff_ou` | Same nca_number+agency, different ou | Creates new (distinct composite key) |

**DeleteAllocation**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_allocation` | Delete existing allocation by id | Allocation removed |
| `test_delete_allocation_not_found` | Delete nonexistent id | `NotFoundError` raised |

### Router Tests

**Auth (`test_auth.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_pipeline_missing_api_key` | POST without `X-API-Key` header | 401 |
| `test_pipeline_invalid_api_key` | POST with wrong `X-API-Key` header | 401 |
| `test_pipeline_empty_api_key` | POST with empty `X-API-Key` header | 401 |
| `test_pipeline_valid_auth` | POST with valid key | Either 201/200/422 (not 401) |

**Upsert Release (`test_upsert_release.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_release_201` | POST with new release id | 201 + release body with all fields |
| `test_upsert_release_200` | POST with existing release id | 200 + updated release body |
| `test_upsert_release_422_empty_body` | POST with empty JSON | 422 |
| `test_upsert_release_422_missing_fields` | POST missing required fields | 422 |

**Delete Release (`test_delete_release.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_release_204` | DELETE existing release | 204 no content |
| `test_delete_release_404` | DELETE nonexistent release | 404 |
| `test_delete_release_with_records` | DELETE release that has associated records | 204 (cascade delete records) |

**Upsert Record (`test_upsert_record.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_record_201` | POST with new nca_number | 201 + record body |
| `test_upsert_record_200` | POST with existing nca_number | 200 + updated record |
| `test_upsert_record_422_missing_fields` | POST missing required fields | 422 |

**Delete Record (`test_delete_record.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_record_204` | DELETE existing nca_number | 204 |
| `test_delete_record_404` | DELETE nonexistent nca_number | 404 |

**Upsert Allocation (`test_upsert_allocation.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_upsert_allocation_201` | POST with new composite key | 201 + allocation body |
| `test_upsert_allocation_200` | POST with existing composite key | 200 + updated allocation |
| `test_upsert_allocation_422_missing_fields` | POST missing required fields | 422 |

**Delete Allocation (`test_delete_allocation.py`)**
| Test | Scenario | Expected |
| :--- | :--- | :--- |
| `test_delete_allocation_204` | DELETE existing allocation id | 204 |
| `test_delete_allocation_404` | DELETE nonexistent allocation id | 404 |
