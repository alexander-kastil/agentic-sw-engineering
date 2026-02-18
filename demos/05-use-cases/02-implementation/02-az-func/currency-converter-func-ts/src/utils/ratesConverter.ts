import { FixerResponse } from "./fixerClient";

export interface ConversionResult {
    from: string;
    to: string;
    amount: number;
    result: number;
    timestamp: number;
    date: string;
}

export class RatesConverter {
    static convert(
        amount: number,
        from: string,
        to: string,
        rates: FixerResponse
    ): ConversionResult {
        const rateToTarget = rates.rates[to];
        if (!rateToTarget) {
            throw new Error(`Currency ${to} not found in rates`);
        }

        let result: number;
        if (from === 'EUR') {
            result = amount * rateToTarget;
        } else {
            const rateFromSource = rates.rates[from];
            if (!rateFromSource) {
                throw new Error(`Currency ${from} not found in rates`);
            }
            result = (amount * rateToTarget) / rateFromSource;
        }

        return {
            from,
            to,
            amount,
            result,
            timestamp: rates.timestamp,
            date: rates.date
        };
    }
}
