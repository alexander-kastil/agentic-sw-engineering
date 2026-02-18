import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function GetConvert(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
    try {
        context.log(`GetConvert function processed request for url "${request.url}"`);

        const apiKey = process.env.FIXER_API_KEY;
        if (!apiKey) {
            return {
                status: 400,
                body: JSON.stringify({ error: 'FIXER_API_KEY not configured' })
            };
        }

        const from = request.query.get('from') || 'EUR';
        const to = request.query.get('to') || 'USD';
        const amountStr = request.query.get('amount') || '1';
        const amount = parseFloat(amountStr);

        if (isNaN(amount)) {
            return {
                status: 400,
                body: JSON.stringify({ error: 'Invalid amount parameter' })
            };
        }

        let url = `https://data.fixer.io/api/latest?access_key=${apiKey}&base=${from}&symbols=${to}`;

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
                body: JSON.stringify({ error: data.error?.info || 'Failed to fetch exchange rates', details: data })
            };
        }

        const rate = data.rates[to];
        if (!rate) {
            return {
                status: 400,
                body: JSON.stringify({ error: `Currency ${to} not found in rates` })
            };
        }

        const result = amount * rate;

        return {
            body: JSON.stringify({
                success: true,
                query: {
                    from,
                    to,
                    amount
                },
                info: {
                    rate,
                    timestamp: data.timestamp,
                    date: data.date
                },
                result
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

app.http('GetConvert', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: GetConvert
});
