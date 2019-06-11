from pathlib import Path
import pytest
import aiohttp
from client import secret, authenticate, login

answers = ["The first door, unlocked.", "The second answer.", "The final test."]

@pytest.fixture
def delete_files(scope="test"):
    for i in range(1,4):
        Path(f'./secret{i}.txt').unlink()

@pytest.mark.asyncio
async def test_secret_function(delete_files):
    async with aiohttp.ClientSession() as session:
        headers = await authenticate(login, session)
        for i in range(1,4):
            assert await(secret(session, headers, i)) == answers[i - 1]

@pytest.mark.asyncio
async def test_secret_files(delete_files):
    async with aiohttp.ClientSession() as session:
        headers = await authenticate(login, session)
        for i in range(1,4):
            await(secret(session, headers, i))
        for i in range(1,4):
            assert Path(f'./secret{i}.txt').exists()
            assert Path(f'./secret{i}.txt').read_text() == answers[i - 1]
