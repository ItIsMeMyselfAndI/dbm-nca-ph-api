from typing import List

from src.core.entities.release import Release
from src.core.interfaces.release_repository import ReleaseRepository
from src.infrastructure.db.supabase_client import client


class SupabaseReleaseRepository(ReleaseRepository):
    def __init__(self):
        self.client = client

    def get_release_by_id(self, id: str) -> Release | None:
        response = self.client.table("release").select("*").eq("id", id).execute()
        data = response.model_dump().get("data", None)
        if not data:
            return None

        release = Release(**data[0])
        return release

    def list_releases(self, limit: int, cursor: str | None = None) -> List[Release]:
        query = self.client.table("release").select("*")

        if cursor is not None:
            query = query.gt("id", cursor)
        query = query.order("id", desc=False).limit(limit)

        response = query.execute()
        data = response.model_dump().get("data", None)
        if not data:
            return []

        releases = [Release(**item) for item in data]
        return releases
