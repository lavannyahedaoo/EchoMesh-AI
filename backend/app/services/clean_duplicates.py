import asyncio
import os
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import engine  # type: ignore
from sqlalchemy import text

async def clean_duplicates():
    print("Connecting to CockroachDB to remove duplicate memories...")
    
    # SQL query to delete duplicate memories based on matching title and content,
    # keeping the earliest created memory.
    delete_query = text("""
        DELETE FROM memories 
        WHERE id IN (
            SELECT id 
            FROM (
                SELECT id, ROW_NUMBER() OVER(PARTITION BY title, content ORDER BY created_at ASC) as row_num 
                FROM memories
            ) t 
            WHERE t.row_num > 1
        );
    """)

    async with engine.begin() as conn:
        result = await conn.execute(delete_query)
        print(f"Cleanup finished successfully! Removed duplicate rows.")

if __name__ == "__main__":
    asyncio.run(clean_duplicates())
