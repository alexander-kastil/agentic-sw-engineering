using System.Linq;
using FoodApp;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace FoodApp.Tests
{
    public sealed class CatalogApiFactory : WebApplicationFactory<Program>
    {
        private readonly SqliteConnection connection = new("DataSource=:memory:");

        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            connection.Open();

            builder.ConfigureServices(services =>
            {
                services.RemoveAll<DbContextOptions<FoodDBContext>>();
                services.AddDbContext<FoodDBContext>(options => options.UseSqlite(connection));
            });
        }

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);
            if (disposing)
            {
                connection.Dispose();
            }
        }
    }
}
