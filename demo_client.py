import asyncio
from acp_sdk.client import Client
from colorama import Fore

async def client_test() -> None:

    user_query = input("Enter ur question: ")
    async with Client(base_url="http://127.0.0.1:8001") as client:
        run = await client.run_sync(
            agent="cloud_engineer",
            input=user_query
        )
        print(Fore.YELLOW + run.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(client_test())