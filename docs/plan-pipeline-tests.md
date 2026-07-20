# Implementation Plan: Pipeline CUD Tests

## 1. Context & Objectives
* **User Intent:** Ensure the 6 new pipeline CUD endpoints (upsert/delete for Release, Record, Allocation) are thoroughly tested before deployment to catch regressions and edge cases.
* **Goal:** Create a complete test suite mirroring the existing v2 read-side test structure, covering both the **core/use-case layer** (unit) and **presentation/router layer** (integration via `TestClient`), plus the required **mock repository CUD methods**.
* **Current Implementation:** Mock async repositories (`MockAsync*Repository`) only implement read methods (get_by_id, list, list_by_filter). No CUD tests exist. No pipelines tests exist.
* **Target Implementation:** CUD methods are added to all 3 mock async repositories. A full test suite exists at both the use-case and router layer, covering all success paths, failure paths, and edge cases documented below.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| Mocks lack CUD methods | Add `create_*`, `update_*`, `delete_*` to all 3 `MockAsync*Repository` classes | Each method mutates the in-memory list to simulate a real DB |
| Pipeline router requires `X-API-Key` | Override `require_pipeline_key` dep in `tests/v2/conftest.py` to a no-op | Keep auth tests separate; router tests don't need key |
| Router tests share mutable mock state | Each test file that mutates state overrides its own fresh mock repos via `app.dependency_overrides` | Follow FastAPI pattern — avoid cross-test pollution |
| UpsertRecord uses `list_records_by_filter(NCA_NUMBER)` | Mock must support `NCA_NUMBER` filter | Already supported in the `RecordFilter` enum |
| UpsertAllocation uses composite key (agency+ou) | Mock must filter by both fields after NCA_NUMBER filter | Implement by iterating existing results |
| DeleteRelease must find records by release_id | Mock must support `RELEASE_ID` filter | Already supported in `RecordFilter` enum |
| No existing pipeline use-case or router test dirs | Create new `pipeline/` subdirectories in both `core/use_cases/` and `presentation/api/routers/` | Follow existing naming conventions |

## 3. Scope & File Modifications

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `tests/mock/repositories_async/mock_async_release_repository.py` | Add `create_release`, `update_release`, `delete_release` methods | Mock CUD for pipeline use-case tests |
| `tests/mock/repositories_async/mock_async_record_repository.py` | Add `create_record`, `update_record`, `delete_record` methods | Mock CUD for pipeline use-case tests |
| `tests/mock/repositories_async/mock_async_allocation_repository.py` | Add `create_allocation`, `update_allocation`, `delete_allocation` methods | Mock CUD for pipeline use-case tests |
| `tests/v2/conftest.py` | Add override for `require_pipeline_key` (no-op) | Allow router tests without API key |

### New Files — Core/Use Case Tests (unit)
| File Path | What It Tests |
| :--- | :--- |
| `tests/v2/core/use_cases/pipeline/__init__.py` | Empty package init |
| `tests/v2/core/use_cases/pipeline/test_upsert_release.py` | UpsertRelease: create new, update existing, edge cases |
| `tests/v2/core/use_cases/pipeline/test_delete_release.py` | DeleteRelease: found, not found, cascade behavior |
| `tests/v2/core/use_cases/pipeline/test_upsert_record.py` | UpsertRecord: create new, update by nca_number, edge cases |
| `tests/v2/core/use_cases/pipeline/test_delete_record.py` | DeleteRecord: found, not found |
| `tests/v2/core/use_cases/pipeline/test_upsert_allocation.py` | UpsertAllocation: create new, update by composite key (agency+ou), multiple nca_allocations |
| `tests/v2/core/use_cases/pipeline/test_delete_allocation.py` | DeleteAllocation: found, not found |

### New Files — Presentation/Router Tests (integration)
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

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `tests/v2/core/use_cases/*` (existing read tests) | Unrelated to pipeline — read tests not modified |
| `tests/v2/presentation/api/routers/{release,record,allocation}/*` | Unrelated to pipeline — read tests not modified |
| `src/core/use_cases/v2/pipeline/*` | Production code — tested, not modified |
| `src/presentation/api/v2/routers/pipeline.py` | Production code — tested, not modified |
| `tests/mock/data/*.json` | Test data unchanged — CUD tests operate on existing data or add new records in-memory |

## 4. Execution Plan

### Phase Breakdown
* **Phase 1:** Add CUD methods to all 3 mock async repositories + conftest auth bypass
* **Phase 2:** Create core/use-case pipeline tests (6 test files)
* **Phase 3:** Create presentation/router pipeline tests (8 test files: 1 auth + 6 endpoint + 1 __init__)
* **Phase 4:** Run full test suite and fix any failures

### Phase Elaboration
* **Phase 1:** Each mock repo gets mutable `create_*`, `update_*`, `delete_*` methods that modify `self.releases`/`self.records`/`self.allocations` in-memory lists. The conftest gets an override for `require_pipeline_key` turning it into a no-op.
* **Phase 2:** 6 use-case test files following the exact pattern of existing read-side tests: `@pytest.mark.asyncio`, per-file `repo`/`use_case` fixtures, `pytest.raises(NotFoundError)`. Edge cases include: create vs update discrimination, not-found deletes, normalization of IDs, composite key matching for allocations.
* **Phase 3:** 7 router test files + 1 `__init__.py` following the exact pattern of existing read-side router tests: `client` fixture injection, HTTP status assertions, JSON body assertions. Auth test covers missing header, wrong key, empty key (401). Pipeline tests use `client` fixture (with auth bypassed) and fresh mock repos injected per test file to avoid state pollution. Each test file overrides its own dependencies.
* **Phase 4:** Run `pytest tests/v2/ -v` and fix any failing tests. Verify no existing tests break.

### Phase Status & Checklist

**Phase 1: Mock CUD Methods + Conftest Auth** — Status: ⏳ Pending
- [ ] Add `create_release`, `update_release`, `delete_release` to `MockAsyncReleaseRepository`
- [ ] Add `create_record`, `update_record`, `delete_record` to `MockAsyncRecordRepository`
- [ ] Add `create_allocation`, `update_allocation`, `delete_allocation` to `MockAsyncAllocationRepository`
- [ ] Add `require_pipeline_key` override to `tests/v2/conftest.py`

**Phase 2: Core/Use Case Pipeline Tests** — Status: ⏳ Pending
- [ ] Create `tests/v2/core/use_cases/pipeline/__init__.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_upsert_release.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_delete_release.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_upsert_record.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_delete_record.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_upsert_allocation.py`
- [ ] Create `tests/v2/core/use_cases/pipeline/test_delete_allocation.py`

**Phase 3: Presentation/Router Pipeline Tests** — Status: ⏳ Pending
- [ ] Create `tests/v2/presentation/api/routers/pipeline/__init__.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_auth.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_release.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_delete_release.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_record.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_delete_record.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_upsert_allocation.py`
- [ ] Create `tests/v2/presentation/api/routers/pipeline/test_delete_allocation.py`

**Phase 4: Verification** — Status: ⏳ Pending
- [ ] Run `pytest tests/v2/ -v` to execute all new and existing tests
- [ ] Fix any failures
- [ ] Confirm existing tests still pass

## 5. Test Case Catalog

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
