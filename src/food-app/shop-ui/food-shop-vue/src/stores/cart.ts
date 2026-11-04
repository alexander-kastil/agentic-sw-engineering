import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { useLogger } from '@/composables/useLogger'
import type { CartItem } from '@/types/food'

export const useCartStore = defineStore('cart', () => {
  const logger = useLogger()
  const items = ref<CartItem[]>([])

  const count = computed(() => items.value.reduce((sum, item) => sum + item.quantity, 0))
  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity * item.price, 0),
  )

  function quantityOf(id: number) {
    return items.value.find((item) => item.id === id)?.quantity ?? 0
  }

  function update(item: CartItem) {
    const index = items.value.findIndex((i) => i.id === item.id)
    if (item.quantity === 0) items.value = items.value.filter((i) => i.id !== item.id)
    else if (index > -1) items.value[index] = { ...item }
    else items.value.push({ ...item })
    logger.logEvent('Cart updated', { ...item })
  }

  function clear() {
    items.value = []
  }

  return { items, count, total, quantityOf, update, clear }
})
