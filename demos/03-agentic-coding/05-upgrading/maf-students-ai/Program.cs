using Azure;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.OpenAI;
using Microsoft.Extensions.AI;
using Microsoft.EntityFrameworkCore;
using OpenAI.Chat;
using SKFunctionCalling;
using Azure.Identity;

var builder = WebApplication.CreateBuilder(args);

builder.Configuration.SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

var model = builder.Configuration["Model"] ?? "gpt-4o";
var endpoint = builder.Configuration["Endpoint"]
    ?? throw new InvalidOperationException("Endpoint configuration is missing");

builder.Services.AddLogging(logging =>
{
    logging.SetMinimumLevel(LogLevel.Information);
    logging.AddConsole();
});

var openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential());
var chatClient = openAIClient.GetChatClient(model);

var studentTools = new[]
{
    AIFunctionFactory.Create(StudentTools.GetStudentDetails),
    AIFunctionFactory.Create(StudentTools.GetStudentAge),
    AIFunctionFactory.Create(StudentTools.GetStudentsBySchool),
    AIFunctionFactory.Create(StudentTools.GetSchoolWithMostOrLeastStudents),
    AIFunctionFactory.Create(StudentTools.GetStudentsInSchool)
};

var studentAgent = chatClient.AsAIAgent(
    instructions: "You help answer student roster questions. Use the provided tools to fetch data rather than guessing.",
    name: "student-assistant",
    tools: studentTools);

builder.Services.AddSingleton<AIAgent>(_ => studentAgent);
builder.Services.AddRazorPages();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}

app.UseRouting();
app.UseAuthorization();
app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();