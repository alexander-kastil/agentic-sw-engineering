using Microsoft.Extensions.Configuration;

IConfiguration configuration = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .Build();

var model = configuration["Model"];
var endpoint = configuration["ProjectEndpoint"];
ChatRunner runner = new ChatRunner();
runner.Run(model, endpoint);