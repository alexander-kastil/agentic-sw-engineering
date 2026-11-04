using System.Net.Http.Json;
using ContosoShop.Shared.Models;

namespace ContosoShop.Client.Services;

/// <summary>
/// Client-side service for communicating with the AI support agent API.
/// </summary>
public class SupportAgentService
{
    private readonly HttpClient _http;

    public SupportAgentService(HttpClient http)
    {
        _http = http;
    }

    /// <summary>
    /// Sends a question to the AI support agent and returns the response.
    /// </summary>
    /// <param name="question">The user's question</param>
    /// <returns>The agent's response text</returns>
    public async Task<string> AskAsync(string question)
    {
        var query = new SupportQuery { Question = question };

        var response = await _http.PostAsJsonAsync("api/supportagent/ask", query);

        if (!response.IsSuccessStatusCode)
        {
            var errorText = await response.Content.ReadAsStringAsync();
            throw new HttpRequestException(
                $"Support agent returned {response.StatusCode}: {errorText}");
        }

        var result = await response.Content.ReadFromJsonAsync<SupportResponse>();
        return result?.Answer ?? "I'm sorry, I didn't receive a response. Please try again.";
    }
}
