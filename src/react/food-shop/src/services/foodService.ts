import type { CatalogItem } from '../models/CatalogItem';

const API_URL = 'http://localhost:5001';

export async function fetchFood(): Promise<CatalogItem[]> {
  const resp = await fetch(`${API_URL}/food`);
  if (!resp.ok) throw new Error('Failed to fetch food');
  return resp.json();
}

export async function addFood(item: Omit<CatalogItem, 'id'>): Promise<CatalogItem> {
  const resp = await fetch(`${API_URL}/food`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  if (!resp.ok) throw new Error('Failed to add food');
  return resp.json();
}

export async function updateFood(item: CatalogItem): Promise<CatalogItem> {
  const resp = await fetch(`${API_URL}/food`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  if (!resp.ok) throw new Error('Failed to update food');
  return resp.json();
}

export async function deleteFood(id: number): Promise<void> {
  const resp = await fetch(`${API_URL}/food/${id}`, { method: 'DELETE' });
  if (!resp.ok) throw new Error('Failed to delete food');
}

export async function checkout(order: unknown): Promise<unknown> {
  const resp = await fetch('http://localhost:5002/orders/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(order),
  });
  if (!resp.ok) throw new Error('Checkout failed');
  return resp.json();
}
