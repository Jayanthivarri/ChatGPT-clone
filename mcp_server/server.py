from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ChatGPT Clone MCP Server")


@mcp.tool()
def calculate(expression: str) -> str:
    """Perform a basic mathematical calculation."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Invalid mathematical expression."


@mcp.tool()
def get_project_info() -> str:
    """Get information about the ChatGPT Clone project."""
    return """
    Project: ChatGPT Clone
    Frontend: React
    Backend: FastAPI
    Database: SQLite
    Deployment: Render
    MCP: Model Context Protocol
    """


@mcp.tool()
def greet(name: str) -> str:
    """Greet a user."""
    return f"Hello {name}! Welcome to the ChatGPT Clone MCP Server."


if __name__ == "__main__":
    mcp.run(transport="streamable-http", json_response=True,host="127.0.0.1",port=8001)