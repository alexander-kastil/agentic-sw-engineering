import { Card, CardHeader, CardContent, Typography } from '@mui/material';

interface Props {
  response: { orderId?: string } | null;
}

export function CheckoutResponse({ response }: Props) {
  return (
    <Card>
      <CardHeader title="Your order was submitted" />
      <CardContent>
        <Typography>Thank you for your order!</Typography>
        <Typography>Your order number is {response?.orderId}</Typography>
        <Typography>We'll let you know after your payment was processed</Typography>
      </CardContent>
    </Card>
  );
}
