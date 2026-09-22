using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

namespace PictureOptimizer;

public class ImageOptimizerService : BackgroundService
{
    private static readonly Dictionary<ImageSize, (int Width, int Height)> Dimensions = new()
    {
        { ImageSize.ExtraSmall, (150, 130) },
        { ImageSize.Small, (640, 400) },
        { ImageSize.Medium, (800, 600) }
    };

    private static readonly string[] SupportedExtensions =
        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"];

    private readonly ILogger<ImageOptimizerService> _logger;
    private readonly FolderOptions _folders;
    private readonly ProcessingOptions _processing;

    public ImageOptimizerService(
        ILogger<ImageOptimizerService> logger,
        IOptions<FolderOptions> folders,
        IOptions<ProcessingOptions> processing)
    {
        _logger = logger;
        _folders = folders.Value;
        _processing = processing.Value;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        Directory.CreateDirectory(_folders.InputPath);
        Directory.CreateDirectory(_folders.OutputPath);

        var interval = TimeSpan.FromSeconds(_processing.PollIntervalSeconds);
        _logger.LogInformation(
            "Watching {Input} every {Interval}s, writing to {Output}",
            Path.GetFullPath(_folders.InputPath), interval.TotalSeconds, Path.GetFullPath(_folders.OutputPath));

        using var timer = new PeriodicTimer(interval);
        do
        {
            ProcessPending();
        }
        while (await timer.WaitForNextTickAsync(stoppingToken));
    }

    private void ProcessPending()
    {
        var pending = Directory
            .EnumerateFiles(_folders.InputPath)
            .Where(f => SupportedExtensions.Contains(Path.GetExtension(f).ToLowerInvariant()));

        foreach (var file in pending)
        {
            var name = Path.GetFileName(file);
            var destination = Path.Combine(_folders.OutputPath, name);

            using (var source = File.OpenRead(file))
            {
                var format = Image.DetectFormat(source);

                source.Position = 0;
                using var image = Image.Load<Rgba32>(source);
                using var output = File.Create(destination);
                Resize(image, output, _processing.Size, format);
            }

            if (_processing.DeleteAfterProcessing)
            {
                File.Delete(file);
            }

            _logger.LogInformation("Resized: {Name}", name);
        }
    }

    private static void Resize(Image<Rgba32> image, Stream output, ImageSize size, IImageFormat format)
    {
        var (width, height) = Dimensions[size];
        image.Mutate(x => x.Resize(width, height));
        image.Save(output, format);
    }
}
