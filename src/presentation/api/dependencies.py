from src.infrastructure.db.supabase_allocation_repository import (
    SupabaseAllocationRepository,
)
from src.infrastructure.db.supabase_record_repository import SupabaseRecordRepository
from src.infrastructure.db.supabase_release_repository import SupabaseReleaseRepository


def get_record_repository():
    return SupabaseRecordRepository()


def get_allocation_repository():
    return SupabaseAllocationRepository()


def get_release_repository():
    return SupabaseReleaseRepository()
