---
description: This file describes the conventions for Azure Functions projects in this repository
---

1. Consult Microsoft Learn MCP FIRST - before ANY action
   - Research latest Azure Functions setup best practices for your language/runtime
   - Understand the proper project structure and required dependencies
   - Identify the correct Azure Functions Core Tools commands for your programming language
   - Always use the latest recommended runtime versions
2. Create a detailed plan based on what you learned
   - Document the exact setup steps in their correct order
   - Identify which Azure Functions Core Tools commands are needed (func init, func new, etc.)
   - Plan parameters and configuration choices in advance
   - Never ask for parameters during execution - the plan should be clear on what to use and when
   - If unsure about parameters, research more until certain before executing
3. Execute the plan using terminal commands
   - Use the Azure Functions Core Tools scaffolding commands (not manual file creation)
   - Follow the tool's configuration and setup process
   - Use terminal commands to install dependencies and build
   - Let the tooling handle project structure and file generation
   - Always use visible terminal commands - never run commands in the background
   - After scaffolding, unless specified otherwise, add "AzureWebJobsStorage": "UseDevelopmentStorage=true" to local.settings.json for local development
4. Execute and verify - don't stop at "files created"
   - Start the local runtime using the appropriate development server command
   - Test the function with realistic requests
   - Fix any errors that appear
   - Only declare success when the function runs correctly, accepts requests, and produces expected results
