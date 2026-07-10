import { InvocationContext } from "@azure/functions";
import { FixerClient, FixerResponse } from "./fixerClient";

export class RatesProvider {
    private client: FixerClient;

    constructor(apiKey: string, context: InvocationContext) {
        this.client = new FixerClient(apiKey, context);
    }

    async getCurrentRates(base: string): Promise<FixerResponse> {
        return this.client.fetchRates(base);
    }

    async getHistoricRates(base: string, date: string): Promise<FixerResponse> {
        return this.client.fetchRates(base, date);
    }

    async getRates(base: string, date?: string): Promise<FixerResponse> {
        return this.client.fetchRates(base, date);
    }
}
