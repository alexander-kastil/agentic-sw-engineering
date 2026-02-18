# Azure Function Typescript Currency Converter

Prompt:

```
Implement the currency converter as azure function in demos\05-use-cases\02-implementation\02-az-func\currency-converter-func-ts according to the attached document.

#fetch https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-typescript and use Azrue Function Core tools for all scaffolding
```

## General Description

A serverless currency conversion service built with Azure Functions and TypeScript that converts amounts between different currencies using real-time exchange rates. The function integrates with the Fixer.io API to fetch current exchange rates and performs calculations based on a source currency and amount provided by the client.

Key features:

- Two HTTP-triggered functions using the Fixer.io API via the /latest endpoint
- GetRates: Retrieves current exchange rates for a base currency (default: EUR). Query parameter: `base`
- GetConvert: Converts an amount from one currency to another using the /latest endpoint. Fetches the exchange rate and calculates the result by multiplying amount × rate. Query parameters: `from`, `to`, `amount`
- API key stored in local.settings.json. See [Fixer.io documentation](https://docs.apilayer.com/fixer/docs/api-documentation)

## Implementation Details and Rules

This project uses Azure Functions v4 with the TypeScript programming model. Scaffolded using Azure Function Core Tools.

Additional requirements:

- A Fixer.io API key (stored in local.settings.json for local development)
- Create a test-conversion.http rest client file with sample HTTP requests to validate both functions
- The project structure and artifacts are generated using Azure Function Core Tools scaffolding commands
