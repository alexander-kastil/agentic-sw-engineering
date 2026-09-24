FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY deploy-azure-solution-cs.csproj ./
RUN dotnet restore -r linux-x64

COPY Program.cs ./
RUN dotnet publish -c Release -r linux-x64 --self-contained false -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/publish .

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl --fail http://127.0.0.1:${PORT}/health || exit 1

ENTRYPOINT ["dotnet", "deploy-azure-solution-cs.dll"]
