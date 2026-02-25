export interface CatalogItem {
    id?: number;
    name: string;
    price: number;
    inStock: number;
    pictureUrl?: string;
    description?: string;
}

export interface AppConfig {
    title: string;
    app: {
        authEnabled: boolean;
        useAppConfig: boolean;
        useSQLite: boolean;
        connectionStrings: {
            sqliteDbConnection: string;
            sqlServerConnection: string;
        };
    };
    logging: {
        logLevel: {
            default: string;
            microsoft: string;
        };
    };
}
