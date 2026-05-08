import { useState, useEffect } from 'react';
import { Toolbar, Typography, Box, TextField, Button, Paper } from '@mui/material';
import type { Order } from '../../models/Order';

interface Props {
  order: Order;
  onCheckout: (order: Order) => void;
}

export function CheckoutForm({ order, onCheckout }: Props) {
  const [form, setForm] = useState(order);

  useEffect(() => { setForm(order); }, [order]);

  const handleCustomer = (field: string, value: string) =>
    setForm(f => ({ ...f, customer: { ...f.customer, [field]: value } }));

  const handlePayment = (field: string, value: string) =>
    setForm(f => ({ ...f, payment: { ...f.payment, [field]: value } }));

  const handleAddress = (field: string, value: string) =>
    setForm(f => ({ ...f, shippingAddress: { ...f.shippingAddress, [field]: value } }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCheckout({ ...form, items: order.items, total: order.total });
  };

  return (
    <Box>
      <Toolbar disableGutters>
        <Typography variant="h6">Checkout</Typography>
      </Toolbar>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField label="Id" value={form.customer.id} onChange={e => handleCustomer('id', e.target.value)} fullWidth required />
            <TextField label="Name" value={form.customer.name} onChange={e => handleCustomer('name', e.target.value)} fullWidth required />
            <TextField label="E-Mail" type="email" value={form.customer.email} onChange={e => handleCustomer('email', e.target.value)} fullWidth required />
            <TextField label="Phone" value={form.customer.phone} onChange={e => handleCustomer('phone', e.target.value)} fullWidth required />
          </Box>
        </Paper>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField label="Payment type" value={form.payment.type} onChange={e => handlePayment('type', e.target.value)} fullWidth required />
            <TextField label="Account" value={form.payment.accountNumber} onChange={e => handlePayment('accountNumber', e.target.value)} fullWidth required />
          </Box>
        </Paper>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <TextField label="Street" value={form.shippingAddress.street} onChange={e => handleAddress('street', e.target.value)} fullWidth required />
            <TextField label="Zip Code" value={form.shippingAddress.zipCode} onChange={e => handleAddress('zipCode', e.target.value)} fullWidth required />
            <TextField label="City" value={form.shippingAddress.city} onChange={e => handleAddress('city', e.target.value)} fullWidth required />
            <TextField label="Country" value={form.shippingAddress.country} onChange={e => handleAddress('country', e.target.value)} fullWidth required />
          </Box>
        </Paper>
        <Paper variant="outlined" sx={{ p: 2 }}>
          {order.items.map((item, i) => (
            <Box key={i} sx={{ display: 'flex', gap: 2, mb: 1 }}>
              <TextField value={item.quantity} size="small" sx={{ width: 80 }} label="Qty" disabled />
              <TextField value={item.name} size="small" sx={{ flexGrow: 1 }} label="Name" disabled />
              <TextField value={item.price} size="small" sx={{ width: 100 }} label="Price" disabled />
            </Box>
          ))}
        </Paper>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography>Total: {order.total.toFixed(2)} €</Typography>
        </Paper>
        <Button type="submit" variant="contained" color="primary">
          Complete Checkout
        </Button>
      </Box>
    </Box>
  );
}
