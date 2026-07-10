FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS base
WORKDIR /app
EXPOSE 3001

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

COPY ["qr-server-cs.csproj", "."]
RUN dotnet restore "qr-server-cs.csproj"

COPY . .

RUN dotnet build "qr-server-cs.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "qr-server-cs.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app

COPY --from=publish /app/publish .

ENV ASPNETCORE_ENVIRONMENT=Production
ENV PORT=3001

ENTRYPOINT ["dotnet", "qr-server-cs.dll"]