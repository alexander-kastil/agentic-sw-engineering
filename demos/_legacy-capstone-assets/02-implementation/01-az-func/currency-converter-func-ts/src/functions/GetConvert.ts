import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { FixerClient } from "../utils/fixerClient";
import { RatesProvider } from "../utils/ratesProvider";
import { RatesConverter } from "../utils/ratesConverter";

interface GetConvertRequest {
    from?: string;
    to?: string;
    amount?: number;
    date?: string;
}

export async function GetConvert(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
    try {
        context.log(`GetConvert function processed request for url "${request.url}"`);

        const apiKey = FixerClient.validateApiKey(process.env.FIXER_API_KEY);

        let body: GetConvertRequest = {};
        try {
            body = await request.json();
        } catch {
            body = {};
        }

        const from = body.from || 'EUR';
        const to = body.to || 'USD';
        const amount = FixerClient.validateAmount(body.amount);
        const date = body.date;

        FixerClient.validateDate(date);

        const provider = new RatesProvider(apiKey, context);
        const rates = await provider.getRates('EUR', date);

        const result = RatesConverter.convert(amount, from, to, rates);

        return {
            body: JSON.stringify({
                success: true,
                query: {
                    from: result.from,
                    to: result.to,
                    amount: result.amount
                },
                info: {
                    timestamp: result.timestamp,
                    date: result.date
                },
                result: result.result
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

        if (message.includes('Invalid amount')) {
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

        if (message.includes('not found in rates')) {
            return {
                status: 400,
                body: JSON.stringify({ error: message })
            };
        }

        return {
            status: 500,
            body: JSON.stringify({ error: message })
        };
    }
}

app.http('GetConvert', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: GetConvert
});
