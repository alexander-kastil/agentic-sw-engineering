import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSidenavStore = defineStore('sidenav', () => {
  const visible = ref(true)

  function toggle() {
    visible.value = !visible.value
  }

  return { visible, toggle }
})
