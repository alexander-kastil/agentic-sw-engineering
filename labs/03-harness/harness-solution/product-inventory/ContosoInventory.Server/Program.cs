using System.Threading.RateLimiting;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.EntityFrameworkCore;
using ContosoInventory.Server.Data;
using ContosoInventory.Server.Services;

var builder = WebApplication.CreateBuilder(args);

// 1. Controllers
builder.Services.AddControllers();

// 2. Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 3. EF Core with SQLite
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? "Data Source=App_Data/ContosoInventory.db";
builder.Services.AddDbContext<InventoryContext>(options =>
    options.UseSqlite(connectionString));

// 4. Identity
builder.Services.AddIdentity<IdentityUser, IdentityRole>(options =>
{
    options.Password.RequiredLength = 8;
    options.Password.RequireUppercase = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireDigit = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;
})
.AddEntityFrameworkStores<InventoryContext>();

// 5. Cookie configuration
// PRODUCTION NOTE: This application runs on HTTP for lab simplification. For production:
//   - Enable HTTPS and update applicationUrl in launchSettings.json
//   - Change CookieSecurePolicy to CookieSecurePolicy.Always
//   - Update CORS origins to use HTTPS only
builder.Services.ConfigureApplicationCookie(options =>
{
    options.Cookie.Name = ".ContosoInventory.Auth";
    options.Cookie.HttpOnly = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.SameAsRequest;
    options.Cookie.SameSite = SameSiteMode.Strict;
    options.LoginPath = "/api/auth/login";
    options.AccessDeniedPath = "/api/auth/login";
    options.SlidingExpiration = true;
    options.ExpireTimeSpan = TimeSpan.FromMinutes(30);
    options.Events.OnRedirectToLogin = context =>
    {
        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
        return Task.CompletedTask;
    };
    options.Events.OnRedirectToAccessDenied = context =>
    {
        context.Response.StatusCode = StatusCodes.Status403Forbidden;
        return Task.CompletedTask;
    };
});

// 6. CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("https://localhost:5240", "http://localhost:5240")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });
});

// 7. Rate limiting — global limiter applies to all endpoints automatically
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(httpContext =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1),
                QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
                QueueLimit = 10
            }));
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});

// 8. Anti-forgery
// Note: For this JSON API + Blazor WASM architecture, CSRF protection is provided by:
//   1. SameSite=Strict cookies (prevents cross-site cookie attachment)
//   2. CORS policy (restricts which origins can make requests)
//   3. [ApiController] JSON model binding (rejects non-JSON Content-Type on body requests)
// Traditional antiforgery tokens are registered for defense-in-depth but are not the
// primary CSRF defense for SPA + JSON API patterns.
builder.Services.AddAntiforgery();

// 9. Application services
builder.Services.AddScoped<ICategoryService, CategoryService>();
builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();

// Middleware pipeline

// 1. Swagger (development only)
// WARNING: Swagger is exposed without authentication. In production deployments,
// remove or secure Swagger behind authentication to prevent API surface exposure.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// 2. Security headers
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("X-XSS-Protection", "0");
    context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");
    context.Response.Headers.Append("Content-Security-Policy",
        "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-eval' 'wasm-unsafe-eval'; img-src 'self' data:");
    await next();
});

// 4. Blazor & static files
app.UseBlazorFrameworkFiles();
app.UseStaticFiles();

// 6. Routing
app.UseRouting();

// 7. CORS
app.UseCors();

// 8. Rate limiter
app.UseRateLimiter();

// 9. Authentication & Authorization
app.UseAuthentication();
app.UseAuthorization();

// 10. Anti-forgery (defense-in-depth; primary CSRF protection is SameSite=Strict + CORS + JSON Content-Type)
app.UseAntiforgery();

// 11. Map controllers
app.MapControllers();

// 12. Fallback
app.MapFallbackToFile("index.html");

// Ensure App_Data directory exists
var appDataPath = Path.Combine(app.Environment.ContentRootPath, "App_Data");
Directory.CreateDirectory(appDataPath);

// Initialize database
using (var scope = app.Services.CreateScope())
{
    await DbInitializer.InitializeAsync(scope.ServiceProvider);
}

app.Run();
