<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const entryImage = '/assets/images/food.png'
</script>

<template>
  <div class="login-card">
    <div class="title">
      Welcome to Food App
    </div>
    <img
      :src="entryImage"
      alt="login-screen"
      class="image"
    >
    <button
      type="button"
      class="login"
      @click="auth.login()"
    >
      Login
    </button>
  </div>
</template>

<style scoped>
.login-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 50vw;
  min-width: 360px;
  padding: 1rem;
  border: 1px dotted var(--color-border-strong);
  background-color: var(--color-surface-muted);
}

.title {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 3.5rem;
  font-size: 2rem;
}

.image {
  max-width: 100%;
}

.login {
  min-width: 140px;
  height: 44px;
  border: none;
  border-radius: var(--radius-control);
  background-color: var(--color-primary);
  color: var(--color-on-primary);
  font-weight: 600;
  cursor: pointer;
}

@media screen and (max-width: 400px) {
  .login-card {
    width: 80vw;
    min-width: 250px;
  }

  .title {
    font-size: 1rem;
  }
}
</style>
