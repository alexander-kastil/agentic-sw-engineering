using System.ComponentModel;
using GitHub.Copilot;
using Microsoft.Extensions.AI;

var analyzeCode = CopilotTool.DefineTool(
    ([Description("The code snippet to analyze")] string code) =>
    {
        var issues = new List<string>();

        if (code.Contains("eval("))
        {
            issues.Add("Dangerous eval() detected");
        }
        if (code.Contains("innerHTML"))
        {
            issues.Add("Potential XSS via innerHTML");
        }
        if (System.Text.RegularExpressions.Regex.IsMatch(code, @"\bpassword\b.*=.*['""][^'""]*['""]", System.Text.RegularExpressions.RegexOptions.IgnoreCase))
        {
            issues.Add("Hardcoded secret/password detected");
        }
        if (!code.Contains("try") && code.Contains("fetch"))
        {
            issues.Add("Unhandled Promise in fetch");
        }

        var severity = issues.Count > 2 ? "high" : issues.Count > 0 ? "medium" : "low";

        return new
        {
            issues = issues.Count > 0 ? issues : new List<string> { "No major issues detected" },
            severity,
            timestamp = DateTimeOffset.UtcNow.ToString("O"),
        };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "analyze_security",
        Description = "Analyze code for common security vulnerabilities",
    });

var readCodeFile = CopilotTool.DefineTool(
    ([Description("The filename to read")] string filename) =>
    {
        const string sampleCode = """

              const password = "admin123";
              fetch('/api/data').then(r => r.json())
                .then(data => document.getElementById('container').innerHTML = data);

            """;

        return new { filename, content = sampleCode };
    },
    toolOptions: new CopilotToolOptions { SkipPermission = true },
    factoryOptions: new AIFunctionFactoryOptions
    {
        Name = "read_code_file",
        Description = "Read a code file to analyze",
    });

try
{
    await using var client = new CopilotClient();
    await using var session = await client.CreateSessionAsync(new SessionConfig
    {
        Model = "gpt-5-mini",
        Streaming = true,
        Tools = [analyzeCode, readCodeFile],
        AvailableTools = new ToolSet().AddCustom("*"),
        SystemMessage = new SystemMessageConfig
        {
            Mode = SystemMessageMode.Append,
            Content = "You are a security-focused code reviewer. Be thorough and specific in your analysis.",
        },
    });

    session.On<SessionEvent>(evt =>
    {
        if (evt is AssistantMessageDeltaEvent delta)
        {
            Console.Write(delta.Data.DeltaContent);
        }
        if (evt is SessionIdleEvent)
        {
            Console.WriteLine("\n");
        }
    });

    await session.SendAndWaitAsync(new MessageOptions
    {
        Prompt = "Read the code file 'app.js' and analyze it for security vulnerabilities.",
    });
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error: {ex.Message}");
    Environment.Exit(1);
}
