using System.Text;
using System.Text.RegularExpressions;
using MenuChat;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;
using Microsoft.Extensions.AI.Evaluation.Quality;

namespace MenuChat.Evals;

public sealed class MenuChatEvalTests(MenuChatFixture fixture) : IClassFixture<MenuChatFixture>
{
    private static readonly string GroundingContext = BuildGroundingContext();

    private static readonly string[] NonMenuDishKeywords =
        ["sushi", "ramen", "burger", "taco", "sashimi", "dumpling", "curry", "kebab"];

    [Fact]
    public async Task CheapestDish_MentionsFalafelAndPrice()
    {
        const string question = "What is the cheapest dish on the menu?";
        string answer = await fixture.Assistant.AskAsync(question);

        Assert.Contains("falafel", answer, StringComparison.OrdinalIgnoreCase);
        AssertContainsPrice(answer, 12);
        AssertNoPriceBelow(answer, 12);
        AssertNoNonMenuDish(answer);

        await AssertGroundedAsync(question, answer);
    }

    [Fact]
    public async Task VegetarianOption_MentionsFalafel()
    {
        const string question = "What vegetarian option do you have?";
        string answer = await fixture.Assistant.AskAsync(question);

        Assert.Contains("falafel", answer, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("schnitzel", answer, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("pad kra pao", answer, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("noodles", answer, StringComparison.OrdinalIgnoreCase);
        AssertNoNonMenuDish(answer);

        await AssertGroundedAsync(question, answer);
    }

    [Fact]
    public async Task SushiQuestion_DeclinesWithoutInventingDish()
    {
        const string question = "Do you have sushi?";
        string answer = await fixture.Assistant.AskAsync(question);

        Assert.DoesNotContain("sushi is on the menu", answer, StringComparison.OrdinalIgnoreCase);
        Assert.True(
            Regex.IsMatch(answer, @"\b(not|no|don't|do not|doesn't|does not|sorry)\b", RegexOptions.IgnoreCase),
            $"Expected a decline for a non-menu dish, got: {answer}");
        AssertNoNonMenuDish(answer, "sushi");

        await AssertGroundedAsync(question, answer);
    }

    [Fact]
    public async Task WienerSchnitzelPrice_Is18()
    {
        const string question = "How much does the Wiener Schnitzel cost?";
        string answer = await fixture.Assistant.AskAsync(question);

        Assert.Contains("schnitzel", answer, StringComparison.OrdinalIgnoreCase);
        AssertContainsPrice(answer, 18);
        AssertNoNonMenuDish(answer);

        await AssertGroundedAsync(question, answer);
    }

    [Fact]
    public async Task MostExpensiveDish_MentionsPizzaTartufoAndPrice()
    {
        const string question = "What is the most expensive dish on the menu?";
        string answer = await fixture.Assistant.AskAsync(question);

        Assert.Contains("pizza tartufo", answer, StringComparison.OrdinalIgnoreCase);
        AssertContainsPrice(answer, 24);
        AssertNoNonMenuDish(answer);

        await AssertGroundedAsync(question, answer);
    }

    private static void AssertContainsPrice(string answer, int price)
    {
        string pattern = $@"(?<![\d.,]){price}(?:[.,]\d{{1,2}})?(?!\d|[.,]\d)";
        Assert.True(Regex.IsMatch(answer, pattern), $"Expected price {price} in answer: {answer}");
    }

    private static void AssertNoPriceBelow(string answer, int minimum)
    {
        foreach (Match match in Regex.Matches(answer, @"(?<![\d.,])(\d{1,3})(?:[.,]\d{1,2})?\s*(?:EUR|€)", RegexOptions.IgnoreCase))
        {
            Assert.True(int.Parse(match.Groups[1].Value) >= minimum, $"Unexpected price below {minimum} EUR in answer: {answer}");
        }
    }

    private static void AssertNoNonMenuDish(string answer, string? askedAbout = null)
    {
        foreach (string keyword in NonMenuDishKeywords.Where(k => k != askedAbout))
        {
            Assert.DoesNotContain(keyword, answer, StringComparison.OrdinalIgnoreCase);
        }
    }

    private async Task AssertGroundedAsync(string question, string answer)
    {
        GroundednessEvaluator evaluator = new();
        List<ChatMessage> messages = [new ChatMessage(ChatRole.User, question)];
        ChatResponse response = new(new ChatMessage(ChatRole.Assistant, answer));
        GroundednessEvaluatorContext context = new(GroundingContext);

        EvaluationResult result = await evaluator.EvaluateAsync(
            messages,
            response,
            fixture.JudgeChatConfiguration,
            [context]);

        NumericMetric groundedness = result.Get<NumericMetric>(GroundednessEvaluator.GroundednessMetricName);

        Assert.False(groundedness.ContainsDiagnostics(d => d.Severity != EvaluationDiagnosticSeverity.Informational));
        Assert.True(
            groundedness.Interpretation is { Rating: EvaluationRating.Good or EvaluationRating.Exceptional },
            $"Groundedness score too low ({groundedness.Value}) for question '{question}': {answer}");
    }

    private static string BuildGroundingContext()
    {
        StringBuilder builder = new();
        foreach (MenuItem item in MenuCatalog.Items)
        {
            builder.AppendLine(MenuCatalog.FormatItem(item));
        }

        return builder.ToString();
    }
}
