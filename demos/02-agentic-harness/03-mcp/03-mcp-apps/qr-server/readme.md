# QR Code MCP Server

Generate QR codes from URLs and text in GitHub Copilot Chat.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
# or with uv: uv run server.py --stdio
```

## Use in GitHub Copilot

1. Open Copilot Chat
2. Switch to **Agent** mode
3. Ask: `Generate a QR code for https://www.integrations.at`

The MCP server is configured in [`.vscode/mcp.json`](./.vscode/mcp.json) and becomes available once you start it from that file.

> Note: To reach the same server from the Copilot CLI instead, register it with `copilot mcp add qr-code -- uv run server.py --stdio` from this folder.

## Parameters

- `text` - URL or text to encode (required)
- `box_size` - Size in pixels (default: 5)
- `border` - Border size (default: 4)
- `error_correction` - Level: L/M/Q/H (default: M)
- `fill_color` - Foreground color (default: black)
- `back_color` - Background color (default: white)

## Links & Resources

- [MCP Apps specification](https://github.com/modelcontextprotocol/ext-apps) - the `ui://` resource contract this server implements
- [FastMCP](https://gofastmcp.com/) - the `@mcp.tool` decorator and the stdio and HTTP transports used here
- [Model Context Protocol](https://modelcontextprotocol.io/introduction) - tools, resources, and how a host connects to a server
