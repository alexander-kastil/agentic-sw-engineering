using GitHub.Copilot;
using MenuChat;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;

namespace MenuChat.Evals;

public sealed class MenuChatFixture : IAsyncLifetime
{
    private readonly CopilotClient client = new();

    public MenuAssistant Assistant { get; private set; } = null!;

    public ChatConfiguration JudgeChatConfiguration { get; private set; } = null!;

    public Task InitializeAsync()
    {
        string chatModel = Environment.GetEnvironmentVariable("CHAT_MODEL") ?? "gpt-5-mini";
        string judgeModel = Environment.GetEnvironmentVariable("JUDGE_MODEL") ?? "gpt-5";

        Assistant = new MenuAssistant(new CopilotChatClient(client, chatModel));
        JudgeChatConfiguration = new ChatConfiguration(new CopilotChatClient(client, judgeModel));

        return Task.CompletedTask;
    }

    public async Task DisposeAsync() => await client.DisposeAsync();
}
