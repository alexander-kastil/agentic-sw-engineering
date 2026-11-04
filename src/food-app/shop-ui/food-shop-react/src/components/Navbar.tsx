import React from 'react';
import './Navbar.css';

const navItems = ['Home', 'Food', 'Catalog', 'About'];

interface NavbarProps {
  theme: 'light' | 'dark';
  onToggleMenu: () => void;
  onToggleTheme: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  theme,
  onToggleMenu,
  onToggleTheme,
}) => (
  <header className='navbar'>
    <button
      type='button'
      className='menu-button'
      aria-label='Open menu'
      onClick={onToggleMenu}
    >
      <span className='material-icons'>menu</span>
    </button>
    <div className='brand'>
      <span className='logo'>
        <span className='material-icons'>restaurant</span>
      </span>
      <span className='brand-name'>Passion for Food</span>
    </div>
    <nav className='links' aria-label='Main'>
      {navItems.map((title) => (
        <span
          key={title}
          className={`nav-link${title === 'Food' ? ' nav-link-active' : ''}`}
        >
          {title}
        </span>
      ))}
    </nav>
    <button
      type='button'
      className='theme-toggle'
      aria-label={
        theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'
      }
      onClick={onToggleTheme}
    >
      <span className='material-icons'>
        {theme === 'dark' ? 'light_mode' : 'dark_mode'}
      </span>
    </button>
  </header>
);
