import { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent, TextField, Button, Box, FormHelperText } from '@mui/material';
import type { CatalogItem } from '../../models/CatalogItem';

interface Props {
  food: CatalogItem;
  onSave: (item: CatalogItem) => void;
}

export function FoodEdit({ food, onSave }: Props) {
  const [form, setForm] = useState(food);
  const [touched, setTouched] = useState({ name: false, price: false });

  useEffect(() => { setForm(food); setTouched({ name: false, price: false }); }, [food]);

  const handleChange = (field: keyof CatalogItem, value: string | number) => {
    setForm(f => ({ ...f, [field]: value }));
  };

  const nameError = touched.name && (form.name.length < 3);
  const priceError = touched.price && (form.price < 1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTouched({ name: true, price: true });
    if (form.name.length >= 3 && form.price >= 1) {
      onSave(form);
    }
  };

  return (
    <Card variant="outlined" sx={{ mt: 2, maxWidth: 400 }}>
      <CardHeader title="Edit" />
      <CardContent>
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Box>
            <TextField
              label="Name"
              value={form.name}
              onChange={e => handleChange('name', e.target.value)}
              onBlur={() => setTouched(t => ({ ...t, name: true }))}
              fullWidth
              error={nameError}
            />
            {nameError && <FormHelperText error>Name is required and must be at least 3 characters long</FormHelperText>}
          </Box>
          <Box>
            <TextField
              label="Price"
              type="number"
              value={form.price}
              onChange={e => handleChange('price', parseFloat(e.target.value))}
              onBlur={() => setTouched(t => ({ ...t, price: true }))}
              fullWidth
              error={priceError}
            />
            {priceError && <FormHelperText error>Price must be greater than 1€</FormHelperText>}
          </Box>
          <TextField
            label="In stock"
            type="number"
            value={form.inStock}
            onChange={e => handleChange('inStock', parseInt(e.target.value))}
            fullWidth
          />
          <Button type="submit" variant="contained" color="primary">Save</Button>
        </Box>
      </CardContent>
    </Card>
  );
}
