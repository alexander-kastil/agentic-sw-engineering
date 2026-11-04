<script setup lang="ts" generic="T extends string | number">
import { useId } from 'vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  label: string
  suffix?: string
  error?: string
}>()

const model = defineModel<T>()
const id = useId()
</script>

<template>
  <div class="form-field">
    <label :for="id">{{ label }}</label>
    <div class="control">
      <input
        :id="id"
        v-model="model"
        v-bind="$attrs"
      >
      <span
        v-if="suffix"
        class="suffix"
      >{{ suffix }}</span>
    </div>
    <p
      v-if="error"
      class="error"
    >
      {{ error }}
    </p>
  </div>
</template>

<style scoped>
.form-field {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-label);
}

.control {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 12px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-control);
}

.control:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-halo);
}

input {
  flex: 1 1 auto;
  min-width: 0;
  border: none;
  outline: none;
  background: transparent;
  color: var(--color-text);
  font-size: 15px;
}

.suffix {
  color: var(--color-text-muted);
}

.error {
  font-size: 12px;
  color: var(--color-danger);
}
</style>
