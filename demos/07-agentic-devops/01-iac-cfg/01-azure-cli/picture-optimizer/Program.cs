using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using PictureOptimizer;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.Configure<FolderOptions>(builder.Configuration.GetSection("Folders"));
builder.Services.Configure<ProcessingOptions>(builder.Configuration.GetSection("Processing"));

builder.Services.AddHostedService<ImageOptimizerService>();

builder.Build().Run();
