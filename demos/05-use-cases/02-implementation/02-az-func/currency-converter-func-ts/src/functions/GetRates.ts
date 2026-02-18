import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function GetRates(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
    try {
        context.log(`GetRates function processed request for url "${request.url}"`);

        const apiKey = process.env.FIXER_API_KEY;
        if (!apiKey) {
            return {
                status: 400,
                body: JSON.stringify({ error: 'FIXER_API_KEY not configured' })
            };
        }

        const base = request.query.get('base') || 'EUR';
        const url = `https://data.fixer.io/api/latest?access_key=${apiKey}&base=${base}`;

        context.log(`Requesting: ${url.replace(apiKey, '***')}`);

        const response = await fetch(url);
        if (!response.ok) {
            const errorBody = await response.text();
            context.log(`API Error: ${response.status} ${response.statusText} - ${errorBody}`);
            return {
                status: response.status,
                body: JSON.stringify({ error: `Fixer API error: ${response.statusText}`, details: errorBody })
            };
        }

        const data = await response.json();
        if (!data.success) {
            context.log(`API Response Error: ${JSON.stringify(data)}`);
            return {
                status: 400,
                body: JSON.stringify({ error: data.error?.info || 'Failed to fetch rates', details: data })
            };
        }

        return {
            body: JSON.stringify({
                success: true,
                timestamp: data.timestamp,
                base: data.base,
                date: data.date,
                rates: data.rates
            })
        };
    } catch (error) {
        context.log(`Error: ${error}`);
        return {
            status: 500,
            body: JSON.stringify({ error: 'Internal server error' })
        };
    }
}

app.http('GetRates', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: GetRates
});
