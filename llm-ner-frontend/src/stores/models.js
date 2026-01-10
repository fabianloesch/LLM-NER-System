import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useModelsStore = defineStore('models', () => {
  // State
  const availableModels = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const getModelById = computed(() => {
    return (id) => availableModels.value.find((model) => model.id === id)
  })

  const hasModels = computed(() => availableModels.value.length > 0)

  // Actions
  async function fetchAvailableModels() {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('http://127.0.0.1:8000/api/availableModels')

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      availableModels.value = data.result
    } catch (err) {
      console.error('Fehler beim Laden der Modelle:', err)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    availableModels,
    isLoading,
    error,
    // Getters
    getModelById,
    hasModels,
    // Actions
    fetchAvailableModels,
  }
})
