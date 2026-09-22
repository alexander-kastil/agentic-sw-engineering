import React from 'react';
import { FoodShopContainer } from './components/FoodShopContainer';
import './App.css';

export const App: React.FC = () => {
  const catalogApiUrl =
    process.env.REACT_APP_CATALOG_API_URL || 'https://localhost:5001';

  return (
    <div className='app'>
      <FoodShopContainer catalogApiUrl={catalogApiUrl} />
    </div>
  );
};

export default App;
