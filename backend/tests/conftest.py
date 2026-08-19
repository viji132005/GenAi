import pytest
import asyncio
from app.database.seed import seed_database
from app.database.connection import engine, Base

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    async def _init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await seed_database()
    
    asyncio.run(_init())
