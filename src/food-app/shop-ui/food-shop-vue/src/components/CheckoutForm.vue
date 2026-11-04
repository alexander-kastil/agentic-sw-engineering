<script setup lang="ts">
import { computed, ref } from 'vue'
import BaseEuroAmount from '@/components/BaseEuroAmount.vue'
import BaseFormField from '@/components/BaseFormField.vue'
import type { Order } from '@/types/food'

const props = defineProps<{
  order: Order
  submitting?: boolean
}>()

const emit = defineEmits<{
  checkout: [order: Order]
}>()

const customer = ref({ ...props.order.customer })
const payment = ref({ ...props.order.payment })
const shippingAddress = ref({ ...props.order.shippingAddress })

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const valid = computed(() => {
  const values = [
    ...Object.values(customer.value),
    ...Object.values(payment.value),
    ...Object.values(shippingAddress.value),
  ]
  return values.every((value) => value.trim() !== '') && emailPattern.test(customer.value.email)
})

function completeCheckout() {
  emit('checkout', {
    ...props.order,
    customer: { ...customer.value },
    payment: { ...payment.value },
    shippingAddress: { ...shippingAddress.value },
  })
}
</script>

<template>
  <form
    class="checkout-form"
    novalidate
    @submit.prevent="completeCheckout"
  >
    <h1 class="toolbar">
      Checkout
    </h1>
    <div class="group">
      <BaseFormField
        v-model="customer.id"
        label="Id"
      />
      <BaseFormField
        v-model="customer.name"
        label="Name"
      />
      <BaseFormField
        v-model="customer.email"
        label="E-Mail"
        type="email"
      />
      <BaseFormField
        v-model="customer.phone"
        label="Phone"
      />
    </div>
    <div class="group">
      <BaseFormField
        v-model="payment.type"
        label="Payment type"
        placeholder="Payment type"
      />
      <BaseFormField
        v-model="payment.accountNumber"
        label="Account"
      />
    </div>
    <div class="group">
      <BaseFormField
        v-model="shippingAddress.street"
        label="Street"
        placeholder="Street"
      />
      <BaseFormField
        v-model="shippingAddress.zipCode"
        label="zipCode"
      />
      <BaseFormField
        v-model="shippingAddress.city"
        label="city"
      />
      <BaseFormField
        v-model="shippingAddress.country"
        label="country"
      />
    </div>
    <ul class="group items">
      <li
        v-for="item in order.items"
        :key="item.id"
        class="item"
      >
        <span class="quantity">{{ item.quantity }}</span>
        <span class="name">{{ item.name }}</span>
        <span class="price-label">item price:</span>
        <BaseEuroAmount
          class="price"
          :amount="item.price"
        />
      </li>
    </ul>
    <div class="group total">
      Total: <BaseEuroAmount :amount="order.total" />
    </div>
    <button
      type="submit"
      class="submit"
      :disabled="!valid || submitting"
    >
      Complete Checkout
    </button>
  </form>
</template>

<style scoped>
.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.toolbar {
  margin: -10px -10px 14px;
  padding: 18px 24px;
  border-bottom: 1px solid var(--color-border);
  font-size: 20px;
  font-weight: 600;
}

.group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
}

.item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
}

.item:last-child {
  border-bottom: none;
}

.quantity {
  width: 50px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.name {
  flex-grow: 4;
}

.price-label {
  color: var(--color-text-muted);
}

.price {
  width: 100px;
  text-align: right;
}

.total {
  flex-direction: row;
  gap: 0.5rem;
  font-weight: 600;
}

.submit {
  align-self: flex-end;
  height: 44px;
  padding: 0 24px;
  border: none;
  border-radius: var(--radius-control);
  background-color: var(--color-primary);
  color: var(--color-on-primary);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.submit:disabled {
  background-color: var(--color-surface-muted);
  color: var(--color-text-muted);
  cursor: not-allowed;
}
</style>
