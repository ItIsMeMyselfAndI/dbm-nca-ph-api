import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from src.infrastructure.db.database import async_session
from src.infrastructure.db.models import ReleaseModel, RecordModel, AllocationModel


releases = [
    ReleaseModel(
        id="id_NCA_2024_Q1",
        title="Notice of Cash Allocation - First Quarter FY 2024",
        url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2024/NCA_Q1_FY2024.pdf",
        filename="NCA_Q1_FY2024.pdf",
        year=2024,
        page_count=1580,
        file_meta_created_at=datetime(2024, 1, 2, 8, 0, 0, tzinfo=timezone.utc),
        file_meta_modified_at=datetime(2024, 1, 15, 14, 30, 0, tzinfo=timezone.utc),
    ),
    ReleaseModel(
        id="id_NCA_2025_Q2",
        title="Notice of Cash Allocation - Second Quarter FY 2025",
        url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2025/NCA_Q2_FY2025.pdf",
        filename="NCA_Q2_FY2025.pdf",
        year=2025,
        page_count=1720,
        file_meta_created_at=datetime(2025, 4, 1, 6, 0, 0, tzinfo=timezone.utc),
        file_meta_modified_at=datetime(2025, 4, 10, 10, 15, 0, tzinfo=timezone.utc),
    ),
    ReleaseModel(
        id="id_SUPPL_NCA_2023",
        title="Supplemental Notice of Cash Allocation - COA Disallowance FY 2023",
        url="https://www.dbm.gov.ph/wp-content/uploads/NCA/2023/SUPPL_NCA_2023.pdf",
        filename="SUPPL_NCA_2023.pdf",
        year=2023,
        page_count=420,
        file_meta_created_at=datetime(2023, 11, 20, 9, 0, 0, tzinfo=timezone.utc),
        file_meta_modified_at=None,
    ),
]

records = [
    RecordModel(
        nca_number="NCA-NCR-25-0001001",
        nca_type="REG",
        released_date="2025-01-15T08:30:00+00:00",
        department="Department of Education (DepEd)",
        purpose="To cover the regular operating and RLIP requirements for the first quarter (January to March 2025)",
        release_id="id_NCA_2025_Q2",
    ),
    RecordModel(
        nca_number="NCA-ROVII-25-0004106",
        nca_type="REG",
        released_date="2025-02-10T09:15:00+00:00",
        department="Department of Health (DOH)",
        purpose="To cover the regular operating requirements for the Health Facilities Enhancement Program (HFEP) FY 2025",
        release_id="id_NCA_2025_Q2",
    ),
    RecordModel(
        nca_number="NCA-CAR-25-0005162",
        nca_type="REG",
        released_date="2025-03-05T10:00:00+00:00",
        department="Department of Public Works and Highways (DPWH)",
        purpose="To cover the regular operating requirements for infrastructure projects under the FY 2025 General Appropriations Act",
        release_id="id_NCA_2025_Q2",
    ),
    RecordModel(
        nca_number="NCA-NCR-24-0000001",
        nca_type="REG",
        released_date="2024-01-10T08:00:00+00:00",
        department="Department of Education (DepEd)",
        purpose="To cover the regular operating requirements for FY 2024",
        release_id="id_NCA_2024_Q1",
    ),
    RecordModel(
        nca_number="NCA-BMB-A-23-0001001",
        nca_type="REG",
        released_date="2023-12-01T09:00:00+00:00",
        department="Department of Budget and Management (DBM)",
        purpose="To cover the supplemental budget requirements per COA disallowance FY 2023",
        release_id="id_SUPPL_NCA_2023",
    ),
]

allocations = [
    AllocationModel(
        nca_number="NCA-NCR-25-0001001",
        agency="Office of the Secretary",
        operating_unit="Juan Sumulong Memorial National High School",
        amount=8_750_000.00,
    ),
    AllocationModel(
        nca_number="NCA-NCR-25-0001001",
        agency="Office of the Secretary",
        operating_unit="Quezon City Science High School",
        amount=6_200_000.00,
    ),
    AllocationModel(
        nca_number="NCA-ROVII-25-0004106",
        agency="University of the Philippines - Philippine General Hospital",
        operating_unit="",
        amount=125_000_000.00,
    ),
    AllocationModel(
        nca_number="NCA-CAR-25-0005162",
        agency="Office of the Secretary",
        operating_unit="Cordillera Center for Health Development",
        amount=48_562_000.00,
    ),
    AllocationModel(
        nca_number="NCA-NCR-24-0000001",
        agency="Office of the Secretary",
        operating_unit="Manila National High School",
        amount=9_100_000.00,
    ),
    AllocationModel(
        nca_number="NCA-BMB-A-23-0001001",
        agency="Commission on Audit",
        operating_unit="COA Central Office",
        amount=15_000_000.00,
    ),
]


async def seed():
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM release"))
        count = result.scalar()
        if count and count > 0:
            print(f"Database already has {count} release(s). Skipping seed.")
            return

        session.add_all(releases)
        await session.flush()

        session.add_all(records)
        await session.flush()

        session.add_all(allocations)
        await session.commit()

    print(
        f"Seeded {len(releases)} releases, "
        f"{len(records)} records, "
        f"{len(allocations)} allocations."
    )


asyncio.run(seed())
