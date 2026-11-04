<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseEuroAmount from '@/components/BaseEuroAmount.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import CurrentUser from '@/components/CurrentUser.vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()

function checkout() {
  router.push({ name: 'checkout' })
}
</script>

<template>
  <aside
    class="panel"
    aria-label="Actions"
  >
    <h2 class="heading">
      Actions
    </h2>
    <div class="cart-info">
      <span class="cart-icon"><BaseIcon name="shopping_cart" /></span>
      <span class="cart-count">{{ cart.count }} items in cart</span>
    </div>
    <div class="sum">
      <span class="sum-label">Sum Total</span>
      <BaseEuroAmount
        class="sum-value"
        :amount="cart.total"
      />
    </div>
    <button
      type="button"
      class="checkout"
      :disabled="cart.items.length === 0"
      @click="checkout"
    >
      <BaseIcon name="shopping_cart" />Checkout
    </button>
    <div
      v-if="auth.authEnabled"
      class="user"
    >
      <CurrentUser />
      <button
        type="button"
        class="logout"
        @click="auth.logout()"
      >
        <BaseIcon name="logout" />Logout
      </button>
    </div>
  </aside>
</template>

<style scoped>
.panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.heading {
  font-size: 16px;
  line-height: 24px;
  font-weight: 700;
}

.cart-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-pill);
  background-color: var(--color-primary-soft);
  color: var(--color-on-primary-soft);
}

.cart-count {
  font-size: 15px;
  font-weight: 500;
}

.sum {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.sum-label {
  font-size: 14px;
  color: var(--color-text-muted);
}

.sum-value {
  font-size: 22px;
  font-weight: 700;
}

.checkout,
.logout {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 48px;
  border-radius: var(--radius-control);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.checkout {
  border: none;
  background-color: var(--color-primary);
  color: var(--color-on-primary);
}

.checkout:disabled {
  background-color: var(--color-surface-muted);
  color: var(--color-text-muted);
  cursor: not-allowed;
}

.logout {
  border: 1px solid var(--color-border-strong);
  background-color: transparent;
  color: var(--color-primary);
}

.user {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}
</style>
