# Use the official .NET 9 runtime image as the base image for the final stage
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

# Use the official .NET 9 SDK image for building the application
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy the project file and restore dependencies
COPY ["hr-mcp-server.csproj", "."]
RUN dotnet restore "hr-mcp-server.csproj"

# Copy the entire source code
COPY . .

# Build the application in Release mode
RUN dotnet build "hr-mcp-server.csproj" -c Release -o /app/build

# Publish the application
FROM build AS publish
RUN dotnet publish "hr-mcp-server.csproj" -c Release -o /app/publish

# Final stage - create the runtime image
FROM base AS final
WORKDIR /app

# Copy the published application from the publish stage
COPY --from=publish /app/publish .

# Create the Data directory and copy the employees data
RUN mkdir -p /app/Data
COPY --from=publish /app/publish/Data/ /app/Data/

# Set environment variables for production
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:80

# Define the entry point for the container
ENTRYPOINT ["dotnet", "hr-mcp-server.dll"]
