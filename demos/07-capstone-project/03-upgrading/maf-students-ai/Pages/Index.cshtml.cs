using Microsoft.Agents.AI;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace SKFunctionCalling;

public class IndexModel(AIAgent studentAgent) : PageModel
{

  private readonly AIAgent _studentAgent = studentAgent;

  [BindProperty]
  public string? Reply { get; set; }

  public void OnGet() { }
  // action method that receives prompt from the form
  public async Task<IActionResult> OnPostAsync(string prompt)
  {
    // call the Azure Function
    var response = await CallFunction(prompt);
    Reply = response;
    return Page();
  }

  private async Task<string> CallFunction(string question)
  {
    var response = await _studentAgent.RunAsync(question);
    return response.Text ?? string.Empty;
  }
}