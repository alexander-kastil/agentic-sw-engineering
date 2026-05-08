import { Card, CardHeader, CardContent, Avatar, Typography } from '@mui/material';

export function AboutPage() {
  return (
    <Card variant="outlined" sx={{ maxWidth: 600 }}>
      <CardHeader
        avatar={<Avatar src="https://avatars3.githubusercontent.com/u/16348023?s=460&v=4" />}
        title="Food App"
        subheader="By alexander.kastil@integrations.at"
      />
      <CardContent>
        <Typography>
          A .NET Core Api and Angular UI implemented a Cloud Native App with step by step Installation Scripts used for ng-dev, ng-adv, az-native, az-400, az-204
        </Typography>
      </CardContent>
    </Card>
  );
}
