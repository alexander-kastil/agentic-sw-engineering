<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import BaseIcon from '@/components/BaseIcon.vue'
import { useFetchJson } from '@/composables/useFetchJson'
import { useSidenavStore } from '@/stores/sidenav'
import { useThemeStore } from '@/stores/theme'

interface NavItem {
  title: string
  url: string
}

const { data: navItems } = useFetchJson<NavItem[]>('/assets/nav-items.json')
const sidenav = useSidenavStore()
const themeStore = useThemeStore()

const isDark = computed(() => themeStore.theme === 'dark')
const themeLabel = computed(() => (isDark.value ? 'Switch to light theme' : 'Switch to dark theme'))
</script>

<template>
  <header class="bar">
    <button
      type="button"
      class="menu-button"
      aria-label="Open menu"
      @click="sidenav.toggle()"
    >
      <BaseIcon name="menu" />
    </button>
    <div class="brand">
      <span class="logo"><BaseIcon name="restaurant" /></span>
      <span class="brand-name">Passion for Food</span>
    </div>
    <nav
      class="links"
      aria-label="Main"
    >
      <RouterLink
        v-for="item in navItems"
        :key="item.url"
        :to="item.url"
        class="nav-link"
        exact-active-class="nav-link-active"
      >
        {{ item.title }}
      </RouterLink>
    </nav>
    <button
      type="button"
      class="theme-toggle"
      :aria-label="themeLabel"
      @click="themeStore.toggle()"
    >
      <BaseIcon :name="isDark ? 'light_mode' : 'dark_mode'" />
    </button>
  </header>
</template>

<style scoped>
.bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 16px;
  padding: 10px
    max(
      var(--layout-pad-x),
      calc((100% - var(--layout-max-width)) / 2 + var(--layout-pad-x))
    );
  padding-top: max(10px, env(safe-area-inset-top));
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.menu-button,
.theme-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background-color: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
}

.menu-button:hover,
.theme-toggle:hover {
  background-color: var(--color-surface-muted);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-right: 16px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background-color: var(--color-primary);
  color: var(--color-on-primary);
}

.logo .base-icon {
  font-size: 18px;
}

.brand-name {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.links {
  flex: 1 1 auto;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  min-height: 44px;
  padding: 0 14px;
  border-radius: var(--radius-pill);
  color: var(--color-text-muted);
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
}

.nav-link:hover {
  background-color: var(--color-surface-muted);
}

.nav-link-active,
.nav-link-active:hover {
  background-color: var(--color-primary-soft);
  color: var(--color-on-primary-soft);
  font-weight: 600;
}

.theme-toggle {
  margin-left: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
  color: var(--color-label);
}
</style>
