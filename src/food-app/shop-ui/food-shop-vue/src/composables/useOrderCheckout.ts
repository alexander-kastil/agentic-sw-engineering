import { ref } from 'vue'
import { config } from '@/config'
import { useApi } from '@/composables/useApi'
import { useLogger } from '@/composables/useLogger'
import { useCartStore } from '@/stores/cart'
import type { Order, OrderEventResponse } from '@/types/food'

export function useOrderCheckout() {
  const api = useApi()
  const logger = useLogger()
  const cart = useCartStore()

  const response = ref<OrderEventResponse | null>(null)
  const error = ref<Error | null>(null)
  const submitting = ref(false)

  async function checkout(order: Order) {
    const url = `${config.ordersApi}/orders/create`
    logger.logEvent('checking out order', { order, url })
    submitting.value = true
    error.value = null
    try {
      response.value = await api.post<OrderEventResponse>(url, order)
      logger.logEvent('checkout response', { ...response.value })
      cart.clear()
    } catch (e) {
      error.value = e as Error
    } finally {
      submitting.value = false
    }
  }

  return { response, error, submitting, checkout }
}
