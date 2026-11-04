import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import colorName from "color-name";
import QRCode, { type QRCodeErrorCorrectionLevel } from "qrcode";
import { z } from "zod";

const VIEW_URI = "ui://qr-server/view.html";
const HOST = process.env.HOST ?? "0.0.0.0";
const PORT = Number(process.env.PORT ?? "3001");

const EMBEDDED_VIEW_HTML = `<!DOCTYPE html>
<html>
<head>
  <meta name="color-scheme" content="light dark">
  <style>
    html, body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: transparent;
    }
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 340px;
      width: 340px;
    }
    img {
      width: 300px;
      height: 300px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div id="qr"></div>
  <script type="module">
    import { App } from "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const app = new App({ name: "QR View", version: "1.0.0" });

    app.ontoolresult = ({ content }) => {
      const img = content?.find(c => c.type === 'image');
      if (img) {
        const qrDiv = document.getElementById('qr');
        qrDiv.innerHTML = '';

        const allowedTypes = ['image/png', 'image/jpeg', 'image/gif'];
        const mimeType = allowedTypes.includes(img.mimeType) ? img.mimeType : 'image/png';

        const image = document.createElement('img');
        image.src = \`data:\${mimeType};base64,\${img.data}\`;
        image.alt = "QR Code";
        qrDiv.appendChild(image);
      }
    };

    function handleHostContextChanged(ctx) {
      if (ctx.safeAreaInsets) {
        document.body.style.paddingTop = \`\${ctx.safeAreaInsets.top}px\`;
        document.body.style.paddingRight = \`\${ctx.safeAreaInsets.right}px\`;
        document.body.style.paddingBottom = \`\${ctx.safeAreaInsets.bottom}px\`;
        document.body.style.paddingLeft = \`\${ctx.safeAreaInsets.left}px\`;
      }
    }

    app.onhostcontextchanged = handleHostContextChanged;

    await app.connect();
    const ctx = app.getHostContext();
    if (ctx) {
      handleHostContextChanged(ctx);
    }
  </script>
</body>
</html>`;

const GENERATE_QR_DESCRIPTION = `Generate a QR code from text or URL.

This tool creates QR codes that can be scanned to access URLs or decode text.
Perfect for sharing links, contact info, WiFi credentials, and more.

Args:
    text: URL or text to encode (e.g., https://www.integrations.at)
    box_size: Size of each box in pixels (default: 5, range: 1-20)
    border: Border size in boxes (default: 4, range: 1-10)
    error_correction: Error correction level - L(7%), M(15%), Q(25%), H(30%)
    fill_color: Foreground color (hex like #FF0000 or name like black)
    back_color: Background color (hex like #FFFFFF or name like white)

Returns:
    A PNG image of the QR code
`;

const ERROR_LEVELS: Record<string, QRCodeErrorCorrectionLevel> = {
  L: "L",
  M: "M",
  Q: "Q",
  H: "H",
};

function toHex(color: string): string {
  const rgb = colorName[color.toLowerCase() as keyof typeof colorName];
  return rgb ? `#${rgb.map((channel) => channel.toString(16).padStart(2, "0")).join("")}` : color;
}

function createMcpServer(): McpServer {
  const mcp = new McpServer({ name: "QR Code Server", version: "1.0.0" });

  mcp.registerTool(
    "generate_qr",
    {
      description: GENERATE_QR_DESCRIPTION,
      inputSchema: {
        text: z.string().meta({ title: "Text" }),
        box_size: z.number().int().default(5).meta({ title: "Box Size" }),
        border: z.number().int().default(4).meta({ title: "Border" }),
        error_correction: z.string().default("M").meta({ title: "Error Correction" }),
        fill_color: z.string().default("black").meta({ title: "Fill Color" }),
        back_color: z.string().default("white").meta({ title: "Back Color" }),
      },
      _meta: {
        ui: { resourceUri: VIEW_URI },
        "ui/resourceUri": VIEW_URI,
      },
    },
    async ({ text, box_size, border, error_correction, fill_color, back_color }) => {
      const png = await QRCode.toBuffer(text, {
        errorCorrectionLevel: ERROR_LEVELS[error_correction.toUpperCase()] ?? "M",
        scale: box_size,
        margin: border,
        color: { dark: toHex(fill_color), light: toHex(back_color) },
      });
      return {
        content: [{ type: "image", data: png.toString("base64"), mimeType: "image/png" }],
      };
    },
  );

  const viewMeta = { ui: { csp: { resourceDomains: ["https://unpkg.com"] } } };

  mcp.registerResource(
    "view",
    VIEW_URI,
    {
      description: "View HTML resource with CSP metadata for external dependencies.",
      mimeType: "text/html;profile=mcp-app",
      _meta: viewMeta,
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          mimeType: "text/html;profile=mcp-app",
          _meta: viewMeta,
          text: EMBEDDED_VIEW_HTML,
        },
      ],
    }),
  );

  return mcp;
}

if (process.argv.includes("--stdio")) {
  await createMcpServer().connect(new StdioServerTransport());
} else {
  createServer(async (req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "*");
    res.setHeader("Access-Control-Allow-Headers", "*");

    if (req.method === "OPTIONS") {
      res.writeHead(204).end();
      return;
    }

    if (new URL(req.url ?? "/", "http://localhost").pathname !== "/mcp") {
      res.writeHead(404).end();
      return;
    }

    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
    res.on("close", () => transport.close());
    await createMcpServer().connect(transport);
    await transport.handleRequest(req, res);
  }).listen(PORT, HOST, () => {
    console.log(`QR Code Server listening on http://${HOST}:${PORT}/mcp`);
  });
}
