import { Avatar, Card, CardContent, CardHeader, Typography } from '@mui/material';

const config = {
  catalogApi: 'https://localhost:5001',
  ordersApi: 'https://localhost:5002',
  features: { persistCart: false, remoteCart: false },
};

export default function About() {
  return (
    <Card variant="outlined" sx={{ m: 2, maxWidth: 700 }}>
      <CardHeader
        avatar={
          <Avatar src="https://avatars3.githubusercontent.com/u/16348023?s=460&v=4" />
        }
        title="Food App"
        subheader="By alexander.kastil@integrations.at"
      />
      <CardContent>
        <Typography>
          A .NET Core Api and Angular UI implemented a Cloud Native App with step by step Installation
          Scripts used for ng-dev, ng-adv, az-native, az-400, az-204
        </Typography>
        <Typography component="div" sx={{ mt: 2 }}>
          <span>Using config:</span>
          <pre style={{ background: '#f5f5f5', padding: '0.5rem', borderRadius: 4 }}>
            {JSON.stringify(config, null, 2)}
          </pre>
        </Typography>
      </CardContent>
    </Card>
  );
}
