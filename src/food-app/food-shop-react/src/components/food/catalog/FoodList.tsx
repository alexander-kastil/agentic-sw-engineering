import {
  Button, Card, IconButton, Table, TableBody, TableCell,
  TableHead, TableRow, Toolbar,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import type { CatalogItem } from '../../../models';

interface FoodListProps {
  foods: CatalogItem[];
  onSelect: (food: CatalogItem) => void;
  onDelete: (food: CatalogItem) => void;
  onAdd: () => void;
}

export default function FoodList({ foods, onSelect, onDelete, onAdd }: FoodListProps) {
  return (
    <>
      <Toolbar variant="dense" sx={{ bgcolor: 'grey.100', mb: 1 }}>
        <Button variant="contained" color="secondary" onClick={onAdd}>Add Food</Button>
      </Toolbar>
      <Card variant="outlined">
        <Table size="small">
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
            {foods.map((row) => (
              <TableRow key={row.id} onClick={() => onSelect(row)} sx={{ cursor: 'pointer' }}>
                <TableCell>{row.id}</TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.price}</TableCell>
                <TableCell>{row.inStock}</TableCell>
                <TableCell padding="none">
                  <IconButton size="small" onClick={(e) => { e.stopPropagation(); onDelete(row); }}>
                    <DeleteIcon fontSize="small" titleAccess="Delete" />
                  </IconButton>
                </TableCell>
                <TableCell padding="none">
                  <IconButton size="small" onClick={(e) => { e.stopPropagation(); onSelect(row); }}>
                    <EditIcon fontSize="small" titleAccess="Select" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </>
  );
}
