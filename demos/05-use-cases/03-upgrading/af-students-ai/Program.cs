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

// Read configuration from appsettings.json
builder.Configuration.SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

// Get Azure OpenAI configuration values directly
var model = builder.Configuration["Model"] ?? throw new InvalidOperationException("Model configuration is missing");
var endpoint = builder.Configuration["Endpoint"] ?? throw new InvalidOperationException("Endpoint configuration is missing");

// Use credential chain (e.g., Azure CLI / Managed Identity); ensure az login is done locally.
var openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential());
var chatClient = openAIClient.GetChatClient(model);

// Expose StudentPlugin functions as Agent Framework tools
var studentTools = new[]
{
    AIFunctionFactory.Create(StudentPlugin.GetStudentDetails),
    AIFunctionFactory.Create(StudentPlugin.GetStudentAge),
    AIFunctionFactory.Create(StudentPlugin.GetStudentsBySchool),
    AIFunctionFactory.Create(StudentPlugin.GetSchoolWithMostOrLeastStudents),
    AIFunctionFactory.Create(StudentPlugin.GetStudentsInSchool)
};

var studentAgent = chatClient.CreateAIAgent(
    instructions: "You help answer student roster questions. Use the provided tools to fetch data rather than guessing.",
    name: "student-assistant",
    tools: studentTools);

// Register agent for DI consumption in pages (expose as AIAgent)
builder.Services.AddSingleton<AIAgent>(_ => studentAgent);

// Add services to the container.
builder.Services.AddRazorPages();

// Add Entity Framework Core with SQLite
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

// Configure the HTTP request pipeline.
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