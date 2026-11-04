# Implementing & Using MCP Apps

## What are MCP Apps?

MCP Apps extend the Model Context Protocol (MCP) by providing a standardized way to deliver interactive user interfaces directly from MCP servers. While MCP tools typically return text and structured data, MCP Apps enable rich, interactive experiences like charts, forms, dashboards, design canvases, and video players to render inline in chat clients such as Claude, ChatGPT, VS Code, and other compliant hosts.

This solves a critical gap: MCP provides the tools and data access, while MCP Apps provide the visual interface. Your UI renders in context, in the conversation, without requiring users to navigate away from their chat client.

![MCP Apps demonstration showing interactive UI rendered in chat](./_images/mcp-app.jpg)

## MCP Server Implementations

| Server                                 | Description                                                           |
| -------------------------------------- | --------------------------------------------------------------------- |
| **[QR Code MCP Server](./qr-server/)** | Generate QR codes from URLs and text directly in GitHub Copilot Chat. |

## How MCP Apps Work

MCP Apps are built on standardized specifications and SDKs maintained at the official Model Context Protocol repository. The protocol works through a clean separation of concerns:

1. Tool definition: Your MCP server tool declares a `ui://` resource containing its HTML interface
2. Tool call: The LLM calls the tool on your server
3. Host renders: The host fetches the resource and displays it in a sandboxed iframe
4. Bidirectional communication: The host passes tool data to the UI via notifications, and the UI can call other tools through the host

The MCP Apps specification is maintained in the official `modelcontextprotocol/ext-apps` repository and provides SDKs for multiple roles. App developers build interactive Views while host developers embed those Views in chat clients, and MCP server authors register tools with UI metadata. Supported frameworks include React, Vue, Svelte, and vanilla JavaScript.

## MCP Apps Register Tools the Model Can Call

The flow above has one direction for the model: it calls a tool, and the host renders the result in the app. The app could show data and call other tools through the host, but the language model never saw anything the app itself offered. Since VS Code 1.145, an MCP app can register tools that the language model can call in its next request. The interface and the model now work on the same thing.

The user clicks and types in the interface, and the model works through tools. When the app registers tools, the model gets a handle on the state the user is looking at.

| Aspect | Before VS Code 1.145 | Since VS Code 1.145 |
| ------ | -------------------- | ------------------- |
| Who defines the tools | The MCP server | The MCP server, and now the app registers tools too |
| What the model can call | The server's tools | The server's tools plus the tools the app registers |
| When the model can use them | Once the server lists them | In the model's next request |
| Role of the interface | Displays a result and calls tools through the host | Displays a result and offers tools to the model |

The reference example is the ShaderToy server from the `ext-apps` repository. The app renders a shader in the chat, and the model can iterate on that shader in real time. You ask for a change in plain words, the model uses the tools the app registered, and the picture on screen follows. 

The QR code server in this topic is the display-only case: its interface shows the PNG it receives and registers no tools of its own. A useful design exercise is to ask which tools a QR interface could register if it needed a conversation with the model, such as changing the colors of the code you are looking at. Every app author faces that decision: which part of the interface state should the model act on?

Keep the same care you apply to any tool. A registered tool needs a clear name, a description the model can use to decide when to call it, and a narrow effect.

## QR Code MCP Server Example

The [qr-server](./qr-server) demonstration shows a practical MCP App that generates QR codes from URLs and text. The server is written in Python using the FastMCP framework and the qrcode library, making it lightweight and easy to run.

When invoked through GitHub Copilot or other MCP clients, the QR Code server generates a PNG image and displays it in an interactive UI embedded directly in the chat. The UI is defined as an embedded HTML view with styling and JavaScript that handles receiving the generated QR code data from the MCP server.

Parameters like box size, border dimensions, error correction level, and colors can be customized, giving users full control over the generated output. The server accepts standard input/output (stdio) transport, making it simple to configure in `.vscode/mcp.json` or other MCP client configuration files.

### How it works

The server uses the FastMCP decorator pattern to expose the QR code generation as a tool with UI metadata. The `@mcp.tool` decorator registers the tool and specifies the `ui/resourceUri` pointing to the HTML view that will render the output.

The tool accepts parameters for customization: text (the content to encode), box_size (pixel dimensions 1-20), border (quiet zone size), and error_correction (L/M/Q/H levels ranging from 7% to 30% recovery). Color options (fill_color and back_color) support hex values or named colors.

The implementation generates QR codes using the Python qrcode library with configurable error correction levels mapped to the qrcode.constants module. The generated PIL image is encoded to PNG format and returned as base64-encoded ImageContent.

The UI layer is embedded as a single HTML resource that loads the MCP Apps SDK from a CDN (`@modelcontextprotocol/ext-apps`). The JavaScript App class receives tool results via the `ontoolresult` handler, extracts the image data, and renders it in an img element. It also handles host context changes to respect safe area insets on mobile or windowed clients.

The server supports two transport modes. Stdio mode, enabled with the `--stdio` flag, suits CLI-based MCP clients such as the Copilot CLI and VS Code. HTTP mode uses Uvicorn with CORS middleware for web-based clients, making it compatible with any MCP-compliant host.

## Links & Resources

- [MCP Apps specification](https://github.com/modelcontextprotocol/ext-apps) - the `ui://` resource contract, the App SDK, and the host rendering rules
- [Model Context Protocol](https://modelcontextprotocol.io/introduction) - tools, resources, and transports the Apps layer builds on
- [FastMCP](https://gofastmcp.com/) - the Python framework and the `@mcp.tool` decorator used by the QR server
