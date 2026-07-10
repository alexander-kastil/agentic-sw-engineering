import { Router } from 'express';
import {
  getAllFoodItems,
  getFoodItemById,
  createFoodItem,
  updateFoodItem,
  deleteFoodItem
} from '../database';
import { CatalogItem } from '../types';

const router = Router();

router.get('/', async (req, res) => {
  try {
    const items = await getAllFoodItems();
    res.json(items);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10);
    const item = await getFoodItemById(id);
    res.json(item || null);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/', async (req, res) => {
  try {
    const data = req.body as Partial<CatalogItem>;

    const item = await createFoodItem({
      name: data.name || '',
      price: parseFloat(String(data.price || 0)),
      inStock: parseInt(String(data.inStock || 0), 10),
      pictureUrl: data.pictureUrl,
      description: data.description
    });

    res.status(201).json(item);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.put('/', async (req, res) => {
  try {
    const data = req.body as Partial<CatalogItem>;
    const itemId = parseInt(String(data.id || 0), 10);

    const updateData: Partial<Omit<CatalogItem, 'id'>> = {};
    if (data.name !== undefined) updateData.name = data.name;
    if (data.price !== undefined) updateData.price = parseFloat(String(data.price));
    if (data.inStock !== undefined) updateData.inStock = parseInt(String(data.inStock), 10);
    if (data.pictureUrl !== undefined) updateData.pictureUrl = data.pictureUrl;
    if (data.description !== undefined) updateData.description = data.description;

    const item = await updateFoodItem(itemId, updateData);
    res.json(item || null);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.delete('/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id, 10);
    await deleteFoodItem(id);
    res.json({});
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;
