<script setup lang="ts">
import { ref } from 'vue'
import FoodCatalogForm from '@/components/FoodCatalogForm.vue'
import FoodCatalogTable from '@/components/FoodCatalogTable.vue'
import { useLogger } from '@/composables/useLogger'
import { useCatalogStore } from '@/stores/catalog'
import type { CatalogItem } from '@/types/food'

const catalog = useCatalogStore()
const logger = useLogger()
const selected = ref<CatalogItem | null>(null)

if (!catalog.loaded) {
  catalog.load()
  logger.logEvent('loaded data food from catalog')
}

function addFood() {
  selected.value = { id: 0, name: '', price: 0, inStock: 0 }
}

function selectFood(item: CatalogItem) {
  selected.value = { ...item }
}

function deleteFood(item: CatalogItem) {
  catalog.remove(item.id)
}

function saveFood(item: CatalogItem) {
  if (item.id === 0) catalog.add(item)
  else catalog.update(item)
}
</script>

<template>
  <section
    class="catalog"
    aria-label="Catalog"
  >
    <p
      v-if="catalog.error"
      class="error"
    >
      Catalog unavailable: {{ catalog.error }}
    </p>
    <FoodCatalogTable
      :food="catalog.sortedItems"
      :selected-id="selected?.id"
      @select="selectFood"
      @delete="deleteFood"
      @add="addFood"
    />
    <FoodCatalogForm
      v-if="selected"
      :food="selected"
      @save="saveFood"
    />
  </section>
</template>

<style scoped>
.catalog {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.error {
  color: var(--color-danger);
}
</style>
