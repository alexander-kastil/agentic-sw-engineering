import { AppBar, Box, Button, Toolbar, Typography } from '@mui/material';
import ShoppingCartCheckoutIcon from '@mui/icons-material/ShoppingCartCheckout';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../../store/cartStore';
import { toEuro } from '../../utils/format';

export default function Sidebar() {
  const navigate = useNavigate();
  const items = useCartStore((s) => s.items);
  const getTotal = useCartStore((s) => s.getTotal);
  const getCount = useCartStore((s) => s.getCount);

  const count = getCount();
  const total = getTotal();

  return (
    <Box sx={{ minWidth: 180 }}>
      <AppBar position="static" color="primary">
        <Toolbar variant="dense">
          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>Actions</Typography>
        </Toolbar>
      </AppBar>
      <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Typography variant="body1">{count} items in cart</Typography>
        <Typography variant="body1">Sum Total: {toEuro(total)}</Typography>
        <Button
          variant="contained"
          color="secondary"
          startIcon={<ShoppingCartCheckoutIcon />}
          disabled={items.length === 0}
          onClick={() => navigate('/food/checkout')}
        >
          Checkout
        </Button>
      </Box>
    </Box>
  );
}
