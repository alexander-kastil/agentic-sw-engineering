import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

interface SidenavContextType {
  open: boolean;
  toggle: () => void;
}

const SidenavContext = createContext<SidenavContextType | null>(null);

export function SidenavProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(o => !o);
  return <SidenavContext.Provider value={{ open, toggle }}>{children}</SidenavContext.Provider>;
}

export function useSidenav() {
  const ctx = useContext(SidenavContext);
  if (!ctx) throw new Error('useSidenav must be used within SidenavProvider');
  return ctx;
}
