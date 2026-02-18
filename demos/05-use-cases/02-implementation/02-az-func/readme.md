# Azure Function Typescript Currency Converter

## General Description

A serverless currency conversion service built with Azure Functions and TypeScript that converts amounts between different currencies using real-time exchange rates. The function integrates with the Fixer.io API to fetch current exchange rates and performs calculations based on a source currency and amount provided by the client.

Key features:

- HTTP-triggered Azure Function accepting GET requests with JSON payload containing source currency code and amount to convert; supports optional date parameter for historical exchange rates
- Fetches live exchange rates from [Fixer.io](https://fixer.io/) API using the /latest endpoint (returns JSON object with success flag, timestamp, base currency, date, and rates map) and stores API key in local.settings.json. Find details [documentation here](https://docs.apilayer.com/fixer/docs/api-documentation?utm_source=FixerHomePage&utm_medium=Referral)
- Uses /convert endpoint for direct currency conversion (returns JSON object with success flag, query parameters, exchange rate info, and converted result amount)
- Returns converted amount and the exchange rate used for transparency

Use the latest Azure Function Typescript programming model to define two HTTP-triggered functions:

- real-time rates via /latest for current calculations (GetRates function)
- direct conversion via /convert for historical date support (GetConvert function)

## Implementation Details and Rules

This project uses Azure Functions v4 with the TypeScript programming model, providing a modern, code-centric approach to function development with support for HTTP triggers and JSON-based configuration. Use Azure Function Core Tools (Typescript / v4) to scaffold the project and define two HTTP-triggered functions

- real-time rates via /latest for current calculations (GetRates function)
- direct conversion via /convert for historical date support (GetConvert function)

- A Fixer.io API key (stored in local.settings.json for local development)

Create a test-conversion.http rest client file with sample HTTP requests to validate both functions

The project structure as well as any artifacts should be generated using Azure Function Core Tools scaffolding commands, not manually created. Use Microsoft Lean MCP for best practices and respect my coding conventions.
