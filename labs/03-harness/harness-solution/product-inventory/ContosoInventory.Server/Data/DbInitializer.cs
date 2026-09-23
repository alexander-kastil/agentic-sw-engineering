using System.Security.Claims;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using ContosoInventory.Server.Models;

namespace ContosoInventory.Server.Data;

/// <summary>
/// Initializes the database schema by applying hand-written SQL delta scripts and seeds baseline data.
/// </summary>
public static class DbInitializer
{
    /// <summary>
    /// Applies every pending SQL delta script, then seeds identity roles, users, and categories.
    /// </summary>
    /// <param name="serviceProvider">The scoped service provider used to resolve required services.</param>
    public static async Task InitializeAsync(IServiceProvider serviceProvider)
    {
        var context = serviceProvider.GetRequiredService<InventoryContext>();
        var environment = serviceProvider.GetRequiredService<IHostEnvironment>();
        var userManager = serviceProvider.GetRequiredService<UserManager<IdentityUser>>();
        var roleManager = serviceProvider.GetRequiredService<RoleManager<IdentityRole>>();
        var logger = serviceProvider.GetRequiredService<ILogger<InventoryContext>>();

        await ApplyDeltaScriptsAsync(context, environment, logger).ConfigureAwait(false);

        // Create roles
        string[] roles = { "Admin", "Viewer" };
        foreach (var role in roles)
        {
            if (!await roleManager.RoleExistsAsync(role))
            {
                await roleManager.CreateAsync(new IdentityRole(role));
            }
        }
        logger.LogInformation("Roles created: {Roles}.", string.Join(", ", roles));

        // Seed users
        await SeedUserAsync(userManager, "mateo@contoso.com", "Mateo Gomez", "Password123!", "Admin", logger);
        await SeedUserAsync(userManager, "megan@contoso.com", "Megan Bowen", "Password123!", "Viewer", logger);

        // Seed categories
        if (!await context.Categories.AnyAsync())
        {
            var categories = new List<Category>
            {
                new Category
                {
                    Name = "Laptops & Desktops",
                    Description = "Portable and desktop computing devices for employee workstations",
                    DisplayOrder = 1,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Monitors & Displays",
                    Description = "Screens, monitors, and display equipment for workstations",
                    DisplayOrder = 2,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Networking Equipment",
                    Description = "Routers, switches, access points, and network cables",
                    DisplayOrder = 3,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Peripherals",
                    Description = "Keyboards, mice, webcams, headsets, and other accessories",
                    DisplayOrder = 4,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Software Licenses",
                    Description = "Operating system, productivity, and developer tool licenses",
                    DisplayOrder = 5,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Printers & Scanners",
                    Description = "Printing, scanning, and imaging devices",
                    DisplayOrder = 6,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Storage Devices",
                    Description = "External hard drives, USB drives, and NAS devices",
                    DisplayOrder = 7,
                    IsActive = true,
                    CreatedDate = new DateTime(2025, 1, 15, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 6, 1, 0, 0, 0, DateTimeKind.Utc)
                },
                new Category
                {
                    Name = "Decommissioned",
                    Description = "Retired equipment pending disposal or recycling",
                    DisplayOrder = 8,
                    IsActive = false,
                    CreatedDate = new DateTime(2024, 3, 20, 0, 0, 0, DateTimeKind.Utc),
                    LastModifiedDate = new DateTime(2025, 9, 15, 0, 0, 0, DateTimeKind.Utc)
                }
            };

            context.Categories.AddRange(categories);
            await context.SaveChangesAsync();
            logger.LogInformation("Categories seeded: {Count} categories.", categories.Count);
        }
    }

    /// <summary>
    /// Applies every <c>*.sql</c> delta script found under <c>db/deltas</c>, in file-name order.
    /// </summary>
    /// <param name="context">The database context used to execute the scripts.</param>
    /// <param name="environment">The hosting environment used to resolve the content root.</param>
    /// <param name="logger">The logger used to record progress.</param>
    private static async Task ApplyDeltaScriptsAsync(InventoryContext context, IHostEnvironment environment, ILogger logger)
    {
        var deltasPath = Path.Combine(environment.ContentRootPath, "..", "db", "deltas");

        if (!Directory.Exists(deltasPath))
        {
            logger.LogWarning("Delta scripts folder not found at {DeltasPath}.", deltasPath);
            return;
        }

        var scriptFiles = Directory.GetFiles(deltasPath, "*.sql")
            .OrderBy(filePath => Path.GetFileName(filePath), StringComparer.Ordinal)
            .ToList();

        foreach (var scriptFile in scriptFiles)
        {
            var sql = await File.ReadAllTextAsync(scriptFile).ConfigureAwait(false);
            await context.Database.ExecuteSqlRawAsync(sql).ConfigureAwait(false);
            logger.LogInformation("Applied delta script {ScriptFile}.", Path.GetFileName(scriptFile));
        }

        logger.LogInformation("Database schema up to date. Applied {Count} delta script(s).", scriptFiles.Count);
    }

    private static async Task SeedUserAsync(
        UserManager<IdentityUser> userManager,
        string email,
        string displayName,
        string password,
        string role,
        ILogger logger)
    {
        if (await userManager.FindByEmailAsync(email) == null)
        {
            var user = new IdentityUser
            {
                UserName = email,
                Email = email,
                EmailConfirmed = true
            };

            var result = await userManager.CreateAsync(user, password);
            if (result.Succeeded)
            {
                await userManager.AddToRoleAsync(user, role);
                await userManager.AddClaimAsync(user, new Claim("DisplayName", displayName));
                logger.LogInformation("Users seeded: {Email} ({Role}).", email, role);
            }
            else
            {
                logger.LogError("Failed to create user {Email}: {Errors}",
                    email, string.Join(", ", result.Errors.Select(e => e.Description)));
            }
        }
    }
}
