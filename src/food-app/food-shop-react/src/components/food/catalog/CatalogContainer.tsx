import { useEffect, useState } from 'react';
import { Box } from '@mui/material';
import type { CatalogItem } from '../../../models';
import { fetchFoodItems, addFoodItem, updateFoodItem, deleteFoodItem } from '../../../services/foodService';
import FoodList from './FoodList';
import FoodEdit from './FoodEdit';

const newFood = (): CatalogItem => ({ id: 0, name: '', price: 0, inStock: 0 });

export default function CatalogContainer() {
  const [foods, setFoods] = useState<CatalogItem[]>([]);
  const [selected, setSelected] = useState<CatalogItem | null>(null);

  useEffect(() => {
    fetchFoodItems().then(setFoods);
  }, []);

  const handleAdd = () => setSelected(newFood());

  const handleSelect = (food: CatalogItem) => setSelected(food);

  const handleDelete = async (food: CatalogItem) => {
    try {
      await deleteFoodItem(food.id);
    } catch {
      // ignore remote error, update local state
    }
    setFoods((prev) => prev.filter((f) => f.id !== food.id));
    if (selected?.id === food.id) setSelected(null);
  };

  const handleSave = async (food: CatalogItem) => {
    try {
      if (food.id === 0) {
        const created = await addFoodItem(food);
        setFoods((prev) => [...prev, created]);
      } else {
        await updateFoodItem(food);
        setFoods((prev) => prev.map((f) => (f.id === food.id ? food : f)));
      }
    } catch {
      if (food.id === 0) {
        const localItem = { ...food, id: Date.now() };
        setFoods((prev) => [...prev, localItem]);
      } else {
        setFoods((prev) => prev.map((f) => (f.id === food.id ? food : f)));
      }
    }
    setSelected(null);
  };

  return (
    <Box sx={{ p: 2 }}>
      <FoodList
        foods={foods}
        onSelect={handleSelect}
        onDelete={handleDelete}
        onAdd={handleAdd}
      />
      {selected && (
        <FoodEdit food={selected} onSave={handleSave} />
      )}
    </Box>
  );
}
