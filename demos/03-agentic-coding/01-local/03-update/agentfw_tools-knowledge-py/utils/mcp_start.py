from contextlib import asynccontextmanager
from agent_framework import MCPStdioTool
from .uv_utils import resolve_uvx


@asynccontextmanager
async def start_calculator_server():
    """
    Start the local MCP calculator server using uvx and yield the MCP tool.
    Prints the resolved command for transparency.
    """
    uvx_cmd = resolve_uvx()
    print(f"Command: {uvx_cmd} mcp-server-calculator")

    async with MCPStdioTool(
        name="calculator",
        command=uvx_cmd,
        args=["mcp-server-calculator"],
    ) as mcp_server:
        print("✅ MCP server started successfully!\n")
        yield mcp_server
