from mcp import ClientSession
from typing import Optional
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamable_http_client
class MCPclient:

    def __init__(self,url):
        self.session:Optional[ClientSession]=None
        self.exit_stack=AsyncExitStack()
        self.url=url
        
    async def __aenter__(self):
        print("Enter Session")
        read,write,_ = await self.exit_stack.enter_async_context(streamable_http_client(self.url))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read,write))
        await self.session.initialize()
        return self

    async def __aexit__(self,*arg):
        print("session exit")
        await self.exit_stack.aclose()



#  list available tools
    async def my_tools(self):
        response= await self.session.list_tools()
        tools=response.tools
        print(f"\nconnected to server with tools  {[tool.name for tool in tools]}")

    async def plus_method(self,name,arg):
        response= await self.session.call_tool(name=name,arguments=arg)
        return response
