<script setup lang="ts">
import { computed } from 'vue'
import CheckoutForm from '@/components/CheckoutForm.vue'
import CheckoutResponse from '@/components/CheckoutResponse.vue'
import { useOrderCheckout } from '@/composables/useOrderCheckout'
import { useCartStore } from '@/stores/cart'
import type { Order } from '@/types/food'

const cart = useCartStore()
const { response, error, submitting, checkout } = useOrderCheckout()

const order = computed<Order>(() => ({
  type: 'order',
  customer: {
    id: '1',
    name: 'Giro Kastil',
    phone: '+43 664 436 07 77',
    email: 'giro.kastil@integrations.at',
  },
  payment: { type: 'Bank Account', accountNumber: '1234' },
  shippingAddress: {
    street: 'Himmelstraße 115',
    city: 'Wien',
    country: 'Austria',
    zipCode: '1190',
  },
  items: cart.items.map((item) => ({ ...item })),
  total: cart.total,
}))
</script>

<template>
  <div class="checkout">
    <CheckoutForm
      v-if="cart.items.length > 0"
      :order="order"
      :submitting="submitting"
      @checkout="checkout"
    />
    <CheckoutResponse
      v-else-if="response"
      :response="response"
    />
    <p
      v-if="error"
      class="error"
    >
      Checkout failed: {{ error.message }}
    </p>
  </div>
</template>

<style scoped>
.checkout {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.error {
  color: var(--color-danger);
}
</style>
