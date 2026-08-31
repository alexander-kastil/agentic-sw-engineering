import { Router } from 'express';
import { AppConfig } from '../types';

const router = Router();

router.get('/', (req, res) => {
    try {
        const config: AppConfig = {
            title: 'Catalog Service',
            app: {
                authEnabled: process.env.AUTH_ENABLED === 'true',
                useAppConfig: false,
                useSQLite: process.env.USE_SQLITE !== 'false',
                connectionStrings: {
                    sqliteDbConnection: `Data Source=${process.env.DATABASE_URL || './food.db'}`,
                    sqlServerConnection: ''
                }
            },
            logging: {
                logLevel: {
                    default: 'Information',
                    microsoft: 'Warning'
                }
            }
        };
        res.json(config);
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

router.get('/getEnvVars', (req, res) => {
    try {
        const envVars = { ...process.env };
        res.json(envVars);
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

export default router;
