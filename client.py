import aiohttp
import asyncio

login = {"username": "guest", "password": "guest"}

async def authenticate(login, session):
    async with session.post('http://localhost:5000/api/login', json=login) as resp:
        token = (await resp.json()).get("access_token")
        return {"Authorization": f"Bearer {token}"}

async def secret(session, headers, num):
    async with session.get(f'http://localhost:5000/api/secret{num}', headers=headers) as resp:
        if(resp.status == 401):
            headers = await authenticate(login, session)
            return(await secret(session, headers, num))
        else:
            with open(f'secret{num}.txt', 'w') as f:
                answer = (await resp.json()).get("answer")
                f.write(answer)
                return answer

async def solution():
    async with aiohttp.ClientSession() as session:
        headers = await authenticate(login, session)
        print(await secret(session, headers, 1))
        print(await secret(session, headers, 2))
        print(await secret(session, headers, 3))

asyncio.run(solution())
