import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { FixerClient } from "../utils/fixerClient";
import { RatesProvider } from "../utils/ratesProvider";

interface GetRatesRequest {
    base?: string;
    date?: string;
}

export async function GetRates(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
    try {
        context.log(`GetRates function processed request for url "${request.url}"`);

        const apiKey = FixerClient.validateApiKey(process.env.FIXER_API_KEY);

        let body: GetRatesRequest = {};
        try {
            body = await request.json();
        } catch {
            body = {};
        }

        const base = body.base || 'EUR';
        const date = body.date;

        FixerClient.validateDate(date);

        const provider = new RatesProvider(apiKey, context);
        const rates = await provider.getRates(base, date);

        return {
            body: JSON.stringify({
                success: true,
                timestamp: rates.timestamp,
                base: rates.base,
                date: rates.date,
                rates: rates.rates
            })
        };
    } catch (error) {
        context.log(`Error: ${error}`);
        const message = error instanceof Error ? error.message : 'Internal server error';

        if (message.includes('FIXER_API_KEY')) {
            return {
                status: 400,
                body: JSON.stringify({ error: message })
            };
        }

        if (message.includes('Invalid date')) {
            return {
                status: 400,
                body: JSON.stringify({ error: 'You have entered an invalid date. [Required format: date=YYYY-MM-DD]' })
            };
        }

        return {
            status: 500,
            body: JSON.stringify({ error: message })
        };
    }
}

app.http('GetRates', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: GetRates
});
