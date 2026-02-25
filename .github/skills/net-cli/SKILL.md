---
name: net-cli
description: Master .NET CLI commands for project management. Use when building, testing, running projects, managing NuGet packages, formatting code, configuring solutions, using hot reload with watch mode, or troubleshooting build issues. Covers dotnet build, dotnet test, dotnet run, dotnet format, package management, and solution organization with proper SDK setup.
---

# .NET CLI

Work efficiently with the .NET CLI to manage projects, packages, builds, tests, and development workflows across .NET Core, .NET Framework, and modern .NET SDK projects.

## When to Use This Skill

Use this skill when you need to:

- Build and compile .NET projects and solutions
- Run applications with hot reload and watch mode
- Execute unit and integration tests with filtering
- Manage NuGet packages and dependencies
- Format and lint C# code
- Organize multi-project solutions
- Configure build properties and target frameworks
- Debug build failures and dependency issues
- Clean and restore project artifacts
- Publish applications to different targets

## Prerequisites

Ensure your environment has:

- .NET SDK 8.0 or higher (download from dotnet.microsoft.com)
- Project files (\*.csproj) in SDK-style format (Microsoft.NET.Sdk)
- NuGet feeds configured in NuGet.Config (if using custom sources)
- Directory.Build.props for shared build properties (optional but recommended)
- Sufficient permissions to modify project files and create directories

## Core Concepts

### Project File Structure

Modern .NET projects use SDK-style format with simplified config:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <LangVersion>latest</LangVersion>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="PackageName" Version="1.0.0" />
    <ProjectReference Include="../Other.csproj" />
  </ItemGroup>
</Project>
```

### NuGet Configuration

NuGet feeds are defined in NuGet.Config at solution root or user level:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="nuget" value="https://api.nuget.org/v3/index.json" />
    <add key="internal" value="https://your-internal-feed" />
  </packageSources>
  <packageSourceCredentials>
    <internal>
      <add key="Username" value="user@example.com" />
      <add key="ClearTextPassword" value="token" />
    </internal>
  </packageSourceCredentials>
</configuration>
```

Do not add new NuGet sources unless explicitly required.

### Directory.Build.props

Shared properties applied to all projects in solution subtree:

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Logging" Version="8.0.0" />
  </ItemGroup>
</Project>
```

Keep Directory.Build.props consistent across solution; changes affect all projects.

## Common Commands

### Restore and Build

```bash
# Restore NuGet packages
dotnet restore

# Build solution (Debug configuration)
dotnet build

# Build specific project
dotnet build src/MyProject/MyProject.csproj

# Release build with optimization
dotnet build -c Release

# Verbose build output for debugging
dotnet build -v detailed

# Clean and rebuild
dotnet clean && dotnet build
```

### Running Applications

```bash
# Run default startup project
dotnet run

# Run specific project
dotnet run --project src/MyProject

# With environment variable
ASPNETCORE_ENVIRONMENT=Development dotnet run --project src/MyWeb

# Pass arguments to application
dotnet run --project src/MyApp -- --option value

# Hot reload with watch mode (ASP.NET Core, Blazor, MAUI)
dotnet watch run --project src/MyWeb

# Watch mode for tests
dotnet watch test
```

### Testing

```bash
# Run all tests
dotnet test

# Run tests with detailed output
dotnet test --verbosity detailed

# Filter by test name (FullyQualifiedName)
dotnet test --filter "FullyQualifiedName~CanCreateUser"

# Filter by class name
dotnet test --filter "ClassName~UserServiceTests"

# Filter by category/trait
dotnet test --filter "Category=Integration"

# Run specific test project
dotnet test src/MyProject.Tests/MyProject.Tests.csproj

# Generate coverage report
dotnet test /p:CollectCoverage=true /p:CoverletOutput=../coverage/
```

### Package Management

```bash
# Add package to project
dotnet add package Newtonsoft.Json

# Add specific version
dotnet add package Newtonsoft.Json --version 13.0.1

# Add to specific project
dotnet add src/MyProject package EntityFrameworkCore

# Remove package
dotnet remove package OldPackage

# List all package references
dotnet list package

# Check for outdated packages
dotnet list package --outdated

# Update packages to latest
dotnet package update

# Update to specific version
dotnet package update PackageName --version 2.0.0
```

### Code Formatting and Quality

```bash
# Format all C# files in solution
dotnet format

# Format specific project
dotnet format --project src/MyProject

# Verify formatting without making changes
dotnet format --verify-no-changes

