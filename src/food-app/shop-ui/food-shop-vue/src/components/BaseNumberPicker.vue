<script setup lang="ts">
import { computed } from 'vue'
import BaseIcon from '@/components/BaseIcon.vue'

const { itemName = '', increment = 1 } = defineProps<{
  itemName?: string
  increment?: number
}>()

const quantity = defineModel<number>({ default: 0 })

const groupLabel = computed(() => (itemName ? `Quantity of ${itemName}` : 'Quantity'))

function add() {
  quantity.value += increment
}

function remove() {
  quantity.value = Math.max(0, quantity.value - increment)
}
</script>

<template>
  <div
    class="number-picker"
    role="group"
    :aria-label="groupLabel"
  >
    <button
      type="button"
      class="remove"
      :aria-label="`Remove one ${itemName}`"
      :disabled="quantity <= 0"
      @click="remove"
    >
      <BaseIcon name="remove" />
    </button>
    <span
      class="quantity"
      aria-live="polite"
    >{{ quantity }}</span>
    <button
      type="button"
      class="add"
      :aria-label="`Add one ${itemName}`"
      @click="add"
    >
      <BaseIcon name="add" />
    </button>
  </div>
</template>

<style scoped>
.number-picker {
  display: flex;
  align-items: center;
  gap: 2px;
  background-color: var(--color-surface-muted);
  border-radius: var(--radius-pill);
}

button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  border: none;
  border-radius: var(--radius-pill);
  background-color: transparent;
  cursor: pointer;
}

.remove {
  color: var(--color-text);
}

.remove:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.add {
  background-color: var(--color-primary);
  color: var(--color-on-primary);
}

.quantity {
  min-width: 24px;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
</style>
