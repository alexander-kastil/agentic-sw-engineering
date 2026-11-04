import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

declare module 'vue-router' {
  interface RouteMeta {
    public?: boolean
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue'),
      meta: { public: true },
    },
    {
      path: '/food',
      children: [
        { path: '', name: 'food', component: () => import('@/views/FoodShopView.vue') },
        { path: 'checkout', name: 'checkout', component: () => import('@/views/CheckoutView.vue') },
        { path: 'catalog', name: 'catalog', component: () => import('@/views/CatalogView.vue') },
      ],
    },
  ],
})

export default router
