"""Topic index MCP server: exposes this masterclass's module and topic tree as a tool."""
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("topic-index")


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "demos").is_dir():
            return parent
    return Path.cwd()


@mcp.tool()
def list_topics(module: str = "") -> list[dict]:
    """List the modules and topics of the masterclass.

    Pass a module folder name such as "02-agentic-harness" to list only that
    module's topics. Omit it to list every module with its topic count.
    """
    demos = repo_root() / "demos"
    modules = sorted(d for d in demos.iterdir() if d.is_dir())

    if module:
        target = demos / module
        return [
            {"module": module, "topic": t.name, "readme": (t / "readme.md").exists()}
            for t in sorted(d for d in target.iterdir() if d.is_dir())
        ]

    return [
        {"module": m.name, "topics": len([d for d in m.iterdir() if d.is_dir()])}
        for m in modules
    ]


if __name__ == "__main__":
    mcp.run()
