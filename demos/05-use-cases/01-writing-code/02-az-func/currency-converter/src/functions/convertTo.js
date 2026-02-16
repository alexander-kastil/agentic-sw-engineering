const { app } = require('@azure/functions');

app.http('convertTo', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        context.log(`Http function processed request for url "${request.url}"`);
        const data = await request.json();         
        const { from, amount } = data;
        const key = process.env.FIXER_IO_API_KEY;

        // make a call to fixer.io to get the exchange rate and add the access key
        const response = await fetch(`http://data.fixer.io/api/latest?access_key=${key}&format=1`);
        const rates = await response.json();

        if (!rates.success) {
            throw new Error('Failed to fetch exchange rates');
        }

        // calculate the amount in the target currency
        const rate = rates.rates[from];
        const convertedAmount = amount / rate;

        return { 
            body: `Converted amount: ${convertedAmount}, Rate used: ${rate}`
        };        
    }
});
