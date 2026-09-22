# QR Code MCP Server

Generate QR codes from URLs and text in GitHub Copilot Chat.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
# or with uv: uv run server.py --stdio
```

## Use in GitHub Copilot

1. Open Copilot Chat (Ctrl+L)
2. Switch to **Agent** mode
3. Ask: `Generate a QR code for https://www.integrations.at`

The MCP server is configured in `.vscode/mcp.json` and will be automatically available.

## Parameters

- `text` - URL or text to encode (required)
- `box_size` - Size in pixels (default: 5)
- `border` - Border size (default: 4)
- `error_correction` - Level: L/M/Q/H (default: M)
- `fill_color` - Foreground color (default: black)
- `back_color` - Background color (default: white)
