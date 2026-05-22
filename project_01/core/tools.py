import json
from typing import Optional, List
from mcp.types import CallToolResult, TextContent
from mcp_client import MCPClient


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list:
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], response
    ) -> list:
        """OpenAI format mein tool calls handle karta hai"""
        
        tool_calls = response.choices[0].message.tool_calls or []
        tool_results = []

        for tool_call in tool_calls:
            tool_use_id = tool_call.id
            tool_name = tool_call.function.name
            try:
                tool_input = json.loads(tool_call.function.arguments)
            except:
                tool_input = {}

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "content": "Could not find that tool",
                })
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = tool_output.content if tool_output else []
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "content": content_json,
                })
            except Exception as e:
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "content": json.dumps({"error": str(e)}),
                })

        return tool_results