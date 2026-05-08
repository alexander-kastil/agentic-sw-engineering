import { AppBar, Toolbar, IconButton, Box, Button } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { NavLink } from 'react-router-dom';
import { useSidenav } from '../../state/SidenavContext';

const navItems = [
  { title: 'Home', url: '/' },
  { title: 'Food', url: '/food' },
  { title: 'Catalog', url: '/food/catalog' },
  { title: 'About', url: '/about' },
];

export function Navbar() {
  const { toggle } = useSidenav();
  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton color="inherit" onClick={toggle} edge="start" sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {navItems.map(item => (
            <Button
              key={item.url}
              component={NavLink}
              to={item.url}
              color="inherit"
              sx={{ '&.active': { fontWeight: 'bold', borderBottom: '2px solid white' } }}
              end={item.url === '/'}
            >
              {item.title}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
}
