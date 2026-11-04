<script setup lang="ts">
import BaseEuroAmount from '@/components/BaseEuroAmount.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import type { CatalogItem } from '@/types/food'

defineProps<{
  food: CatalogItem[]
  selectedId?: number
}>()

const emit = defineEmits<{
  select: [item: CatalogItem]
  delete: [item: CatalogItem]
  add: []
}>()
</script>

<template>
  <div class="card">
    <div class="header">
      <div class="title">
        <span class="tile"><BaseIcon name="restaurant_menu" /></span>
        <h1 class="page-title">
          Catalog
        </h1>
        <span
          class="count"
          :aria-label="`${food.length} items`"
        >{{ food.length }}</span>
      </div>
      <button
        type="button"
        class="add"
        @click="emit('add')"
      >
        <BaseIcon name="add" />Add Food
      </button>
    </div>
    <div class="scroller">
      <table>
        <thead>
          <tr>
            <th class="id-col">
              Id
            </th>
            <th>Name</th>
            <th class="price-col">
              Price
            </th>
            <th>In Stock</th>
            <th class="action-col" />
            <th class="action-col" />
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in food"
            :key="item.id"
            :class="{ selected: item.id === selectedId }"
            :aria-selected="item.id === selectedId"
            @click="emit('select', item)"
          >
            <td class="id-col">
              {{ item.id }}
            </td>
            <td class="name-col">
              {{ item.name }}
            </td>
            <td class="price-col">
              <BaseEuroAmount :amount="item.price" />
            </td>
            <td>
              <span
                class="badge"
                :class="item.inStock < 5 ? 'low' : 'ok'"
              >{{ item.inStock }}</span>
            </td>
            <td class="action-col">
              <button
                type="button"
                class="row-action"
                :aria-label="`Edit ${item.name}`"
                title="Select"
                @click.stop="emit('select', item)"
              >
                <BaseIcon name="edit" />
              </button>
            </td>
            <td class="action-col">
              <button
                type="button"
                class="row-action danger"
                :aria-label="`Delete ${item.name}`"
                title="Delete"
                @click.stop="emit('delete', item)"
              >
                <BaseIcon name="delete" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.card {
  overflow: hidden;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 16px;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tile {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-control);
  background-color: var(--color-primary-soft);
  color: var(--color-on-primary-soft);
}

.page-title {
  font-size: 20px;
  line-height: 28px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.count {
  padding: 2px 10px;
  border-radius: var(--radius-pill);
  background-color: var(--color-surface-muted);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.add {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  height: 44px;
  padding: 0 18px;
  border: none;
  border-radius: var(--radius-control);
  background-color: var(--color-primary);
  color: var(--color-on-primary);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.scroller {
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 560px;
  font-size: 15px;
}

th {
  height: 44px;
  padding: 12px 20px;
  background-color: var(--color-surface-muted);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  text-align: left;
}

td {
  height: 56px;
  padding: 6px 20px;
  white-space: nowrap;
  border-bottom: 1px solid var(--color-border);
}

tbody tr {
  cursor: pointer;
}

tbody tr:last-child td {
  border-bottom: none;
}

tr.selected td {
  background-color: var(--color-row-selected);
}

tr.selected .row-action:not(.danger) {
  background-color: var(--color-primary-soft);
  color: var(--color-on-primary-soft);
}

tr.selected .name-col {
  font-weight: 600;
}

.id-col {
  width: 72px;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.price-col {
  text-align: right;
}

.name-col {
  font-weight: 500;
}

.action-col {
  width: 56px;
  padding: 6px 4px;
  text-align: right;
}

.action-col:last-child {
  padding-right: 12px;
}

.row-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 10px;
  border: none;
  border-radius: 50%;
  background-color: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
}

.row-action.danger {
  color: var(--color-danger);
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.badge.ok {
  background-color: var(--color-success-soft);
  color: var(--color-on-success-soft);
}

.badge.low {
  background-color: var(--color-warning-soft);
  color: var(--color-on-warning-soft);
}
</style>
