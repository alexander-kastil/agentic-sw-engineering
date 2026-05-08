using System.ComponentModel;
using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;
using QRCoder;

namespace QRServer;

[McpServerToolType]
internal class QRTools
{
    [McpServerTool]
    [Description("""
        Generate a QR code from text or URL.
        Creates QR codes that can be scanned to access URLs or decode text.
        Perfect for sharing links, contact info, WiFi credentials, and more.
        """)]
    public static IEnumerable<ContentBlock> GenerateQr(
        [Description("URL or text to encode (e.g., https://example.com)")] string text,
        [Description("Pixels per module / box size (default: 10, range: 1-50)")] int pixelsPerModule = 10,
        [Description("Error correction level - L(7%), M(15%), Q(25%), H(30%) (default: M)")] string errorCorrection = "M",
        [Description("Dark / foreground color as hex (default: #000000)")] string darkColor = "#000000",
        [Description("Light / background color as hex (default: #ffffff)")] string lightColor = "#ffffff")
    {
        var eccLevel = errorCorrection.ToUpperInvariant() switch
        {
            "L" => QRCodeGenerator.ECCLevel.L,
            "Q" => QRCodeGenerator.ECCLevel.Q,
            "H" => QRCodeGenerator.ECCLevel.H,
            _ => QRCodeGenerator.ECCLevel.M,
        };

        using var generator = new QRCodeGenerator();
        var data = generator.CreateQrCode(text, eccLevel);
        var qr = new PngByteQRCode(data);
        var pngBytes = qr.GetGraphic(pixelsPerModule, ParseColor(darkColor), ParseColor(lightColor), drawQuietZones: true);
        var base64 = Convert.ToBase64String(pngBytes);

        return [new ImageContentBlock { Data = base64, MimeType = "image/png" }];
    }

    private static byte[] ParseColor(string color)
    {
        var hex = color.TrimStart('#');
        if (hex.Length == 3)
            hex = string.Concat(hex[0], hex[0], hex[1], hex[1], hex[2], hex[2]);

        if (hex.Length == 6)
        {
            return
            [
                Convert.ToByte(hex[..2], 16),
                Convert.ToByte(hex[2..4], 16),
                Convert.ToByte(hex[4..6], 16),
                255,
            ];
        }

        return color.ToLowerInvariant() switch
        {
            "black" => [0, 0, 0, 255],
            "white" => [255, 255, 255, 255],
            "red" => [255, 0, 0, 255],
            "green" => [0, 128, 0, 255],
            "blue" => [0, 0, 255, 255],
            _ => [0, 0, 0, 255],
        };
    }
}
