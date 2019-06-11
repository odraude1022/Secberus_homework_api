import asyncio
import aiohttp
from pathlib import Path

login = {"username": "guest", "password": "guest"}
url = 'http://localhost:5000/api/{}'

async def authenticate(login, session):
    async with session.post(url.format('login'), json=login) as resp:
        token = (await resp.json()).get("access_token")
        return {"Authorization": f"Bearer {token}"}

async def secret(session, headers, num):
    async with session.get(url.format(f'secret{num}'), headers=headers) as resp:
        if(resp.status == 401):
            headers = await authenticate(login, session)
            return(await secret(session, headers, num))
        else:
            answer = (await resp.json()).get("answer")
            Path(f'secret{num}.txt').write_text(answer)
            return answer

async def solution():
    async with aiohttp.ClientSession() as session:
        headers = await authenticate(login, session)
        for i in range(1, 4):
            print(await secret(session, headers, i))

asyncio.run(solution())
