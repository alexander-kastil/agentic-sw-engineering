import { useState } from 'react';
import {
  Box, Button, TextField, Toolbar, Typography, Paper,
} from '@mui/material';
import type { Order, CartItem } from '../../../models';
import { toEuro } from '../../../utils/format';

interface CheckoutFormProps {
  order: Order;
  onCheckout: (order: Order) => void;
}

interface FormData {
  customer: { id: string; name: string; email: string; phone: string };
  shippingAddress: { street: string; city: string; country: string; zipCode: string };
  payment: { type: string; accountNumber: string };
}

function validateForm(data: FormData): boolean {
  const { customer, shippingAddress, payment } = data;
  return !!(
    customer.name && customer.email && customer.phone &&
    shippingAddress.street && shippingAddress.city && shippingAddress.country && shippingAddress.zipCode &&
    payment.type && payment.accountNumber
  );
}

export default function CheckoutForm({ order, onCheckout }: CheckoutFormProps) {
  const [formData, setFormData] = useState<FormData>({
    customer: { ...order.customer },
    shippingAddress: { ...order.shippingAddress },
    payment: { ...order.payment },
  });
  const [touched, setTouched] = useState(false);

  const isValid = validateForm(formData);

  const handleChange = (section: keyof FormData, field: string) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [section]: { ...prev[section], [field]: e.target.value },
    }));
  };

  const handleSubmit = () => {
    setTouched(true);
    if (!isValid) return;
    onCheckout({ ...order, ...formData, items: order.items });
  };

  const fieldProps = (section: keyof FormData, field: string, label: string, required = true) => ({
    label,
    size: 'small' as const,
    fullWidth: true,
    required,
    value: (formData[section] as Record<string, string>)[field],
    onChange: handleChange(section, field),
    error: touched && required && !(formData[section] as Record<string, string>)[field],
  });

  return (
    <Box>
      <Toolbar variant="dense" sx={{ bgcolor: 'grey.200', mb: 2 }}>
        <Typography variant="h6">Checkout</Typography>
      </Toolbar>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>Customer</Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField {...fieldProps('customer', 'id', 'Id', false)} />
            <TextField {...fieldProps('customer', 'name', 'Name')} />
            <TextField {...fieldProps('customer', 'email', 'E-Mail')} type="email" />
            <TextField {...fieldProps('customer', 'phone', 'Phone')} />
          </Box>
        </Paper>

        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>Payment</Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField {...fieldProps('payment', 'type', 'Payment type')} />
            <TextField {...fieldProps('payment', 'accountNumber', 'Account')} />
          </Box>
        </Paper>

        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>Shipping Address</Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField {...fieldProps('shippingAddress', 'street', 'Street')} />
            <TextField {...fieldProps('shippingAddress', 'zipCode', 'Zip Code')} />
            <TextField {...fieldProps('shippingAddress', 'city', 'City')} />
            <TextField {...fieldProps('shippingAddress', 'country', 'Country')} />
          </Box>
        </Paper>

        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>Items</Typography>
          {order.items.map((item: CartItem, i: number) => (
            <Box key={i} sx={{ display: 'flex', gap: 2, mb: 0.5 }}>
              <TextField size="small" value={item.quantity} disabled label="Qty" sx={{ width: 60 }} />
              <TextField size="small" value={item.name} disabled label="Name" sx={{ flex: 1 }} />
              <TextField size="small" value={`${item.price} €`} disabled label="Price" sx={{ width: 80 }} />
            </Box>
          ))}
          <Typography sx={{ mt: 1 }}>Total: {toEuro(order.total)}</Typography>
        </Paper>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={touched && !isValid}
          type="submit"
        >
          Complete Checkout
        </Button>
      </Box>
    </Box>
  );
}
