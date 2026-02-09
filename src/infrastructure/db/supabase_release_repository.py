from typing import List

from src.core.domain.release import Release
from src.core.interfaces.release_repository import ReleaseRepository


class SupabaseReleaseRepository(ReleaseRepository):
    def __init__(self, client):
        self.client = client

    def get_release_by_id(self, id: str) -> Release:
        response = self.client.table("releases").select("*").eq("id", id).execute()
        data = response.data
        if not data:
            raise ValueError(f"Release with ID {id} not found.")
        release = Release(**data[0])
        return release

    def list_releases(self, cursor: int, limit: int) -> List[Release]:
        response = (
            self.client.table("releases")
            .select("*")
            .range(cursor, cursor + limit - 1)
            .execute()
        )
        data = response.data
        if not data:
            return []
        releases = [Release(**item) for item in data]
        return releases
