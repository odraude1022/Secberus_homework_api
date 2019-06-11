import aiohttp
import asyncio

login = {"username": "guest", "password": "guest"}

async def authenticate(login, session):
    async with session.post('http://localhost:5000/api/login', json=login) as resp:
        print(resp.status)
        return (await resp.json()).get("access_token")


async def solution():
    async with aiohttp.ClientSession() as session:
        token = await authenticate(login, session)
        headers={"Authorization": f"Bearer {token}"}
        print(headers)
        async with session.get('http://localhost:5000/api/secret1', headers=headers) as resp:
            print(resp.status)
            with open('secret1.txt', 'w') as f:
                answer1 = (await resp.json()).get("answer")
                f.write(answer1)
                print(answer1)
        async with session.get('http://localhost:5000/api/secret2', headers=headers) as resp:
            print(resp.status)
            if(resp.status == 200):
                with open('secret2.txt', 'w') as f:
                    answer2 = (await resp.json()).get("answer")
                    f.write(answer2)
                    print(answer2)
        async with session.get('http://localhost:5000/api/secret3', headers=headers) as resp:
            print(resp.status)
            if(resp.status == 200):
                with open('secret3.txt', 'w') as f:
                    answer3 = (await resp.json()).get("answer")
                    f.write(answer3)
                    print(answer3)
        await session.close()

asyncio.run(solution())
