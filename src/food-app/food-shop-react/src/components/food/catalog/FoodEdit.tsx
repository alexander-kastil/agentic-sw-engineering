import { useState, useEffect } from 'react';
import {
  Box, Button, Card, CardContent, CardHeader, TextField, Typography,
} from '@mui/material';
import type { CatalogItem } from '../../../models';

interface FoodEditProps {
  food: CatalogItem;
  onSave: (food: CatalogItem) => void;
}

export default function FoodEdit({ food, onSave }: FoodEditProps) {
  const [form, setForm] = useState({ name: food.name, price: food.price, inStock: food.inStock });
  const [touched, setTouched] = useState(false);

  useEffect(() => {
    setForm({ name: food.name, price: food.price, inStock: food.inStock });
    setTouched(false);
  }, [food]);

  const nameError = touched && (form.name.length < 3);
  const priceError = touched && (form.price < 1);

  const handleSave = () => {
    setTouched(true);
    if (form.name.length < 3 || form.price < 1) return;
    onSave({ ...food, ...form });
  };

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardHeader title="Edit" />
      <CardContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          <TextField
            label="Name"
            size="small"
            value={form.name}
            onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
            error={nameError}
          />
          {nameError && <Typography color="error" variant="caption">Name is required &amp; must be more than 3 chars</Typography>}
          <TextField
            label="Price"
            size="small"
            type="number"
            value={form.price}
            onChange={(e) => setForm((p) => ({ ...p, price: Number(e.target.value) }))}
            error={priceError}
          />
          {priceError && <Typography color="error" variant="caption">Price must be greater than 1€</Typography>}
          <TextField
            label="In stock"
            size="small"
            type="number"
            value={form.inStock}
            onChange={(e) => setForm((p) => ({ ...p, inStock: Number(e.target.value) }))}
          />
          <Box sx={{ mt: 1 }}>
            <Button variant="contained" color="primary" onClick={handleSave}>Save</Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
