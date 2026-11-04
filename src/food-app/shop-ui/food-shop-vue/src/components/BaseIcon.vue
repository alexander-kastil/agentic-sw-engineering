<script setup lang="ts">
defineProps<{
  name: string
}>()
</script>

<template>
  <span
    class="material-icons base-icon"
    aria-hidden="true"
  >{{ name }}</span>
</template>

<style scoped>
.base-icon {
  font-size: 24px;
  line-height: 1;
}
</style>
