# Implementation Plan: Break `DATABASE_URL` into Individual Env Vars

## 1. Context & Objectives
- **User Intent:** Replace the opaque `DATABASE_URL` connection string with explicit, individual environment variables for each PostgreSQL connection parameter (host, user, password, database name, test database name). This makes configuration more transparent and eliminates the need for URL parsing in the test suite.
- **Goal:** Introduce `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME`, and `PSQL_TEST_DB_NAME` env vars, compose `DATABASE_URL` internally from them, and update all consumers (config, tests, docs).
- **Current Implementation:** `DATABASE_URL` is a single string `postgresql+asyncpg://user:pass@host:port/dbname` used directly by SQLAlchemy and parsed by tests.
- **Target Implementation:** Users set individual `PSQL_*` vars in `.env`. The API config composes `DATABASE_URL` internally. Tests read individual vars directly. `DATABASE_URL` is no longer an env var users need to set.

## 2. Issue Mapping

| Problem / Gap | Proposed Solution | Specific Fix / Implementation Detail |
| :--- | :--- | :--- |
| Opaque connection string requires URL parsing in tests | Split into discrete env vars | Introduce `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME`, `PSQL_TEST_DB_NAME` |
| Hardcoded defaults in config.py | Move defaults to a single place | `PSQL_HOST` defaults to `localhost`, `PSQL_USER` to `postgres`, `PSQL_PASS` to `postgres`, `PSQL_DB_NAME` to `dbm_nca_ph` |
| Tests parsed DATABASE_URL to get credentials | Use individual vars directly | `tests/v2/conftest.py` reads `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME`, `PSQL_TEST_DB_NAME` |

## 3. Scope & File Modifications

### Modified Files
| File Path | Planned Changes | Reason |
| :--- | :--- | :--- |
| `env.sample` | Replace `DATABASE_URL` line with 5 new `PSQL_*` vars | Document new env vars for developers |
| `src/infrastructure/config.py` | Add `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME` fields; compose `DATABASE_URL` as a computed property | API needs to build the connection string for SQLAlchemy |
| `tests/conftest.py` | Set `PSQL_*` env vars instead of `DATABASE_URL` | Root test fixture must provide defaults for the new vars |
| `tests/v2/conftest.py` | Read `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_TEST_DB_NAME` directly; remove urlparse import | Tests get credentials from explicit vars, no parsing needed |
| `README.md` | Update "Configuration" table and "Local PostgreSQL" section to use new vars | Keep developer docs in sync |
| `docs/test-documentation.md` | Update env vars table and troubleshooting section | Keep test docs in sync |

### Excluded Files (Analyzed but untouched)
| File Path | Reason for Not Changing |
| :--- | :--- |
| `src/infrastructure/db/database.py` | Still uses `settings.DATABASE_URL` internally — no change needed |
| `plan/local-postgres-migration.md` | Historical plan, not updated |
| `main.py` | No direct reference to `DATABASE_URL` |

## 4. Execution Plan

### Phase Breakdown
- **Phase 1:** Update `env.sample` with new vars
- **Phase 2:** Update `src/infrastructure/config.py` to accept new vars and compose URL
- **Phase 3:** Update `tests/conftest.py` and `tests/v2/conftest.py` to use new vars
- **Phase 4:** Update `README.md` and `docs/test-documentation.md`
- **Phase 5:** Verify all tests pass

### Phase Status & Checklist

**Phase 1: Update `env.sample`** — Status: ✅ Done
- [x] Replace `DATABASE_URL=...` with `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME`, `PSQL_TEST_DB_NAME`

**Phase 2: Update `src/infrastructure/config.py`** — Status: ✅ Done
- [x] Add `PSQL_HOST: str = "localhost"`
- [x] Add `PSQL_USER: str = "postgres"`
- [x] Add `PSQL_PASS: str = "postgres"`
- [x] Add `PSQL_DB_NAME: str = "dbm_nca_ph"`
- [x] Add `DATABASE_URL` as a computed property composing the above fields
- [x] Verify pydantic-settings compatibility

**Phase 3: Update test conftest files** — Status: ✅ Done
- [x] `tests/conftest.py`: set `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS`, `PSQL_DB_NAME` defaults
- [x] `tests/v2/conftest.py`: read `PSQL_*` vars directly, remove `urlparse`, update `_admin_url`

**Phase 4: Update documentation** — Status: ✅ Done
- [x] `README.md`: replace `DATABASE_URL` references with new vars
- [x] `docs/test-documentation.md`: replace `DATABASE_URL` references with new vars

**Phase 5: Verify** — Status: ✅ Done
- [x] Run `pytest tests/v2/ -x` and confirm all 135 tests pass
