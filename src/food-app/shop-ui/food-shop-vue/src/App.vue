<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import LoginCard from '@/components/LoginCard.vue'
import TheNavbar from '@/components/TheNavbar.vue'
import TheSidebar from '@/components/TheSidebar.vue'
import { useAuthStore } from '@/stores/auth'
import { useSidenavStore } from '@/stores/sidenav'
import { useThemeStore } from '@/stores/theme'

const route = useRoute()
const auth = useAuthStore()
const sidenav = useSidenavStore()
useThemeStore()

const showLogin = computed(() => !auth.isAuthenticated && !route.meta.public)
const showSidebar = computed(() => sidenav.visible && route.name !== 'home')
</script>

<template>
  <div
    v-if="showLogin"
    class="login-splash"
  >
    <LoginCard />
  </div>
  <div
    v-else
    class="main-grid"
  >
    <TheNavbar />
    <main class="layout">
      <TheSidebar
        v-if="showSidebar"
        class="aside"
      />
      <div class="content">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.login-splash {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.main-grid {
  display: grid;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.layout {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 32px;
  width: 100%;
  max-width: var(--layout-max-width);
  margin: 0 auto;
  padding: 32px var(--layout-pad-x) max(40px, env(safe-area-inset-bottom));
}

.aside {
  flex: 1 1 260px;
  min-width: 0;
}

.content {
  flex: 999 1 560px;
  min-width: 0;
}

@media (max-width: 600px) {
  .layout {
    padding: 20px var(--layout-pad-x) 32px;
    gap: 20px;
  }
}
</style>
