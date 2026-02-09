from supabase import create_client

from src.infrastructure.config import settings

client = create_client(
    supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_ANON_KEY
)
