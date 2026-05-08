import { useEffect, useState } from 'react';
import {
  Box, Button, Card, Table, TableBody, TableCell, TableHead, TableRow,
  Toolbar, IconButton, Tooltip, CircularProgress
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import type { CatalogItem } from '../models/CatalogItem';
import { FoodEdit } from '../components/catalog/FoodEdit';
import { fetchFood, addFood, updateFood, deleteFood } from '../services/foodService';

export function FoodCatalogPage() {
  const [food, setFood] = useState<CatalogItem[]>([]);
  const [selected, setSelected] = useState<CatalogItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFood()
      .then(setFood)
      .catch(() => setFood([]))
      .finally(() => setLoading(false));
  }, []);

  const handleAdd = () => setSelected({ id: 0, name: '', price: 0, inStock: 0 });
  const handleSelect = (item: CatalogItem) => setSelected({ ...item });
  const handleDelete = async (item: CatalogItem) => {
    await deleteFood(item.id);
    setFood(f => f.filter(i => i.id !== item.id));
  };
  const handleSave = async (item: CatalogItem) => {
    if (item.id === 0) {
      const created = await addFood(item);
      setFood(f => [...f, created]);
    } else {
      const updated = await updateFood(item);
      setFood(f => f.map(i => i.id === updated.id ? updated : i));
    }
    setSelected(null);
  };

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Toolbar disableGutters>
        <Button variant="contained" color="secondary" onClick={handleAdd}>Add Food</Button>
      </Toolbar>
      <Card variant="outlined">
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>In Stock</TableCell>
              <TableCell />
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {food.map(item => (
              <TableRow key={item.id} hover onClick={() => handleSelect(item)} sx={{ cursor: 'pointer' }}>
                <TableCell>{item.id}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.price}</TableCell>
                <TableCell>{item.inStock}</TableCell>
                <TableCell onClick={e => e.stopPropagation()}>
                  <Tooltip title="Delete">
                    <IconButton size="small" onClick={() => handleDelete(item)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
                <TableCell onClick={e => e.stopPropagation()}>
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => handleSelect(item)}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
      {selected && <FoodEdit food={selected} onSave={handleSave} />}
    </Box>
  );
}