# Format and report issues
dotnet format --verbosity diagnostic
```

### Solution and Project Management

```bash
# List all projects in solution
dotnet sln list

# Add project to solution
dotnet sln add src/NewProject/NewProject.csproj

# Remove project from solution
dotnet sln remove src/OldProject/OldProject.csproj

# Build only specific project (without dependencies)
dotnet build src/MyProject/MyProject.csproj --no-restore
```

### Publishing and Output

```bash
# Publish for deployment (Release configuration)
dotnet publish -c Release --output ./publish

# Publish as self-contained executable
dotnet publish -c Release --self-contained

# Publish to specific platform
dotnet publish -c Release -r win-x64

# Publish without restoration
dotnet publish -c Release --no-restore --no-build
```

## Architectural Best Practices

### Project Organization

- src/: All source projects
- tests/: All test projects (unit, integration, e2e)
- Directory.Build.props at solution root for shared settings
- Each logical component in separate project
- Clear naming: MyProject.Core, MyProject.Web, MyProject.Tests

### Build Configuration

- Debug: Default, includes symbols, slower
- Release: Optimized, no symbols, faster

Use configuration-specific packaging:

```xml
<PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|AnyCPU'">
  <DebugSymbols>true</DebugSymbols>
  <DebugType>full</DebugType>
</PropertyGroup>
```

### Dependency Management

- Keep transitive dependencies to minimum
- Review outdated packages regularly with dotnet list package --outdated
- Test after upgrading major versions
- Use PackageReference (not packages.config)
- Lock files (\*.lock.json) for reproducible builds

### NuGet Feed Best Practices

- Configure all necessary feeds before build
- Do not commit credentials to version control
- Use local NuGet.Config in root (added to .gitignore)
- Use nuget locals all --clear if encountering stale cache issues

## Troubleshooting

| Issue                               | Solution                                                                                                                                     |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Package not found                   | Verify NuGet feeds in NuGet.Config; run dotnet restore; check package spelling and version                                                   |
| Build fails with namespace errors   | Ensure all projects are in solution; add ProjectReference; run dotnet build --verbosity detailed                                             |
| Tests not discovered                | Verify test project references Microsoft.NET.Test.Sdk; check test class/method names match conventions; run dotnet test --verbosity detailed |
| Port already in use                 | Change port with dotnet run --launch-profile profilename or kill process on port                                                             |
| Hot reload not working              | Verify dotnet watch is installed; use supported framework (net6.0+); check for compilation errors                                            |
| NuGet restore timeout               | Increase timeout with --no-cache or check network/feed availability                                                                          |
| Inconsistent builds across machines | Check Directory.Build.props for hardcoded paths; ensure same SDK version; validate NuGet.Config                                              |
| Symbol/source issues                | Verify --configuration is Release for published apps; ensure .pdb files included; check debug paths                                          |

## Cleanup and Maintenance

### Clear NuGet Cache

When encountering persistent NuGet errors:

```bash
# Clear all NuGet caches
dotnet nuget locals all --clear

# Clear specific cache type
dotnet nuget locals global-packages --clear
dotnet nuget locals http-cache --clear
dotnet nuget locals temp --clear

# List cache locations
dotnet nuget locals all --list
```

### Clean Solution

```bash
# Remove build artifacts from current directory
dotnet clean

# Remove from specific project
dotnet clean src/MyProject

# Remove with verbose output
dotnet clean --verbosity detailed
```

## Common Workflows

### Daily Development

```bash
# Start dev session with hot reload
dotnet watch run --project src/MyWeb

# In separate terminal, run tests with watch
dotnet watch test --project src/MyProject.Tests

# Commit-time checks
dotnet format --verify-no-changes
dotnet build -c Release
dotnet test
```

### CI/CD Pipeline

```bash
# Restore all packages
dotnet restore

# Build in Release mode
dotnet build -c Release --no-restore

# Run all tests
dotnet test -c Release --no-build --verbosity minimal

# Publish application
dotnet publish -c Release --no-restore --no-build --output ./articles
```

### Debugging Dependency Issues

```bash
# Verbose restore
dotnet restore --verbosity detailed

# Show dependency tree
dotnet list package --include-transitive

# Find outdated packages
dotnet list package --outdated

# Clean and restore from scratch
dotnet clean && dotnet nuget locals all --clear && dotnet restore
```

## References

- Microsoft Learn: .NET CLI documentation
- NuGet CLI reference
- Entity Framework Core CLI tools
- .NET SDK release notes
- MSBuild property reference
