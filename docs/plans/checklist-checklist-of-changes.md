# Checklist: Remove `/api` Prefix from API Routes

## Completed Tasks

- [x] Updated `src/main.py` to remove `prefix="/api"` from both `app.include_router()` calls
- [x] Updated `docs/api-documentation.md`:
    - Replaced `/api/v1/` with `/v1/` for all endpoints
    - Replaced `/api/v2/` with `/v2/` for all endpoints
    - Replaced `/api/v2/private/` with `/v2/private/` for authenticated endpoints
    - Reorganized tables by HTTP method (GET, POST, DELETE, Health Check)
    - Updated Swagger UI redirect from `/api/v1/docs` to `/v1/docs`
    - Updated filtering examples from `/api/v1/` to `/v1/`
- [x] Updated `docs/plans/plan-remove-api-prefix.md` - created comprehensive implementation plan
- [x] Updated `docs/test-documentation.md`:
    - Replaced `/api/v2/private/` with `/v2/private/` in auth section
- [x] Updated test configuration in `tests/conftest.py` and `tests/v2/conftest.py`:
    - Changed TestClient base_url from `/api/v1` → `/v1` and `/api/v2` → `/v2`

## Summary

**All route prefixes have been successfully removed:**

| Version | Before | After |
|---------|--------|-------|
| v1 | `/api/v1/releases` | `/v1/releases` |
| v1 | `/api/v1/records` | `/v1/records` |
| v1 | `/api/v1/allocations` | `/v1/allocations` |
| v2 | `/api/v2/releases` | `/v2/releases` |
| v2 | `/api/v2/records` | `/v2/records` |
| v2 | `/api/v2/allocations` | `/v2/allocations` |
| v2 Private | `/api/v2/private/releases` | `/v2/private/releases` |
| v2 Private | `/api/v2/private/records` | `/v2/private/records` |
| v2 Private | `/api/v2/private/allocations` | `/v2/private/allocations` |

The API now serves all routes directly at `/v1/`, `/v2/`, and `/v2/private/` without the unnecessary `/api/` prefix, resulting in cleaner, more professional URLs for the entire Philippine DBM NCA API system.