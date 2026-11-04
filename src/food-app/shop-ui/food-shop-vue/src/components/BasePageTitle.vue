<script setup lang="ts">
import BaseIcon from '@/components/BaseIcon.vue'

defineProps<{
  icon: string
  title: string
}>()
</script>

<template>
  <div class="page-title">
    <span class="tile"><BaseIcon :name="icon" /></span>
    <h1 class="heading">
      {{ title }}
    </h1>
  </div>
</template>

<style scoped>
.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
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

.heading {
  font-size: 20px;
  line-height: 28px;
  font-weight: 700;
  letter-spacing: -0.01em;
}
</style>
