<script setup>
import { onMounted } from 'vue'
import { useModelsStore } from './stores/models'

const modelsStore = useModelsStore()

onMounted(() => {
  modelsStore.fetchAvailableModels()
})
</script>

<template>
  <router-view />
</template>

<style scoped></style>
