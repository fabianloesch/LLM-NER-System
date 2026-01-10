<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const usageId = computed(() => route.params.usageId)

// Get NER Model Run
const modelRun = ref(null)
const isLoading = ref(false)
const error = ref(null)

async function fetchNerRun(modelRunId) {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/modelRun/${modelRunId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    modelRun.value = data.result
  } catch (err) {
    console.error('Fehler beim Laden des Modeldurchlaufs:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>{{ usageId }}</div>
</template>
