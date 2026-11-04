<script setup lang="ts">
const entryImage = '/assets/images/food.png'
</script>

<template>
  <div class="home">
    <img
      :src="entryImage"
      alt="login-screen"
      class="entry-image"
    >
  </div>
</template>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

.entry-image {
  width: 250px;
}
</style>
