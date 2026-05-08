import { Routes, Route } from 'react-router-dom';
import { Box, Drawer } from '@mui/material';
import { CartProvider } from './state/CartContext';
import { SidenavProvider, useSidenav } from './state/SidenavContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { HomePage } from './pages/HomePage';
import { AboutPage } from './pages/AboutPage';
import { FoodShopPage } from './pages/FoodShopPage';
import { FoodCatalogPage } from './pages/FoodCatalogPage';
import { CheckoutPage } from './pages/CheckoutPage';

function AppLayout() {
  const { open } = useSidenav();
  return (
    <Box sx={{ display: 'grid', gridTemplateRows: '64px 1fr', height: '100vh' }}>
      <Navbar />
      <Box sx={{ display: 'flex', overflow: 'hidden' }}>
        <Drawer variant="persistent" open={open} sx={{ '& .MuiDrawer-paper': { position: 'relative', width: 200 } }}>
          <Sidebar />
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 2, overflow: 'auto' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/food" element={<FoodShopPage />} />
            <Route path="/food/checkout" element={<CheckoutPage />} />
            <Route path="/food/catalog" element={<FoodCatalogPage />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <CartProvider>
      <SidenavProvider>
        <AppLayout />
      </SidenavProvider>
    </CartProvider>
  );
}

export default App;
