import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { initDatabase, closeDatabase } from './database';
import foodRoutes from './routes/foodRoutes';
import configRoutes from './routes/configRoutes';

const app = express();

app.use(cors());
app.use(express.json());

async function startServer() {
  try {
    await initDatabase();
    
    app.use('/food', foodRoutes);
    app.use('/config', configRoutes);
    
    app.use((req, res) => {
      res.status(404).json({ error: 'Not found' });
    });
    
    app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
      console.error(err);
      res.status(500).json({ error: 'Internal server error' });
    });
    
    const PORT = parseInt(process.env.PORT || '5000', 10);
    
    const server = app.listen(PORT, '0.0.0.0', () => {
      console.log(`Catalog service listening on port ${PORT}`);
    });
    
    process.on('SIGINT', async () => {
      console.log('Shutting down gracefully...');
      server.close(async () => {
        await closeDatabase();
        process.exit(0);
      });
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
