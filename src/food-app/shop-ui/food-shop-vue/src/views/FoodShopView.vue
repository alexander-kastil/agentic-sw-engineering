<script setup lang="ts">
import BasePageTitle from '@/components/BasePageTitle.vue'
import FoodShopItem from '@/components/FoodShopItem.vue'
import { useCatalogStore } from '@/stores/catalog'

const catalog = useCatalogStore()

if (!catalog.loaded) catalog.load()
</script>

<template>
  <section
    class="food-shop"
    aria-label="Food"
  >
    <BasePageTitle
      icon="local_dining"
      title="Food"
    />
    <p
      v-if="catalog.error"
      class="error"
    >
      Catalog unavailable: {{ catalog.error }}
    </p>
    <FoodShopItem
      v-for="item in catalog.sortedItems"
      :key="item.id"
      :food="item"
    />
  </section>
</template>

<style scoped>
.food-shop {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error {
  color: var(--color-danger);
}
</style>
