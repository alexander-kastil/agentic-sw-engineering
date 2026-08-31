# Model Context Protocol & MCP Registry

Model Context Protocol (MCP) is the standardized framework that connects GitHub Copilot to external tools, services, and data sources. It extends Copilot beyond code generation into infrastructure management, testing automation, and domain-specific tooling. This topic covers MCP from both ends: consuming servers that already exist, then writing your own.

Work through them in order. The basics teach the configuration surface and the registry you discover servers in, and the implementation half then shows what the same protocol looks like from the server side, using three working servers shipped in [/src](/src/).

| Topic | Description |
|-------|-------------|
| [MCP Basics & the MCP Registry](./01-basics/) | Discover, configure, and call MCP servers: local `stdio` executables, remote HTTP endpoints, global versus workspace `mcp.json`, and secure input parameters. |
| [Implementing MCP Servers](./02-implementing/) | Write your own servers in Python and C#, choose a transport, add state and dependency injection, and debug them with the MCP Inspector before a client ever sees them. |
