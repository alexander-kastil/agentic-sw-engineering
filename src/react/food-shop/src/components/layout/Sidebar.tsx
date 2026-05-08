import { Box, Toolbar, Typography, Button } from '@mui/material';
import ShoppingCartCheckoutIcon from '@mui/icons-material/ShoppingCartCheckout';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../state/CartContext';

export function Sidebar() {
  const { items, itemsCount, sumTotal } = useCart();
  const navigate = useNavigate();

  return (
    <Box sx={{ width: 200, bgcolor: '#37474f', height: '100%', color: 'white', display: 'flex', flexDirection: 'column' }}>
      <Toolbar sx={{ bgcolor: '#263238' }}>
        <Typography variant="subtitle1">Actions</Typography>
      </Toolbar>
      <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Typography variant="h6">{itemsCount} items in cart</Typography>
        <Typography variant="h6">Sum Total: {sumTotal.toFixed(2)} €</Typography>
        <Button
          variant="contained"
          color="secondary"
          startIcon={<ShoppingCartCheckoutIcon />}
          onClick={() => navigate('/food/checkout')}
          disabled={items.length === 0}
        >
          Checkout
        </Button>
      </Box>
    </Box>
  );
}
