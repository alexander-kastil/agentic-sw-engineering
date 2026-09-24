using System.Runtime.CompilerServices;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

namespace MenuChat;

public sealed class CopilotChatClient(CopilotClient client, string model) : IChatClient
{
    private static readonly string IsolatedConfigDirectory = Directory.CreateDirectory(
        Path.Combine(Path.GetTempPath(), "menu-chat-copilot")).FullName;

    public async Task<ChatResponse> GetResponseAsync(
        IEnumerable<ChatMessage> messages,
        ChatOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        List<ChatMessage> messageList = [.. messages];
        string? systemPrompt = messageList.FirstOrDefault(m => m.Role == ChatRole.System)?.Text;
        string userPrompt = string.Join(
            Environment.NewLine,
            messageList.Where(m => m.Role != ChatRole.System).Select(m => m.Text));

        SessionConfig config = new()
        {
            Model = model,
            ConfigDirectory = IsolatedConfigDirectory,
            DisabledMcpServers = ["github-mcp-server"],
            EnableSkills = false,
            ExcludedTools = new ToolSet().AddBuiltIn("*"),
            SystemMessage = string.IsNullOrEmpty(systemPrompt)
                ? null
                : new SystemMessageConfig { Mode = SystemMessageMode.Replace, Content = systemPrompt },
        };

        await using CopilotSession session = await client.CreateSessionAsync(config, cancellationToken).ConfigureAwait(false);

        AssistantMessageEvent? assistantEvent = await session.SendAndWaitAsync(
            new MessageOptions { Prompt = userPrompt },
            timeout: null,
            cancellationToken: cancellationToken).ConfigureAwait(false);

        return new ChatResponse(new ChatMessage(ChatRole.Assistant, assistantEvent?.Data?.Content ?? string.Empty)) { ModelId = model };
    }

    public async IAsyncEnumerable<ChatResponseUpdate> GetStreamingResponseAsync(
        IEnumerable<ChatMessage> messages,
        ChatOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        ChatResponse response = await GetResponseAsync(messages, options, cancellationToken).ConfigureAwait(false);
        foreach (ChatResponseUpdate update in response.ToChatResponseUpdates())
        {
            yield return update;
        }
    }

    public object? GetService(Type serviceType, object? serviceKey = null) =>
        serviceKey is null && serviceType.IsInstanceOfType(this) ? this : null;

    public void Dispose()
    {
    }
}
