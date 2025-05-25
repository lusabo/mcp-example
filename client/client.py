import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        response = await client.call_tool("hello", {"name": "World"})
        print(response[0].text)

asyncio.run(main())
