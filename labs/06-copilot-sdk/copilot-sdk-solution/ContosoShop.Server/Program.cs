using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;
using AspNetCoreRateLimit;
using ContosoShop.Server.Data;
using ContosoShop.Server.Services;
using ContosoShop.Shared.Models;
using System.Text.Json.Serialization;
using GitHub.Copilot;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        // Handle circular references in entity navigation properties
        options.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
    });
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure Entity Framework Core with SQLite
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<ContosoContext>(options =>
    options.UseSqlite(connectionString));

// Configure ASP.NET Core Identity (T015s-T018s)
builder.Services.AddIdentity<User, IdentityRole<int>>(options =>
{
    // Password requirements (T017s)
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequiredLength = 8;
    options.Password.RequireNonAlphanumeric = true;
    
    // Lockout settings
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;
    
    // User settings
    options.User.RequireUniqueEmail = true;
})
.AddEntityFrameworkStores<ContosoContext>()
.AddDefaultTokenProviders();

// Configure Authentication with Cookies (T016s, T018s)
builder.Services.ConfigureApplicationCookie(options =>
{
    options.Cookie.HttpOnly = true;
    // SameAsRequest: secure in production (HTTPS), allows HTTP in development
    options.Cookie.SecurePolicy = CookieSecurePolicy.SameAsRequest;
    options.Cookie.SameSite = SameSiteMode.Strict;
    options.ExpireTimeSpan = TimeSpan.FromMinutes(30); // Session timeout (T018s)
    options.SlidingExpiration = true;
    options.LoginPath = "/login";
    options.LogoutPath = "/api/auth/logout";
});

// Configure Rate Limiting (T019s-T020s)
builder.Services.AddMemoryCache();
builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting"));
builder.Services.AddInMemoryRateLimiting();
builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();

// Configure Anti-forgery (CSRF) protection (T021s)
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN";
    options.Cookie.HttpOnly = true;
    // SameAsRequest: secure in production (HTTPS), allows HTTP in development
    options.Cookie.SecurePolicy = CookieSecurePolicy.SameAsRequest;
    options.Cookie.SameSite = SameSiteMode.Strict;
});

// Register email service
builder.Services.AddScoped<IEmailService, EmailServiceDev>();

// Register inventory management service
builder.Services.AddScoped<IInventoryService, InventoryService>();

// Register order business logic service
builder.Services.AddScoped<IOrderService, OrderService>();

// Register AI agent tools service
builder.Services.AddScoped<SupportAgentTools>();

// Register GitHub Copilot SDK client as a singleton
builder.Services.AddSingleton<CopilotClient>(sp =>
{
    var logger = sp.GetRequiredService<ILogger<CopilotClient>>();
    return new CopilotClient(new CopilotClientOptions
    {
        Logger = logger,
        LogLevel = CopilotLogLevel.Info
    });
});

// Configure CORS with explicit whitelist (T024s - Security hardened)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowBlazorClient", policy =>
    {
        policy.WithOrigins("https://localhost:7202", "http://localhost:5266") // Explicit whitelist for actual server ports
              .WithMethods("GET", "POST") // Only required methods
              .WithHeaders("Content-Type", "Authorization", "X-CSRF-TOKEN") // Only required headers
              .AllowCredentials(); // Allow credentials for authentication
    });
});

var app = builder.Build();

// Ensure CopilotClient is started
var copilotClient = app.Services.GetRequiredService<CopilotClient>();
await copilotClient.StartAsync();

// Initialize database with sample data
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var context = services.GetRequiredService<ContosoContext>();
        var userManager = services.GetRequiredService<UserManager<User>>();
        await DbInitializer.InitializeAsync(context, userManager);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "An error occurred while seeding the database.");
    }
}

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
    app.UseWebAssemblyDebugging();
}
else
{
    app.UseExceptionHandler("/Error");
    // HSTS configuration (T023s)
    app.UseHsts();
}

// Security headers middleware (T022s)
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");
    await next();
});

app.UseHttpsRedirection();
app.UseBlazorFrameworkFiles();
app.UseStaticFiles();

app.UseRouting();

// Rate limiting middleware
app.UseIpRateLimiting();

app.UseCors("AllowBlazorClient");

// Authentication and Authorization middleware
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapFallbackToFile("index.html");

app.Run();

// Make the Program class accessible to integration tests
public partial class Program { }
