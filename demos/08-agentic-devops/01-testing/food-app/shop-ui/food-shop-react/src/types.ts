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
