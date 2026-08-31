namespace PictureOptimizer;

public class FolderOptions
{
    public string InputPath { get; set; } = "drop";
    public string OutputPath { get; set; } = "processed";
}

public class ProcessingOptions
{
    public int PollIntervalSeconds { get; set; } = 5;
    public ImageSize Size { get; set; } = ImageSize.ExtraSmall;
    public bool DeleteAfterProcessing { get; set; } = true;
}

public enum ImageSize
{
    ExtraSmall,
    Small,
    Medium
}
