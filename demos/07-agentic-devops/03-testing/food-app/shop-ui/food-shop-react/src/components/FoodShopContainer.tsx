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
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [checkoutMessage, setCheckoutMessage] = useState<string | null>(null);

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

  const handleCheckout = async () => {
    try {
      setCheckoutLoading(true);
      setCheckoutMessage(null);

      if (cart.length === 0) {
        setCheckoutMessage('Cart is empty');
        setCheckoutLoading(false);
        return;
      }

      const orderRequest = {
        items: cart.map(item => ({
          id: item.id,
          name: item.name,
          quantity: item.quantity,
          price: item.price,
        })),
      };

      console.log('Sending order to API:', orderRequest);

      const response = await fetch(`${catalogApiUrl}/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderRequest),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Order created:', result);
      setCheckoutMessage(`Order #${result.id} created successfully!`);
      setCart([]);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to create order';
      console.error('Error creating order:', err);
      setCheckoutMessage(`Error: ${errorMessage}`);
    } finally {
      setCheckoutLoading(false);
    }
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
        <button
          className='checkout-btn'
          disabled={cart.length === 0 || checkoutLoading}
          onClick={handleCheckout}
        >
          {checkoutLoading ? 'Processing...' : 'Checkout'}
        </button>
        {checkoutMessage && (
          <div className='checkout-message' data-testid='checkout-message'>
            {checkoutMessage}
          </div>
        )}
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
