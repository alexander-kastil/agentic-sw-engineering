import { Card, CardContent, CardHeader, Box, Typography } from '@mui/material';
import NumberPicker from '../../shared/number-picker/NumberPicker';
import type { CatalogItem, CartItem } from '../../../models';
import { toEuro } from '../../../utils/format';

interface ShopItemProps {
  food: CatalogItem;
  inCart: number;
  onAmountChange: (item: CartItem) => void;
}

export default function ShopItem({ food, inCart, onAmountChange }: ShopItemProps) {
  const handleAmountChange = (amount: number) => {
    onAmountChange({ id: food.id, name: food.name, price: food.price, quantity: amount });
  };

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardHeader title={`${food.name} - ${toEuro(food.price)}`} />
      <CardContent>
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: '200px auto',
            gridTemplateRows: '3fr 1fr',
            gridTemplateAreas: '"imgContainer textContainer" "imgContainer actionsContainer"',
          }}
        >
          <Box sx={{ gridArea: 'imgContainer' }}>
            <img
              src={`/images/${food.pictureUrl}`}
              alt={food.name}
              style={{ paddingLeft: '0.5rem', paddingTop: '1rem', maxWidth: 200 }}
              onError={(e) => { (e.target as HTMLImageElement).src = '/images/food.png'; }}
            />
          </Box>
          <Box sx={{ gridArea: 'textContainer', pt: 2 }}>
            <Typography>{food.description}</Typography>
          </Box>
          <Box sx={{ gridArea: 'actionsContainer', display: 'flex', flexDirection: 'row-reverse' }}>
            <NumberPicker value={inCart} onChange={handleAmountChange} />
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
