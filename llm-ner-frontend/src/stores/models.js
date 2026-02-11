import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'

export const useModelsStore = defineStore('models', () => {
  // Getters
  const getModelById = computed(() => {
    return (id) => availableModels.value.find((model) => model.id === id)
  })

  const hasModels = computed(() => availableModels.value.length > 0)

  const {
    data: availableModels,
    loading,
    error,
    execute: fetchAvailableModels,
  } = useApi(apiService.getAvailableModels, [])

  return {
    // State
    availableModels,
    isLoading: loading,
    error,
    // Getters
    getModelById,
    hasModels,
    // Actions
    fetchAvailableModels,
  }
})
