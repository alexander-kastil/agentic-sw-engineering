import { Card, CardHeader, CardContent, Box, Typography } from '@mui/material';
import type { CatalogItem } from '../../models/CatalogItem';
import { NumberPicker } from '../shared/NumberPicker';

interface Props {
  food: CatalogItem;
  inCart: number;
  onAmountChange: (qty: number) => void;
}

export function ShopItem({ food, inCart, onAmountChange }: Props) {
  return (
    <Card variant="outlined" sx={{ width: 280 }}>
      <CardHeader title={`${food.name} - ${food.price.toFixed(2)} €`} />
      <CardContent>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Box sx={{ width: 80, height: 80, bgcolor: '#eee', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            {food.pictureUrl ? (
              <img src={`/assets/images/${food.pictureUrl}`} alt={food.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <Typography variant="caption" color="text.secondary">No image</Typography>
            )}
          </Box>
          <Typography variant="body2" sx={{ flexGrow: 1 }}>{food.description}</Typography>
        </Box>
        <Box sx={{ mt: 1 }}>
          <NumberPicker value={inCart} onChange={onAmountChange} />
        </Box>
      </CardContent>
    </Card>
  );
}
