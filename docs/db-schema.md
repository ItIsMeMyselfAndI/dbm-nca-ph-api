# Database Schema

## Overview

Three tables with foreign-key relationships:

```
release ──┐
          │
record  ──┤──> nca_number
          │
allocation ┘
```

- A **Release** contains many **Records**
- A **Record** belongs to one **Release** and can have many **Allocations**
- An **Allocation** belongs to one **Record**

---

## Table: `release`

Stores DBM release documents (NCA issuance bulletins).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `VARCHAR` | `PRIMARY KEY` | Release identifier (e.g. `"NCA-2024-001"`) |
| `title` | `VARCHAR` | `NOT NULL` | Descriptive title |
| `url` | `TEXT` | `NOT NULL` | Link to the published PDF |
| `filename` | `VARCHAR` | `NOT NULL` | PDF filename |
| `year` | `INTEGER` | `NOT NULL` | Fiscal year |
| `page_count` | `INTEGER` | `DEFAULT 0` | Number of pages |
| `file_meta_created_at` | `TIMESTAMPTZ` | Nullable | PDF metadata created timestamp |
| `file_meta_modified_at` | `TIMESTAMPTZ` | Nullable | PDF metadata modified timestamp |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row last-updated timestamp |

**Relationships:**
- `records` → `record(release_id)`

---

## Table: `record`

Stores individual NCA (Notice of Cash Allocation) records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `UUID` | `PRIMARY KEY` | Auto-generated UUID |
| `nca_number` | `VARCHAR` | `UNIQUE NOT NULL` | Official NCA number (e.g. `"NCA-2024-001-A"`) |
| `nca_type` | `VARCHAR` | `NOT NULL` | Type of allocation |
| `department` | `VARCHAR` | `NOT NULL` | Department or agency name |
| `released_date` | `VARCHAR` | `NOT NULL` | Date released (stored as string, e.g. `"2024-01-15"`) |
| `purpose` | `TEXT` | `NOT NULL` | Purpose or description of the allocation |
| `release_id` | `VARCHAR` | `NOT NULL REFERENCES release(id)` | FK to parent release |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row last-updated timestamp |

**Indexes:**
- Unique index on `nca_number`

**Relationships:**
- `release` → `release(id)`
- `allocations` → `allocation(nca_number)`

---

## Table: `allocation`

Stores allocation breakdowns for each NCA record (agency-level detail).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `UUID` | `PRIMARY KEY` | Auto-generated UUID |
| `operating_unit` | `VARCHAR` | `NOT NULL` | Operating unit (e.g. `"OU North"`) |
| `agency` | `VARCHAR` | `NOT NULL` | Agency name |
| `amount` | `FLOAT` | `NOT NULL` | Allocated amount in PHP |
| `nca_number` | `VARCHAR` | `NOT NULL REFERENCES record(nca_number)` | FK to parent record |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `NOT NULL DEFAULT NOW()` | Row last-updated timestamp |

**Relationships:**
- `record` → `record(nca_number)`

---

## Entity-Relationship Diagram

```
┌────────────────┐
│    release     │
├────────────────┤
│ id (PK)        │──┐
│ title          │  │
│ url            │  │
│ filename       │  │
│ year           │  │
│ page_count     │  │
└────────────────┘  │
                    │
┌───────────────────┘
│
▼
┌──────────────────────┐
│       record         │
├──────────────────────┤
│ id (PK)              │
│ nca_number (UNIQUE)  │──┐
│ nca_type             │  │
│ department           │  │
│ released_date        │  │
│ purpose              │  │
│ release_id (FK)      │  │
└──────────────────────┘  │
                          │
┌─────────────────────────┘
│
▼
┌───────────────────────┐
│     allocation        │
├───────────────────────┤
│ id (PK)               │
│ operating_unit        │
│ agency                │
│ amount                │
│ nca_number (FK)       │
└───────────────────────┘
```

---

## SQLAlchemy ORM Models

Defined in `src/infrastructure/db/models.py`:

| Class | Table |
|-------|-------|
| `ReleaseModel` | `release` |
| `RecordModel` | `record` |
| `AllocationModel` | `allocation` |

All three inherit from `Base` (`DeclarativeBase`). Relationships use `back_populates` for bidirectional navigation.

---

## Domain Entities

Defined in `src/core/entities/`:

| File | Entity |
|------|--------|
| `release.py` | `Release` |
| `record.py` | `Record` |
| `allocation.py` | `Allocation` |
| `record_filter.py` | `RecordFilter` |
| `allocation_filter.py` | `AllocationFilter` |

Domain entities are plain Pydantic/dataclass models separate from ORM models.
