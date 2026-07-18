using GitHub.Copilot.SDK;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var model = config["model"] ?? "gpt-5-mini";
var prompt = config["prompt"] ?? "What are the use cases for Copilot SDK?";

Console.WriteLine($"Model: {model}");
Console.WriteLine($"Prompt: {prompt}");
Console.WriteLine(new string('-', 60));

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig { Model = model });

var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = prompt });

if (response?.Data?.Content != null)
{
    Console.WriteLine("\nResponse:");
    Console.WriteLine(response.Data.Content);
}
else
{
    Console.WriteLine("No response received.");
}
