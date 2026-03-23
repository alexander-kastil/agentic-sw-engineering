import { useState } from 'react';
import { Box } from '@mui/material';
import { useCartStore } from '../../../store/cartStore';
import { submitOrder } from '../../../services/foodService';
import type { Order, OrderEventResponse } from '../../../models';
import CheckoutForm from './CheckoutForm';
import CheckoutResponse from './CheckoutResponse';

const mockOrderData = {
  customer: { id: '1', name: 'Giro Kastil', phone: '+43 664 436 07 77', email: 'giro.kastil@integrations.at' },
  payment: { type: 'Bank Account', accountNumber: '1234' },
  shippingAddress: { street: 'Himmelstraße 115', city: 'Wien', country: 'Austria', zipCode: '1190' },
};

export default function Checkout() {
  const items = useCartStore((s) => s.items);
  const getTotal = useCartStore((s) => s.getTotal);
  const clear = useCartStore((s) => s.clear);
  const [response, setResponse] = useState<OrderEventResponse | null>(null);

  const order: Order = {
    ...mockOrderData,
    type: 'order',
    items: [...items],
    total: getTotal(),
  };

  const completeCheckout = async (o: Order) => {
    const resp = await submitOrder(o);
    setResponse(resp);
    clear();
  };

  return (
    <Box sx={{ p: 2 }}>
      {order.items.length > 0 && <CheckoutForm order={order} onCheckout={completeCheckout} />}
      {response !== null && order.items.length === 0 && (
        <CheckoutResponse response={response} />
      )}
    </Box>
  );
}
