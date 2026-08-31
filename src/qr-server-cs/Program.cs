using ModelContextProtocol.Server;

if (args.Contains("--stdio"))
{
	var hostBuilder = Host.CreateApplicationBuilder(args);
	hostBuilder.Services.AddMcpServer()
		.WithStdioServerTransport()
		.WithToolsFromAssembly();

	using var host = hostBuilder.Build();
	host.Run();
	return;
}

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMcpServer()
	.WithHttpTransport()
	.WithToolsFromAssembly();

builder.Services.AddCors(options =>
{
	options.AddDefaultPolicy(policy =>
	{
		policy.AllowAnyOrigin()
			.AllowAnyMethod()
			.AllowAnyHeader();
	});
});

var app = builder.Build();

var portValue = Environment.GetEnvironmentVariable("PORT");
var port = int.TryParse(portValue, out var parsedPort) ? parsedPort : 3001;

app.UseRouting();
app.UseCors();
app.MapMcp();
app.Run($"http://0.0.0.0:{port}");
