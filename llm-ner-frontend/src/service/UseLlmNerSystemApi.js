import { ref } from 'vue'

export function useApi(apiFunction, defaultValue = null) {
  const data = ref(defaultValue)
  const loading = ref(false)
  const error = ref(null)

  const execute = async (...args) => {
    loading.value = true
    error.value = null

    try {
      const fetchedData = await apiFunction(...args)
      data.value = fetchedData.result
      return data.value
    } catch (err) {
      error.value = err.response
        ? `Fehler beim Laden (${err.response.status} ${err.response.statusText})`
        : err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    data,
    loading,
    error,
    execute,
  }
}
