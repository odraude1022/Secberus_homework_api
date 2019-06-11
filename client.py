import aiohttp
import asyncio

login = {"username": "guest", "password": "guest"}

async def authenticate(login, session):
    async with session.post('http://localhost:5000/api/login', json=login) as resp:
        token = (await resp.json()).get("access_token")
        return {"Authorization": f"Bearer {token}"}

async def secret1(session, headers):
    async with session.get('http://localhost:5000/api/secret1', headers=headers) as resp:
        if(resp.status == 401):
            headers = await authenticate(login, session)
            await secret1(session, headers)
        else:
            with open('secret1.txt', 'w') as f:
                answer1 = (await resp.json()).get("answer")
                f.write(answer1)
                print(answer1)

async def secret2(session, headers):
    async with session.get('http://localhost:5000/api/secret2', headers=headers) as resp:
        if(resp.status == 401):
            headers = await authenticate(login, session)
            await secret2(session, headers)
        else:
            with open('secret2.txt', 'w') as f:
                answer2 = (await resp.json()).get("answer")
                f.write(answer2)
                print(answer2)

async def secret3(session, headers):
    async with session.get('http://localhost:5000/api/secret3', headers=headers) as resp:
        if(resp.status == 401):
            headers = await authenticate(login, session)
            await secret3(session, headers)
        else:
            with open('secret3.txt', 'w') as f:
                answer3 = (await resp.json()).get("answer")
                f.write(answer3)
                print(answer3)


async def solution():
    async with aiohttp.ClientSession() as session:
        headers = await authenticate(login, session)
        await secret1(session, headers)
        await secret2(session, headers)
        await secret3(session, headers)

asyncio.run(solution())
