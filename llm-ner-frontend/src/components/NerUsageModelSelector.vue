<script setup>
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { defineModel } from 'vue'
import { Select } from 'primevue'

const selectedModel = defineModel('selectedModel', { type: String })
const modelsStore = useModelsStore()
const { availableModels } = storeToRefs(modelsStore)
</script>

<template>
  <div class="font-semibold text-xl mb-2">Model</div>
  <Select
    v-model="selectedModel"
    :options="availableModels"
    showClear
    filter
    optionLabel="name"
    optionValue="id"
    placeholder="Select a Model"
    size="medium"
    class="w-80"
  />
</template>
