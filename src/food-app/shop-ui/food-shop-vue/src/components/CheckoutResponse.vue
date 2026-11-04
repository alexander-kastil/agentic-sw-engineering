<script setup lang="ts">
import type { OrderEventResponse } from '@/types/food'

defineProps<{
  response: OrderEventResponse
}>()
</script>

<template>
  <article class="checkout-response">
    <h2 class="title">
      Your order was submitted
    </h2>
    <p>Thank you for your order!</p>
    <p>Your order number is {{ response.orderId }}</p>
    <p>We'll let you know after your payment was processed</p>
  </article>
</template>

<style scoped>
.checkout-response {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.title {
  font-size: 20px;
  font-weight: 600;
}
</style>
