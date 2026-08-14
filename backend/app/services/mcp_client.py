from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"


async def get_mcp_tools():

    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description
                }
                for tool in result.tools
            ]


async def call_mcp_tool(tool_name, arguments=None):

    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments or {}
            )

            return result