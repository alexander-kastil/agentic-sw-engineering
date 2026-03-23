# Food Shop React

A React version of the [Angular food-shop app](../food-shop). Built as a 1-to-1 conversion preserving the same layout, routes, and features.

## Tech Stack

- **React 19** with TypeScript
- **Material UI (MUI)** - matches Angular Material styling
- **React Router v7** - mirrors Angular Router routes
- **Zustand** - lightweight cart state (replaces NgRx)
- **Vite** - fast build tooling

## Features

- 🏠 **Home** - landing page with food image
- 🍽️ **Food Shop** (`/food`) - browse food items, add to cart with quantity picker
- 📋 **Catalog** (`/food/catalog`) - admin table with add/edit/delete CRUD
- 💳 **Checkout** (`/food/checkout`) - order form with customer, payment, shipping details
- ℹ️ **About** (`/about`) - app info

## Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | Home | Landing page |
| `/food` | FoodShop | Product listing with cart |
| `/food/catalog` | CatalogContainer | Admin CRUD |
| `/food/checkout` | Checkout | Order form |
| `/about` | About | App info |

## Development

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # Production build
```

## API

Falls back to local mock data when the API is unavailable:
- Catalog API: `https://localhost:5001`
- Orders API: `https://localhost:5002`
