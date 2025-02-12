import asyncio
import pytest


class TestExample:

    def test_a(self) -> None:
        assert 1 == 1

    @pytest.mark.asyncio
    async def test_a_async(self) -> None:
        await asyncio.sleep(1)
        assert 1 == 1
