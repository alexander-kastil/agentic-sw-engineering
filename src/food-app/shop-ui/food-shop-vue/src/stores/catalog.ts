import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { config } from '@/config'
import { useApi } from '@/composables/useApi'
import type { CatalogItem } from '@/types/food'

export const useCatalogStore = defineStore('catalog', () => {
  const api = useApi()
  const url = `${config.catalogApi}/food`

  const items = ref<CatalogItem[]>([])
  const loaded = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const sortedItems = computed(() =>
    [...items.value].sort((a, b) => a.name.localeCompare(b.name)),
  )

  async function run(action: () => Promise<void>) {
    loading.value = true
    error.value = null
    try {
      await action()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  function load() {
    return run(async () => {
      items.value = await api.get<CatalogItem[]>(url)
      loaded.value = true
    })
  }

  function add(item: CatalogItem) {
    return run(async () => {
      items.value.push(await api.post<CatalogItem>(url, item))
    })
  }

  function update(item: CatalogItem) {
    return run(async () => {
      const saved = await api.put<CatalogItem>(url, item)
      items.value = items.value.map((i) => (i.id === saved.id ? saved : i))
    })
  }

  function remove(id: number) {
    return run(async () => {
      await api.remove(`${url}/${id}`)
      items.value = items.value.filter((i) => i.id !== id)
    })
  }

  return { items, loaded, loading, error, sortedItems, load, add, update, remove }
})
