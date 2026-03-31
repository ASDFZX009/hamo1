import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
# ใช้ service role key สำหรับ backend (ชื่อใน .env คือ SUPABASE_KEY)
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY (or SUPABASE_ANON_KEY) must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)