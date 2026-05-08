import { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Box, Drawer } from '@mui/material';
import Navbar from './components/navbar/Navbar';
import Sidebar from './components/sidebar/Sidebar';
import Home from './components/home/Home';
import About from './components/about/About';
import FoodShop from './components/food/shop/FoodShop';
import Checkout from './components/food/shop/Checkout';
import CatalogContainer from './components/food/catalog/CatalogContainer';

export default function App() {
  const [sidenavOpen, setSidenavOpen] = useState(true);

  return (
    <Box sx={{ display: 'grid', gridTemplateRows: '80px auto', gridTemplateColumns: 'auto', height: '100vh', width: '100%' }}>
      <Box sx={{ gridRow: 1 }}>
        <Navbar onToggleSidenav={() => setSidenavOpen((prev) => !prev)} />
      </Box>
      <Box sx={{ gridRow: 2, display: 'flex', minHeight: '90vh', bgcolor: 'white' }}>
        <Drawer
          variant="persistent"
          anchor="left"
          open={sidenavOpen}
          sx={{
            '& .MuiDrawer-paper': { position: 'relative', minWidth: 180, bgcolor: 'white' },
          }}
        >
          <Sidebar />
        </Drawer>
        <Box sx={{ flex: 1, p: '0 1rem', overflowY: 'auto' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/food" element={<FoodShop />} />
            <Route path="/food/catalog" element={<CatalogContainer />} />
            <Route path="/food/checkout" element={<Checkout />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}
