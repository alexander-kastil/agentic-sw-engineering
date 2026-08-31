---
name: scaffold-app
description: Describe when to use this prompt
---

Navigate to src/ and execute: dotnet new webapi -n copilot-api
Navigate to src/copilot-api and execute: dotnet new .gitignore
In src/copilot-api i want you to apply my coding conventions for .net and then remove all weather (controller) related data. next implement a InstructionsController with model name, description as a standalone controller and register it. Use microsoft learn mcp for planning.
Provide scalar ui in the root. 
Build run and fix all errors. while keeping the dotnet app running use your chrome dev tools mcp visit the http url and port it is configured to run on an check the result. no need to use https