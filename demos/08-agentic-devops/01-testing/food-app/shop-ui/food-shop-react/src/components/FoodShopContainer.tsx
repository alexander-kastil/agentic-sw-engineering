import React, { useState, useEffect, useCallback } from 'react';
import { CatalogItem, CartItem } from '../types';
import { ShopItem } from './ShopItem';
import './FoodShopContainer.css';

interface FoodShopContainerProps {
  catalogApiUrl: string;
}

export const FoodShopContainer: React.FC<FoodShopContainerProps> = ({
  catalogApiUrl,
}) => {
  const [catalog, setCatalog] = useState<CatalogItem[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCatalog = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${catalogApiUrl}/food`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCatalog(Array.isArray(data) ? data : data.items || []);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to fetch catalog';
      setError(errorMessage);
      console.error('Error fetching catalog:', err);
    } finally {
      setLoading(false);
    }
  }, [catalogApiUrl]);

  useEffect(() => {
    fetchCatalog();
  }, [fetchCatalog]);

  const getItemsInCart = (id: number): number => {
    const item = cart.find((i) => i.id === id);
    return item ? item.quantity : 0;
  };

  const updateCart = (item: CartItem) => {
    setCart((prevCart) => {
      const existingIndex = prevCart.findIndex((i) => i.id === item.id);
      if (existingIndex > -1) {
        if (item.quantity === 0) {
          return prevCart.filter((i) => i.id !== item.id);
        }
        const newCart = [...prevCart];
        newCart[existingIndex] = item;
        return newCart;
      } else {
        if (item.quantity > 0) {
          return [...prevCart, item];
        }
        return prevCart;
      }
    });
  };

  if (loading) {
    return <div className='loading'>Loading catalog...</div>;
  }

  if (error) {
    return (
      <div className='error-container'>
        <h2>Error loading catalog</h2>
        <p>{error}</p>
        <button onClick={fetchCatalog}>Retry</button>
      </div>
    );
  }

  const getTotalItems = (): number => {
    return cart.reduce((sum, item) => sum + item.quantity, 0);
  };

  const getTotalPrice = (): number => {
    return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  };

  return (
    <div className='food-shop-container'>
      <aside className='cart-sidebar'>
        <button className='actions-button'>Actions</button>
        <div className='cart-info'>
          <div className='cart-items'>Items {getTotalItems()} in cart</div>
          <div className='cart-total'>
            Sum Total €{getTotalPrice().toFixed(2)}
          </div>
        </div>
        <button className='checkout-btn' disabled>
          Checkout
        </button>
      </aside>
      <main className='items-container'>
        <div className='shop-list'>
          {catalog.map((food) => (
            <ShopItem
              key={food.id}
              food={food}
              inCart={getItemsInCart(food.id)}
              onAmountChange={updateCart}
            />
          ))}
        </div>
        {catalog.length === 0 && (
          <div className='no-items'>No items available in catalog</div>
        )}
      </main>
    </div>
  );
};
