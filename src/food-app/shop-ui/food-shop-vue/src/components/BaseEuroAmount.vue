<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  amount: number
}>()

const formatted = computed(() => `${props.amount.toFixed(2)} €`)
</script>

<template>
  <span class="euro-amount">{{ formatted }}</span>
</template>

<style scoped>
.euro-amount {
  font-variant-numeric: tabular-nums;
}
</style>
