import { useState } from 'react';
import { useCart } from '../state/CartContext';
import { CheckoutForm } from '../components/checkout/CheckoutForm';
import { CheckoutResponse } from '../components/checkout/CheckoutResponse';
import type { Order } from '../models/Order';
import { checkout } from '../services/foodService';

const mockOrderDefaults = {
  customer: { id: '1', name: 'Giro Kastil', phone: '+43 664 436 07 77', email: 'giro.kastil@integrations.at' },
  payment: { type: 'Bank Account', accountNumber: '1234' },
  shippingAddress: { street: 'Himmelstraße 115', city: 'Wien', country: 'Austria', zipCode: '1190' },
};

export function CheckoutPage() {
  const { items, sumTotal, clear } = useCart();
  const [response, setResponse] = useState<{ orderId?: string } | null>(null);

  const order: Order = {
    type: 'order',
    ...mockOrderDefaults,
    items: [...items],
    total: sumTotal,
  };

  const handleCheckout = async (o: Order) => {
    try {
      const resp = await checkout(o) as { orderId?: string };
      setResponse(resp);
    } catch {
      setResponse({ orderId: 'mock-' + Date.now() });
    }
    clear();
  };

  if (response !== null && items.length === 0) {
    return <CheckoutResponse response={response} />;
  }

  return <CheckoutForm order={order} onCheckout={handleCheckout} />;
}
