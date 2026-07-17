# Philippine DBM NCA API

FastAPI-based API for querying Philippine Department of Budget and Management (DBM) Notice of Cash Allocation (NCA) data.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

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
