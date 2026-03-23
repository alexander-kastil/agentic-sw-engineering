import { AppBar, Toolbar, IconButton, Box, Button } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { NavLink } from 'react-router-dom';
import type { NavItem } from '../../models';
import { useEffect, useState } from 'react';

interface NavbarProps {
  onToggleSidenav: () => void;
}

export default function Navbar({ onToggleSidenav }: NavbarProps) {
  const [menuItems, setMenuItems] = useState<NavItem[]>([]);

  useEffect(() => {
    fetch('/nav-items.json')
      .then((r) => r.json())
      .then(setMenuItems)
      .catch(() => {
        setMenuItems([
          { title: 'Home', url: '/' },
          { title: 'Food', url: '/food' },
          { title: 'Catalog', url: '/food/catalog' },
          { title: 'About', url: '/about' },
        ]);
      });
  }, []);

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <IconButton color="inherit" onClick={onToggleSidenav} edge="start" sx={{ mr: 1 }}>
          <MenuIcon color="secondary" />
        </IconButton>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {menuItems.map((mi) => (
            <Button
              key={mi.url}
              component={NavLink}
              to={mi.url}
              end={mi.url === '/'}
              color="inherit"
              sx={{
                '&.active': { borderBottom: '2px solid', borderColor: 'secondary.main' },
                textTransform: 'none',
                fontWeight: 400,
              }}
            >
              {mi.title}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
}
