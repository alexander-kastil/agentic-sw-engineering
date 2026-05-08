import { useEffect, useState } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import type { CatalogItem } from '../models/CatalogItem';
import { ShopItem } from '../components/shop/ShopItem';
import { useCart } from '../state/CartContext';
import { fetchFood } from '../services/foodService';

export function FoodShopPage() {
  const [food, setFood] = useState<CatalogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const { items, updateCart } = useCart();

  useEffect(() => {
    fetchFood()
      .then(setFood)
      .catch(() => setFood([]))
      .finally(() => setLoading(false));
  }, []);

  const getInCart = (id: number) => {
    const item = items.find(i => i.id === id);
    return item ? item.quantity : 0;
  };

  if (loading) return <CircularProgress />;

  return (
    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
      {food.length === 0 && <Typography>No food items available. Make sure the API is running.</Typography>}
      {food.map(f => (
        <ShopItem
          key={f.id}
          food={f}
          inCart={getInCart(f.id)}
          onAmountChange={qty => updateCart({ id: f.id, name: f.name, price: f.price, quantity: qty })}
        />
      ))}
    </Box>
  );
}
