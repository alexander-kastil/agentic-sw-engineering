<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <h5 class="current-user">
    {{ auth.user }}
  </h5>
</template>

<style scoped>
.current-user {
  font-size: 14px;
  font-weight: 600;
}
</style>
