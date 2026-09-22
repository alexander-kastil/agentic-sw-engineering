FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY picture-optimizer.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app

FROM mcr.microsoft.com/dotnet/runtime:10.0
WORKDIR /app
COPY --from=build /app .

ENV Folders__InputPath=/data/drop
ENV Folders__OutputPath=/data/processed
VOLUME ["/data"]

ENTRYPOINT ["dotnet", "picture-optimizer.dll"]
