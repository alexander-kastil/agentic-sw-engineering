import { createContext, useContext, useReducer, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { CartItem } from '../models/CartItem';

interface CartState {
  items: CartItem[];
  persist: boolean;
}

type CartAction =
  | { type: 'UPDATE_CART'; item: CartItem }
  | { type: 'CLEAR' }
  | { type: 'LOAD_FROM_STORAGE'; items: CartItem[] }
  | { type: 'TOGGLE_PERSIST' };

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'UPDATE_CART': {
      let cart = [...state.items];
      const idx = cart.findIndex(i => i.id === action.item.id);
      if (idx > -1) {
        if (action.item.quantity === 0) {
          cart = cart.filter(i => i.id !== action.item.id);
        } else {
          cart[idx] = { ...action.item };
        }
      } else if (action.item.quantity > 0) {
        cart.push(action.item);
      }
      return { ...state, items: cart };
    }
    case 'CLEAR':
      return { ...state, items: [] };
    case 'LOAD_FROM_STORAGE':
      return { ...state, items: action.items };
    case 'TOGGLE_PERSIST':
      return { ...state, persist: !state.persist };
    default:
      return state;
  }
}

interface CartContextType {
  items: CartItem[];
  persist: boolean;
  updateCart: (item: CartItem) => void;
  clear: () => void;
  togglePersist: () => void;
  itemsCount: number;
  sumTotal: number;
}

const CartContext = createContext<CartContextType | null>(null);

const STORAGE_KEY = 'food-shop-cart';

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], persist: true });

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      dispatch({ type: 'LOAD_FROM_STORAGE', items: JSON.parse(stored) });
    }
  }, []);

  useEffect(() => {
    if (state.persist) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.items));
    }
  }, [state.items, state.persist]);

  const updateCart = (item: CartItem) => dispatch({ type: 'UPDATE_CART', item });
  const clear = () => {
    dispatch({ type: 'CLEAR' });
    localStorage.removeItem(STORAGE_KEY);
  };
  const togglePersist = () => dispatch({ type: 'TOGGLE_PERSIST' });
  const itemsCount = state.items.reduce((sum, i) => sum + i.quantity, 0);
  const sumTotal = state.items.reduce((sum, i) => sum + i.quantity * i.price, 0);

  return (
    <CartContext.Provider value={{ items: state.items, persist: state.persist, updateCart, clear, togglePersist, itemsCount, sumTotal }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used within CartProvider');
  return ctx;
}
