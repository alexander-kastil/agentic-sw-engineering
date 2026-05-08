export interface CatalogItem {
  id: number;
  name: string;
  price: number;
  inStock: number;
  code?: string;
  pictureUrl?: string;
  description?: string;
}

export interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
}

export interface Address {
  street: string;
  city: string;
  country: string;
  zipCode: string;
}

export interface Payment {
  type: string;
  accountNumber: string;
}

export interface Order {
  id?: string;
  type: string;
  customer: Customer;
  shippingAddress: Address;
  payment: Payment;
  items: CartItem[];
  total: number;
}

export interface OrderEventResponse {
  id: string;
  eventType: string;
  orderId: string;
  customerId: string;
  timestamp: string;
}

export interface NavItem {
  title: string;
  url: string;
}
