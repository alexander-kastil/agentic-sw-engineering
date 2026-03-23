import { Card, CardContent, CardHeader, Typography } from '@mui/material';
import type { OrderEventResponse } from '../../../models';

interface CheckoutResponseProps {
  response: OrderEventResponse;
}

export default function CheckoutResponse({ response }: CheckoutResponseProps) {
  return (
    <Card>
      <CardHeader title="Your order was submitted" />
      <CardContent>
        <Typography>Thank you for your order!</Typography>
        <Typography>Your order number is {response.orderId}</Typography>
        <Typography>{"We'll let you know after your payment was processed"}</Typography>
      </CardContent>
    </Card>
  );
}
