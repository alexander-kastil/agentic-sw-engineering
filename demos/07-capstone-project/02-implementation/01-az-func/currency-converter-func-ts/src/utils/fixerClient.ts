import { InvocationContext } from "@azure/functions";

export interface FixerResponse {
    success: boolean;
    timestamp: number;
    base: string;
    date: string;
    rates: Record<string, number>;
    error?: {
        code: string;
        info: string;
    };
}

export class FixerClient {
    private apiKey: string;
    private context: InvocationContext;

    constructor(apiKey: string, context: InvocationContext) {
        this.apiKey = apiKey;
        this.context = context;
    }

    static validateApiKey(apiKey: string | undefined): string {
        if (!apiKey) {
            throw new Error('FIXER_API_KEY not configured');
        }
        return apiKey;
    }

    static validateDate(date: string | undefined): void {
        if (date && !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
            throw new Error('Invalid date format. Required format: YYYY-MM-DD');
        }
    }

    static validateAmount(amount: number | undefined): number {
        const num = amount || 1;
        if (typeof num !== 'number' || num <= 0) {
            throw new Error('Invalid amount: must be a positive number');
        }
        return num;
    }

    async fetchRates(base: string, date?: string): Promise<FixerResponse> {
        FixerClient.validateDate(date);

        const endpoint = date ? date : 'latest';
        const url = `https://data.fixer.io/api/${endpoint}?access_key=${this.apiKey}&base=${base}`;

        this.context.log(`Requesting: ${url.replace(this.apiKey, '***')}`);

        const response = await fetch(url);
        if (!response.ok) {
            const errorBody = await response.text();
            this.context.log(
                `API Error: ${response.status} ${response.statusText} - ${errorBody}`
            );
            throw new Error(`Fixer API error: ${response.statusText}`);
        }

        const data = (await response.json()) as FixerResponse;
        if (!data.success) {
            this.context.log(`API Response Error: ${JSON.stringify(data)}`);
            throw new Error(data.error?.info || 'Failed to fetch exchange rates');
        }

        return data;
    }
}
