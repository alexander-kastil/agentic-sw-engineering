using System.ComponentModel.DataAnnotations;

namespace ContosoShop.Shared.Models;

/// <summary>
/// Represents a support question submitted by the user to the AI agent.
/// </summary>
public class SupportQuery
{
    /// <summary>
    /// The user's question or message for the AI support agent.
    /// </summary>
    [Required]
    [StringLength(1000, MinimumLength = 1)]
    public string Question { get; set; } = string.Empty;
}

/// <summary>
/// Represents the AI agent's response to a support query.
/// </summary>
public class SupportResponse
{
    /// <summary>
    /// The AI agent's answer to the user's question.
    /// </summary>
    public string Answer { get; set; } = string.Empty;
}
