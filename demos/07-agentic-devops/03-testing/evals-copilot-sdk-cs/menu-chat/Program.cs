using GitHub.Copilot;
using MenuChat;
using Microsoft.Extensions.AI;

string model = Environment.GetEnvironmentVariable("CHAT_MODEL") ?? "gpt-5-mini";
await using CopilotClient copilot = new();
IChatClient chatClient = new CopilotChatClient(copilot, model);
MenuAssistant assistant = new(chatClient);

if (args.Length > 0)
{
    string question = string.Join(' ', args);
    string answer = await assistant.AskAsync(question).ConfigureAwait(false);
    Console.WriteLine(answer);
}
else
{
    Console.WriteLine($"Menu chat assistant ({model}). Type a question, or press Enter on an empty line to exit.");
    while (true)
    {
        Console.Write("> ");
        string? question = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(question))
        {
            break;
        }

        string answer = await assistant.AskAsync(question).ConfigureAwait(false);
        Console.WriteLine(answer);
    }
}
