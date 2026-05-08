import { useEffect, useState } from 'react';
import { Box } from '@mui/material';
import type { CatalogItem, CartItem } from '../../../models';
import { fetchFoodItems } from '../../../services/foodService';
import { useCartStore } from '../../../store/cartStore';
import ShopItem from './ShopItem';

export default function FoodShop() {
  const [foods, setFoods] = useState<CatalogItem[]>([]);
  const items = useCartStore((s) => s.items);
  const setItem = useCartStore((s) => s.set);

  useEffect(() => {
    fetchFoodItems().then(setFoods);
  }, []);

  const getInCart = (id: number): number => {
    const found = items.find((i) => i.id === id);
    return found ? found.quantity : 0;
  };

  const updateCart = (cartItem: CartItem) => {
    setItem(cartItem);
  };

  return (
    <Box sx={{ p: '0 1rem' }}>
      {foods.map((f) => (
        <ShopItem
          key={f.id}
          food={f}
          inCart={getInCart(f.id)}
          onAmountChange={updateCart}
        />
      ))}
    </Box>
  );
}
