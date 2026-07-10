using ModelContextProtocol.Protocol;
using ModelContextProtocol.Server;
using QRCoder;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using System.ComponentModel;
using System.IO;
using System.Text;

namespace QrServerCs;

[McpServerToolType]
internal class QrTools
{
    [McpServerTool(Name = "generate_qr")]
    [Description("Generate a QR code PNG image from text or URL. Returns a base64-encoded PNG image.")]
    public static IEnumerable<ImageContentBlock> GenerateQr(
        [Description("Text or URL to encode in the QR code")] string text,
        [Description("Size in pixels of each QR module (box). Default: 5")] int box_size = 5,
        [Description("Width of the quiet zone border in modules. Default: 4")] int border = 4,
        [Description("Error correction level: L, M, Q, or H. Default: M")] string error_correction = "M",
        [Description("Foreground color as CSS name or hex (e.g. 'black', '#000000'). Default: black")] string fill_color = "black",
        [Description("Background color as CSS name or hex (e.g. 'white', '#ffffff'). Default: white")] string back_color = "white")
    {
        var safeBoxSize = Math.Clamp(box_size, 1, 20);
        var safeBorder = Math.Clamp(border, 0, 10);

        var eccLevel = error_correction.ToUpperInvariant() switch
        {
            "L" => QRCodeGenerator.ECCLevel.L,
            "Q" => QRCodeGenerator.ECCLevel.Q,
            "H" => QRCodeGenerator.ECCLevel.H,
            _ => QRCodeGenerator.ECCLevel.M
        };

        var darkBytes = ParseColor(fill_color, [0, 0, 0, 255]);
        var lightBytes = ParseColor(back_color, [255, 255, 255, 255]);

        using var generator = new QRCodeGenerator();
        var data = generator.CreateQrCode(text, eccLevel);
        var qrCode = new PngByteQRCode(data);
        var pngBytes = qrCode.GetGraphic(safeBoxSize, darkBytes, lightBytes, drawQuietZones: false);

        if (safeBorder > 0)
        {
            var pad = safeBorder * safeBoxSize;
            using var source = Image.Load<Rgba32>(pngBytes);
            using var canvas = new Image<Rgba32>(
                source.Width + (pad * 2),
                source.Height + (pad * 2),
                new Rgba32(lightBytes[0], lightBytes[1], lightBytes[2], lightBytes[3]));

            canvas.Mutate(ctx => ctx.DrawImage(source, new Point(pad, pad), 1f));

            using var output = new MemoryStream();
            canvas.SaveAsPng(output);
            pngBytes = output.ToArray();
        }

        var b64 = Convert.ToBase64String(pngBytes);

        return
        [
            new ImageContentBlock
            {
                MimeType = "image/png",
                Data = Encoding.UTF8.GetBytes(b64)
            }
        ];
    }

    private static byte[] ParseColor(string color, byte[] fallback)
    {
        var named = color.ToLowerInvariant() switch
        {
            "black" => new byte[] { 0, 0, 0, 255 },
            "white" => new byte[] { 255, 255, 255, 255 },
            "red" => new byte[] { 255, 0, 0, 255 },
            "green" => new byte[] { 0, 128, 0, 255 },
            "blue" => new byte[] { 0, 0, 255, 255 },
            _ => null
        };

        if (named is not null)
        {
            return named;
        }

        var hex = color.TrimStart('#');
        if (hex.Length is 6 or 8)
        {
            try
            {
                var r = Convert.ToByte(hex[..2], 16);
                var g = Convert.ToByte(hex[2..4], 16);
                var b = Convert.ToByte(hex[4..6], 16);
                var a = hex.Length == 8 ? Convert.ToByte(hex[6..8], 16) : (byte)255;
                return [r, g, b, a];
            }
            catch
            {
            }
        }

        return fallback;
    }
}