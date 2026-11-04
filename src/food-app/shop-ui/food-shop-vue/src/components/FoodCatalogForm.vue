<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import BaseFormField from '@/components/BaseFormField.vue'
import type { CatalogItem } from '@/types/food'

const props = defineProps<{
  food: CatalogItem
}>()

const emit = defineEmits<{
  save: [item: CatalogItem]
}>()

const draft = ref<CatalogItem>({ ...props.food })
const nameTouched = ref(false)

const nameError = computed(() =>
  nameTouched.value && draft.value.name.trim().length < 3
    ? 'Name is required & must be more than 3 chars'
    : '',
)

watch(
  () => props.food,
  (food) => {
    draft.value = { ...food }
    nameTouched.value = false
  },
)

function save() {
  emit('save', { ...draft.value })
}
</script>

<template>
  <form
    class="card"
    novalidate
    @submit.prevent="save"
  >
    <div class="heading">
      <h2 class="title">
        Edit
      </h2>
      <span class="subject">{{ food.name }}</span>
    </div>
    <div class="fields">
      <BaseFormField
        v-model="draft.name"
        label="Name"
        type="text"
        :error="nameError"
        @blur="nameTouched = true"
      />
      <BaseFormField
        v-model="draft.price"
        label="Price"
        type="number"
        suffix="€"
      />
      <BaseFormField
        v-model="draft.inStock"
        label="In stock"
        type="number"
      />
    </div>
    <div class="actions">
      <button
        type="submit"
        class="save"
      >
        Save
      </button>
    </div>
  </form>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.heading {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.title {
  font-size: 18px;
  line-height: 26px;
  font-weight: 600;
}

.subject {
  font-size: 14px;
  color: var(--color-text-muted);
}

.fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.fields > :first-child {
  grid-column: span 2;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

.save {
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

@media (max-width: 600px) {
  .fields > :first-child {
    grid-column: auto;
  }
}
</style>
