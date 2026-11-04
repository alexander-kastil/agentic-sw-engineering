<script setup lang="ts">
import { computed } from 'vue'
import BaseEuroAmount from '@/components/BaseEuroAmount.vue'
import BaseNumberPicker from '@/components/BaseNumberPicker.vue'
import { useCartStore } from '@/stores/cart'
import type { CatalogItem } from '@/types/food'

const props = defineProps<{
  food: CatalogItem
}>()

const cart = useCartStore()

const quantity = computed({
  get: () => cart.quantityOf(props.food.id),
  set: (value: number) =>
    cart.update({
      id: props.food.id,
      name: props.food.name,
      price: props.food.price,
      quantity: value,
    }),
})

const imageUrl = computed(() => `/assets/images/${props.food.pictureUrl}`)
</script>

<template>
  <article
    class="card"
    :class="{ 'in-cart': quantity > 0 }"
  >
    <img
      class="image"
      :src="imageUrl"
      :alt="food.name"
    >
    <div class="text">
      <h2 class="title">
        {{ food.name }}
      </h2>
      <p class="description">
        {{ food.description }}
      </p>
    </div>
    <div class="side">
      <BaseEuroAmount
        class="price"
        :amount="food.price"
      />
      <BaseNumberPicker
        v-model="quantity"
        :item-name="food.name"
      />
    </div>
  </article>
</template>

<style scoped>
.card {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 16px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.in-cart {
  border-color: var(--color-primary-border);
}

.image {
  flex: 0 0 176px;
  width: 176px;
  height: 128px;
  object-fit: cover;
  border-radius: 12px;
}

.text {
  flex: 999 1 260px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 4px;
}

.title {
  font-size: 18px;
  line-height: 26px;
  font-weight: 600;
}

.description {
  max-width: 68ch;
  font-size: 15px;
  line-height: 24px;
  color: var(--color-text-muted);
}

.side {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
  padding-top: 4px;
}

.price {
  font-size: 18px;
  font-weight: 700;
}
</style>
