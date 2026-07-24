import os

import asyncpg
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("PIPELINE_API_KEY", "test-api-key-123")

from main import app
from src.infrastructure.config import settings

BASE_DB = "postgres"
TEST_DB_NAME = os.environ.get("PSQL_TEST_DB_NAME", "dbm_nca_ph_test")
_USER = settings.PSQL_USER
_PASS = settings.PSQL_PASS
_HOST = settings.PSQL_HOST
_PORT = 5432


def _admin_url(db_name=BASE_DB):
    pw = f":{_PASS}" if _PASS else ""
    return f"postgresql://{_USER}{pw}@{_HOST}:{_PORT}/{db_name}"


async def _force_drop_db(conn, name):
    await conn.execute(
        f"""SELECT pg_terminate_backend(pid)
           FROM pg_stat_activity
           WHERE datname = $1 AND pid <> pg_backend_pid()""",
        name,
    )
    try:
        await conn.execute(f"DROP DATABASE IF EXISTS {name} WITH (FORCE)")
    except Exception:
        await conn.execute(f"DROP DATABASE IF EXISTS {name}")


async def _create_db():
    conn = await asyncpg.connect(dsn=_admin_url())
    try:
        await _force_drop_db(conn, TEST_DB_NAME)
        await conn.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    finally:
        await conn.close()


async def _drop_db():
    conn = await asyncpg.connect(dsn=_admin_url())
    try:
        await _force_drop_db(conn, TEST_DB_NAME)
    finally:
        await conn.close()


async def _create_tables():
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS "release" (
                id VARCHAR PRIMARY KEY,
                title VARCHAR NOT NULL,
                url TEXT NOT NULL,
                filename VARCHAR NOT NULL,
                year INTEGER NOT NULL,
                page_count INTEGER DEFAULT 0,
                file_meta_created_at TIMESTAMPTZ,
                file_meta_modified_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS "record" (
                id UUID PRIMARY KEY,
                nca_number VARCHAR UNIQUE NOT NULL,
                nca_type VARCHAR NOT NULL,
                department VARCHAR NOT NULL,
                released_date VARCHAR NOT NULL,
                purpose TEXT NOT NULL,
                release_id VARCHAR NOT NULL REFERENCES "release"(id),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS "allocation" (
                id UUID PRIMARY KEY,
                operating_unit VARCHAR NOT NULL,
                agency VARCHAR NOT NULL,
                amount FLOAT NOT NULL,
                nca_number VARCHAR NOT NULL REFERENCES "record"(nca_number),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    finally:
        await conn.close()


async def _drop_tables():
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        await conn.execute('DROP TABLE IF EXISTS "allocation" CASCADE')
        await conn.execute('DROP TABLE IF EXISTS "record" CASCADE')
        await conn.execute('DROP TABLE IF EXISTS "release" CASCADE')
    finally:
        await conn.close()


@pytest.fixture(scope="session", autouse=True)
async def db_lifecycle():
    await _create_db()
    await _create_tables()
    yield
    await _drop_tables()
    await _drop_db()


@pytest.fixture(autouse=True)
async def clean_db():
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        async with conn.transaction():
            for table in ("allocation", "record", "release"):
                await conn.execute(f"DELETE FROM \"{table}\"")
    finally:
        await conn.close()


@pytest.fixture
def client():
    with TestClient(app, base_url="http://testserver/v2") as c:
        yield c


@pytest.fixture
def auth_header():
    return {"X-API-Key": os.environ["PIPELINE_API_KEY"]}


# ---------------------------------------------------------------------------
# Seed fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def seed_releases():
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        rows = [
            ("test_release_a", "Test Release A", 2024,
             "http://test.example/a", "test_a.pdf", 10),
            ("test_release_b", "Test Release B", 2025,
             "http://test.example/b", "test_b.pdf", 20),
            ("test_release_c", "Test Release C", 2026,
             "http://test.example/c", "test_c.pdf", 30),
        ]
        for r_id, title, year, url, fn, pg in rows:
            await conn.execute(
                """INSERT INTO "release" (id, title, year, url, filename, page_count)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                r_id, title, year, url, fn, pg,
            )
    finally:
        await conn.close()
    return [
        {"id": r[0], "title": r[1], "year": r[2], "url": r[3], "filename": r[4], "page_count": r[5]}
        for r in rows
    ]


@pytest.fixture
async def seed_records(seed_releases):
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        records = [
            ("00000000-0000-0000-0000-000000000001", "test_nca_001", "test_type_a",
             "Test Department Alpha", "2024-01-15",
             "Test purpose alpha", "test_release_a"),
            ("00000000-0000-0000-0000-000000000002", "test_nca_002", "test_type_b",
             "Test Department Beta", "2024-02-20",
             "Test purpose beta", "test_release_a"),
            ("00000000-0000-0000-0000-000000000003", "test_nca_003", "test_type_a",
             "Test Department Alpha", "2024-03-10",
             "Test purpose gamma", "test_release_a"),
        ]
        for r_id, nca, typ, dept, date, purp, rel_id in records:
            await conn.execute(
                """INSERT INTO "record" (id, nca_number, nca_type, department,
                                        released_date, purpose, release_id)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                r_id, nca, typ, dept, date, purp, rel_id,
            )
    finally:
        await conn.close()
    return [
        {"id": r[0], "nca_number": r[1], "nca_type": r[2],
         "department": r[3], "released_date": r[4],
         "purpose": r[5], "release_id": r[6]}
        for r in records
    ]


@pytest.fixture
async def seed_allocations(seed_records):
    conn = await asyncpg.connect(dsn=_admin_url(TEST_DB_NAME))
    try:
        allocations = [
            ("00000000-0000-0000-0000-000000000101", "test_nca_001", "Test Agency One",
             "Test OU North", 100000.00),
            ("00000000-0000-0000-0000-000000000102", "test_nca_001", "Test Agency Two",
             "Test OU South", 200000.00),
            ("00000000-0000-0000-0000-000000000201", "test_nca_002", "Test Agency One",
             "Test OU East", 150000.00),
        ]
        for a_id, nca, agency, ou, amount in allocations:
            await conn.execute(
                """INSERT INTO "allocation" (id, nca_number, agency,
                                            operating_unit, amount)
                   VALUES ($1, $2, $3, $4, $5)""",
                a_id, nca, agency, ou, amount,
            )
    finally:
        await conn.close()
    return [
        {"id": a[0], "nca_number": a[1], "agency": a[2],
         "operating_unit": a[3], "amount": a[4]}
        for a in allocations
    ]
