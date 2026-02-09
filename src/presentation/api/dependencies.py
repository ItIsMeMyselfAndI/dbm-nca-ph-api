from src.core.interfaces.allocation_repository import AllocationRepository
from src.core.interfaces.record_repository import RecordRepository
from src.core.interfaces.release_repository import ReleaseRepository
from src.infrastructure.db.supabase_allocation_repository import (
    SupabaseAllocationRepository,
)
from src.infrastructure.db.supabase_record_repository import SupabaseRecordRepository
from src.infrastructure.db.supabase_release_repository import SupabaseReleaseRepository


def get_release_repository() -> ReleaseRepository:
    return SupabaseReleaseRepository()


def get_record_repository() -> RecordRepository:
    return SupabaseRecordRepository()


def get_allocation_repository() -> AllocationRepository:
    return SupabaseAllocationRepository()
