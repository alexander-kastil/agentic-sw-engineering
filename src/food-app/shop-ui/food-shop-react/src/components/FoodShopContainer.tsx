import React, { useState, useEffect, useCallback } from 'react';
import { CatalogItem, CartItem } from '../types';
import { ShopItem } from './ShopItem';
import './FoodShopContainer.css';

interface FoodShopContainerProps {
  catalogApiUrl: string;
  sidebarVisible: boolean;
}

export const FoodShopContainer: React.FC<FoodShopContainerProps> = ({
  catalogApiUrl,
  sidebarVisible,
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
    <main className='layout'>
      {sidebarVisible && (
        <aside className='aside panel' aria-label='Actions'>
          <h2 className='panel-heading'>Actions</h2>
          <div className='cart-info'>
            <span className='cart-icon'>
              <span className='material-icons'>shopping_cart</span>
            </span>
            <span className='cart-count'>{getTotalItems()} items in cart</span>
          </div>
          <div className='sum'>
            <span className='sum-label'>Sum Total</span>
            <span className='sum-value'>{getTotalPrice().toFixed(2)} €</span>
          </div>
          <button className='checkout-btn' disabled={cart.length === 0}>
            <span className='material-icons'>shopping_cart</span>
            Checkout
          </button>
        </aside>
      )}
      <div className='content'>
        <section className='shop-list' aria-labelledby='food-title'>
          <div className='page-title'>
            <span className='title-tile'>
              <span className='material-icons'>local_dining</span>
            </span>
            <h1 id='food-title'>Food</h1>
          </div>
          {catalog.map((food) => (
            <ShopItem
              key={food.id}
              food={food}
              inCart={getItemsInCart(food.id)}
              onAmountChange={updateCart}
            />
          ))}
        </section>
        {catalog.length === 0 && (
          <div className='no-items'>No items available in catalog</div>
        )}
      </div>
    </main>
  );
};
