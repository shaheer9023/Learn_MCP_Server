import asyncio
from client import MCPclient
from test import url
from rich import print

async def main():
    async with MCPclient(url) as client:
        response=await client.plus_method(name="plus_tool",arg={
            "n1":100,
            "n2":345
        })
        print(response)


asyncio.run(main())