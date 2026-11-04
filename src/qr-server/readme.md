# QR Code MCP Server

The same MCP server in three stacks. Each exposes one `generate_qr` tool that turns text or a URL into a PNG QR code, over stdio and Streamable HTTP, so the SDK differences show side by side while the tool contract stays identical.

## Table of Contents

| Project                                | Description                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------- |
| [QR Server - C#](./qr-server-cs)       | ASP.NET Core with the `ModelContextProtocol` SDK, QRCoder and SkiaSharp         |
| [QR Server - Python](./qr-server-py)   | Python with the `mcp` SDK and `qrcode`, pinned packages, run with `uv`          |
| [QR Server - TypeScript](./qr-server-ts) | Node.js with `@modelcontextprotocol/sdk` and `qrcode`, pinned packages        |
