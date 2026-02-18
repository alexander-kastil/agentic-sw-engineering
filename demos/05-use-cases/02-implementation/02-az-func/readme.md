# Azure Function Typescript Currency Converter

## General Description

A serverless currency conversion service built with Azure Functions and TypeScript that converts amounts between different currencies using real-time exchange rates. The function integrates with the Fixer.io API to fetch current exchange rates and performs calculations based on a source currency and amount provided by the client.

Key features:

- HTTP-triggered Azure Function accepting GET requests with JSON payload containing source currency code and amount to convert; supports optional date parameter for historical exchange rates
- Fetches live exchange rates from [Fixer.io](https://fixer.io/) API using the /latest endpoint (returns JSON object with success flag, timestamp, base currency, date, and rates map) and stores API key in local.settings.json. Find details [documentation here](https://docs.apilayer.com/fixer/docs/api-documentation?utm_source=FixerHomePage&utm_medium=Referral)
- Uses /convert endpoint for direct currency conversion (returns JSON object with success flag, query parameters, exchange rate info, and converted result amount)
- Returns converted amount and the exchange rate used for transparency

## Implementation Details

This project uses Azure Functions v4 with the TypeScript programming model, providing a modern, code-centric approach to function development with support for HTTP triggers and JSON-based configuration.

Use the latest Azure Function Typescript programming model to define two HTTP-triggered functions:

- real-time rates via /latest for current calculations (GetRates function)
- direct conversion via /convert for historical date support (GetConvert function)

## Requirements

To run this project locally and deploy to Azure, you need:

- Node.js v18+ for runtime support
- TypeScript v4+ for compilation
- @azure/functions npm package v4.0.0 (included in package.json)
- Azure Functions Core Tools v4.0.5382 or higher for local development
- Azure Functions Runtime v4.25+ for cloud deployment
- A Fixer.io API key (stored in local.settings.json for local development)

## DevOps

This project follows modern cloud-native DevOps practices:

- Flex Consumption plan for cost-effective, scalable serverless hosting with per-execution billing
- Infrastructure as Code using Bicep templates to define and version all Azure resources
- GitHub Actions workflows for automated CI/CD pipeline, enabling continuous integration and deployment to Azure
- Workload Identity Federation for secure, keyless authentication between GitHub Actions and Azure resources
- Deployed to Azure resource group rg-github-copilot for centralized resource management and organization
