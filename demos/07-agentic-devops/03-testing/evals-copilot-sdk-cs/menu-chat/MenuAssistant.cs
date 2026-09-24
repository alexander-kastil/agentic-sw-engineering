using Microsoft.Extensions.AI;

namespace MenuChat;

public sealed class MenuAssistant(IChatClient chatClient)
{
    private static readonly string SystemPrompt = MenuCatalog.BuildSystemPrompt();

    public async Task<string> AskAsync(string question)
    {
        List<ChatMessage> messages =
        [
            new ChatMessage(ChatRole.System, SystemPrompt),
            new ChatMessage(ChatRole.User, question)
        ];

        ChatResponse response = await chatClient.GetResponseAsync(messages).ConfigureAwait(false);
        return response.Text;
    }
}
