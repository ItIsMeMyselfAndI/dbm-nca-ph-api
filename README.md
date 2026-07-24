# Philippine DBM NCA API

FastAPI-based API for querying Philippine Department of Budget and Management (DBM) Notice of Cash Allocation (NCA) data. Built with Clean Architecture, it exposes both a synchronous (v1) and asynchronous (v2) API over identical read endpoint surfaces, plus a set of authenticated write endpoints.

> **Self-hosting guide:** [`docs/guides/self-hosting-guide.md`](docs/guides/self-hosting-guide.md) — step-by-step deployment behind Cloudflare Tunnel.  
> **API documentation:** [`docs/api-documentation.md`](docs/api-documentation.md) — full reference of all endpoints, schemas, and examples.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Configuration

Copy the sample files and fill in your values:

```bash
cp env.sample .env
cp env.local.sample .env.local
```

Available variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes (v1) | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes (v1) | Supabase anonymous key |
| `PSQL_HOST` | Yes (v2) | PostgreSQL host (default: `localhost`) |
| `PSQL_USER` | Yes (v2) | PostgreSQL user (default: `postgres`) |
| `PSQL_PASS` | Yes (v2) | PostgreSQL password (default: `postgres`) |
| `PSQL_DB_NAME` | Yes (v2) | PostgreSQL database name (default: `dbm_nca_ph`) |
| `PSQL_TEST_DB_NAME` | No | PostgreSQL test database name (default: `dbm_nca_ph_test`) |
| `PIPELINE_API_KEY` | Yes (v2 private) | API key for authenticated write endpoints (`X-API-Key` header) |
| `VERCEL_OIDC_TOKEN` | No | Vercel OIDC token (deployment only) |

## Database Setup

The API supports two backends via API versioning — **v1** uses Supabase (REST), **v2** uses local PostgreSQL (SQLAlchemy + asyncpg).

### Supabase (v1)

Set up a Supabase project and populate your `.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

### Local PostgreSQL (v2)

**Install PostgreSQL:**

*Arch Linux:*
```bash
sudo pacman -S postgresql
sudo -iu postgres initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

*Debian/Ubuntu:*
```bash
sudo apt update && sudo apt install postgresql postgresql-client
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Create database and user:**
```bash
sudo -iu postgres createuser --superuser <name> -P
sudo -iu postgres createdb -O <name> dbm_nca_ph
```

If `Peer authentication failed`, edit `pg_hba.conf` and change `peer` to `md5` for local lines, then restart PostgreSQL.

**Set env vars in `.env` (replace `<name>` and `<password>`):**
```
PSQL_HOST=localhost
PSQL_USER=<name>
PSQL_PASS=<password>
PSQL_DB_NAME=dbm_nca_ph
```

If you configured trust or peer auth (no password), omit `PSQL_PASS`.

**Create tables:**
```bash
python scripts/create_tables.py
```

**Seed data (optional):**
```bash
python scripts/seed.py
```

**Verify (replace `<name>` with your username):**
```bash
psql -U <name> -h localhost -d dbm_nca_ph -c "\dt"
```
Should show: `release`, `record`, `allocation`.

## Running

```bash
python main.py
```

Binds to `0.0.0.0:8000` by default. Override via environment variables:

```bash
HOST=192.168.1.100 PORT=9000 python main.py
```

## Tests

### v1 Tests (Mock Backend)

No external dependencies — uses in-memory mock repositories:

```bash
pytest tests/v1/
```

### v2 Tests (Real PostgreSQL)

Connect to a **local PostgreSQL instance** with a superuser role. The test suite:

1. Reads `PSQL_HOST`, `PSQL_USER`, `PSQL_PASS` from your `.env` file (falls back to `postgres`/`postgres`/`localhost`)
2. Creates a temporary `dbm_nca_ph_test` database at session start
3. Creates all tables, runs 135+ tests, then drops the database

```bash
pytest tests/v2/
```

To run all tests:

```bash
pytest
```

**Note**: The test database is created/destroyed per session. Make sure your PostgreSQL is running.

### Requirements

- v2 tests require a running local PostgreSQL instance
- v1 tests run standalone with mock data

## Project Structure

```
main.py                          # Application entry point
pytest.ini                       # Pytest config (asyncio, fixture loop scope)
env.sample                       # Environment variable template
env.local.sample                 # Local env template (Vercel)
docs/
  api-documentation.md           # Full API docs
  plan-restructure-routes.md     # Route restructuring plan
  plan-pipeline-cud-v2.md        # CUD endpoints plan
  plan-restructure-tests.md      # Test restructuring plan
src/
  core/                          # Domain layer
    entities/                    #   Domain models: Release, Record, Allocation
    exceptions/                  #   NotFoundError, ValidationError
    interfaces/                  #   Repository protocols (sync + async)
    use_cases/                   #   v1 + v2 business logic
  infrastructure/
    config.py                    #   Pydantic settings (env variables)
    db/
      database.py                #   SQLAlchemy async engine + session
      models.py                  #   ORM models
      postgres_*_repository.py   #   PostgreSQL repo implementations
      supabase_*_repository.py   #   Supabase repo implementations
  presentation/
    api/
      app.py -> main.py          # FastAPI app (via main.py)
      auth.py                    # Pipeline API key auth dependency
      dependencies.py            #   v1 DI
      dependencies_v2.py         #   v2 DI (real repos)
      schemas.py                 #   Pydantic request/response schemas
      v1/                        #   v1 routes (sync, Supabase)
        routers/
          public/                #     Read endpoints
            releases.py, records.py, allocations.py
      v2/                        #   v2 routes (async, PostgreSQL)
        routers/
          public/                #     Read endpoints
            releases.py, records.py, allocations.py
          private/               #     Write endpoints (authenticated)
            __init__.py          #       Auth applied at package level
            releases.py, records.py, allocations.py
tests/
  conftest.py                    # Shared fixtures + env var setup
  core/                          # Entity unit tests
  mock/                          # Mock repository implementations
  v1/                            # v1 tests (mock repos)
  v2/                            # v2 tests (real PostgreSQL)
    conftest.py                  #   DB lifecycle, clean_db, seed fixtures
    core/use_cases/              #   Use case tests
    presentation/api/routers/
      public/                    #   Read endpoint tests
      private/                   #   Write endpoint + auth tests
```
