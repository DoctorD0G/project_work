import pytest_asyncio

from infrastructure.repositories.psql.db import Base


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_setup(dependencies):
    psql_db_client = dependencies.psql_db_client()

    async with psql_db_client._async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
