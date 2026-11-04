<script setup lang="ts">
import BasePageTitle from '@/components/BasePageTitle.vue'
import { config } from '@/config'
</script>

<template>
  <div class="about">
    <BasePageTitle
      icon="info"
      title="About"
    />
    <article class="card">
      <header class="card-header">
        <img
          class="avatar"
          src="https://avatars3.githubusercontent.com/u/16348023?s=460&v=4"
          alt="Alexander Kastil"
        >
        <div>
          <h2 class="card-title">
            Food App
          </h2>
          <p class="card-subtitle">
            By alexander.kastil@integrations.at
          </p>
        </div>
      </header>
      <div class="card-content">
        <p>
          A .NET Core Api and Vue UI implemented a Cloud Native App with step by step Installation
          Scripts used for ng-dev, ng-adv, az-native, az-400, az-204
        </p>
        <p>Using config:</p>
        <pre class="config">{{ config }}</pre>
      </div>
    </article>
  </div>
</template>

<style scoped>
.about {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
}

.card-subtitle {
  font-size: 14px;
  color: var(--color-text-muted);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0.8rem;
}

.config {
  overflow-x: auto;
  padding: 12px;
  background-color: var(--color-surface-muted);
  border-radius: var(--radius-control);
  font-size: 13px;
}
</style>
