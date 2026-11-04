import React, { useEffect, useState } from 'react';
import { FoodShopContainer } from './components/FoodShopContainer';
import { Navbar } from './components/Navbar';
import './App.css';

type Theme = 'light' | 'dark';

const initialTheme = (): Theme =>
  (localStorage.getItem('theme') as Theme | null) ??
  (window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light');

export const App: React.FC = () => {
  const catalogApiUrl =
    process.env.REACT_APP_CATALOG_API_URL || 'https://localhost:5001';
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [theme, setTheme] = useState<Theme>(initialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <div className='app'>
      <Navbar
        theme={theme}
        onToggleMenu={() => setSidebarVisible((visible) => !visible)}
        onToggleTheme={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      />
      <div className='main-row'>
        <FoodShopContainer
          catalogApiUrl={catalogApiUrl}
          sidebarVisible={sidebarVisible}
        />
      </div>
    </div>
  );
};

export default App;
