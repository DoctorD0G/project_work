import asyncio
import sys

import pytest

from infrastructure.container import container, init_container

if sys.platform.startswith("win"):

    @pytest.yield_fixture(scope="session")
    def event_loop():
        """
        Create an instance of the default event loop for each test case.
        https://github.com/pytest-dev/pytest-asyncio/issues/371
        """
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        res = policy.new_event_loop()
        asyncio.set_event_loop(res)
        res._close = res.close
        res.close = lambda: None
        yield res
        res._close()

else:

    @pytest.fixture(scope="session")
    def event_loop():
        return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def dependencies():
    init_container()
    try:
        yield container
    finally:
        container.unwire()
