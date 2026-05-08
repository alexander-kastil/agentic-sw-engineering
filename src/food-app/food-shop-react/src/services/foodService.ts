import type { CatalogItem, Order, OrderEventResponse } from '../models';

const CATALOG_API = 'https://localhost:5001';
const ORDERS_API = 'https://localhost:5002';

const mockFoodData: CatalogItem[] = [
  { id: 1, name: 'Butter Chicken', price: 12, inStock: 10, pictureUrl: 'falafel.jpg', description: 'Rich and creamy Indian butter chicken with aromatic spices' },
  { id: 2, name: 'Blini with Salmon', price: 9, inStock: 15, pictureUrl: 'zander.jpg', description: 'Delicate Russian blini topped with smoked salmon and cream cheese' },
  { id: 3, name: 'Wiener Schnitzel', price: 18, inStock: 8, pictureUrl: 'schnitzel.jpg', description: 'Classic Viennese schnitzel, breaded and fried to golden perfection' },
  { id: 4, name: 'Pizza Margherita', price: 11, inStock: 20, pictureUrl: 'pizza.jpg', description: 'Classic Italian pizza with fresh tomato, mozzarella and basil' },
  { id: 5, name: 'Pad Kra Pao', price: 10, inStock: 12, pictureUrl: 'pad-kra-pao.png', description: 'Spicy Thai basil stir-fry with minced meat and chilies' },
  { id: 6, name: 'Fried Noodles', price: 8, inStock: 25, pictureUrl: 'fried-noodels.jpg', description: 'Asian-style wok fried noodles with vegetables and sauce' },
];

export async function fetchFoodItems(): Promise<CatalogItem[]> {
  try {
    const resp = await fetch(`${CATALOG_API}/food`);
    if (!resp.ok) throw new Error('API unavailable');
    return resp.json();
  } catch {
    return mockFoodData;
  }
}

export async function addFoodItem(item: CatalogItem): Promise<CatalogItem> {
  const resp = await fetch(`${CATALOG_API}/food`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  if (!resp.ok) throw new Error('Failed to add item');
  return resp.json();
}

export async function updateFoodItem(item: CatalogItem): Promise<CatalogItem> {
  const resp = await fetch(`${CATALOG_API}/food/${item.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  if (!resp.ok) throw new Error('Failed to update item');
  return resp.json();
}

export async function deleteFoodItem(id: number): Promise<void> {
  const resp = await fetch(`${CATALOG_API}/food/${id}`, { method: 'DELETE' });
  if (!resp.ok) throw new Error('Failed to delete item');
}

export async function submitOrder(order: Order): Promise<OrderEventResponse> {
  try {
    const resp = await fetch(`${ORDERS_API}/orders/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(order),
    });
    if (!resp.ok) throw new Error('Order API unavailable');
    return resp.json();
  } catch {
    return {
      id: crypto.randomUUID(),
      eventType: 'OrderCreated',
      orderId: crypto.randomUUID(),
      customerId: order.customer.id,
      timestamp: new Date().toISOString(),
    };
  }
}
