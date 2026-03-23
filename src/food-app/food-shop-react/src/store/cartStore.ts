import { create } from 'zustand';
import type { CartItem } from '../models';

const STORAGE_KEY = 'cart';

interface CartState {
  items: CartItem[];
  persist: boolean;
  set: (item: CartItem) => void;
  clear: () => void;
  togglePersist: () => void;
  saveToStorage: () => void;
  loadFromStorage: () => void;
  getTotal: () => number;
  getCount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  persist: false,

  set: (item: CartItem) => {
    set((state) => {
      const existing = state.items.find((i) => i.id === item.id);
      let items: CartItem[];
      if (item.quantity === 0) {
        items = state.items.filter((i) => i.id !== item.id);
      } else if (existing) {
        items = state.items.map((i) => (i.id === item.id ? item : i));
      } else {
        items = [...state.items, item];
      }
      return { items };
    });
  },

  clear: () => {
    set({ items: [] });
    localStorage.removeItem(STORAGE_KEY);
  },

  togglePersist: () => {
    set((state) => ({ persist: !state.persist }));
  },

  saveToStorage: () => {
    const { items } = get();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  },

  loadFromStorage: () => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try {
        const items: CartItem[] = JSON.parse(raw);
        set({ items });
      } catch {
        // ignore parse errors
      }
    }
  },

  getTotal: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),

  getCount: () => get().items.reduce((sum, i) => sum + i.quantity, 0),
}));
