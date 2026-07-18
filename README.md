# Philippine DBM NCA API

FastAPI-based API for querying Philippine Department of Budget and Management (DBM) Notice of Cash Allocation (NCA) data.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Configuration

Copy the sample files and fill in your values:

```bash
cp .env.sample .env
cp .env.local.sample .env.local
```

Available variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes (v1) | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes (v1) | Supabase anonymous key |
| `DATABASE_URL` | Yes (v2) | PostgreSQL connection string for v2 local backend |
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
sudo -iu postgres createuser --superuser <name>
sudo -iu postgres createdb -O <name> dbm_nca_ph
```

If `Peer authentication failed`, edit `pg_hba.conf` and change `peer` to `md5` for local lines, then restart PostgreSQL.

**Set `DATABASE_URL` in `.env` (replace `<name>` and `<password>`):**
```
DATABASE_URL=postgresql+asyncpg://<name>:<password>@localhost:5432/dbm_nca_ph
```

If you configured trust or peer auth (no password), omit the password:
```
DATABASE_URL=postgresql+asyncpg://<name>@localhost:5432/dbm_nca_ph
```

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

```bash
pytest
```

## Project Structure

```
├── .env.sample                      # Environment variable template
├── .env.local.sample                # Local env template (Vercel)
├── main.py                          # Application entry point
├── src/
│   ├── core/entities/               # Domain models and filter enums
│   ├── infrastructure/config.py     # Pydantic settings (env file)
│   ├── infrastructure/db/           # Supabase repository implementations
│   └── presentation/api/            # FastAPI routes and dependencies
└── tests/
    ├── conftest.py                  # Shared fixtures (test client, repos)
    ├── infrastructure/db/           # Repository-level tests
    └── presentation/api/            # API endpoint integration tests
```
