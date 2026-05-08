import type { CartItem } from './CartItem';
export interface Order {
  id?: string;
  type: string;
  customer: Customer;
  shippingAddress: Address;
  payment: Payment;
  items: CartItem[];
  total: number;
}
export interface Payment { type: string; accountNumber: string; }
export interface Address { street: string; city: string; country: string; zipCode: string; }
export interface Customer { id: string; name: string; email: string; phone: string; }
