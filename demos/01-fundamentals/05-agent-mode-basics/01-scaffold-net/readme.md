# Scaffold a .NET Instructions API with Scalar UI

A single prompt drives a local agent from project scaffolding through refactoring, API documentation, build validation, and browser-based verification of the running .NET service.

```text
Navigate to src/ and execute: dotnet new webapi -n copilot-api
Navigate to src/copilot-api and execute: dotnet new .gitignore
In src/copilot-api i want you to apply my coding conventions for .NET and then remove all weather (controller) related data. 
Next implement a InstructionsController with model name, description as a standalone controller and register it. 
Use Microsoft Learn MCP for planning.
Provide Scalar UI in the root. 
Build run and fix all errors. while keeping the .NET app running use your Chrome Dev Tools MCP visit the HTTP URL 
and port it is configured to run on an check the result. no need to use HTTPS
```