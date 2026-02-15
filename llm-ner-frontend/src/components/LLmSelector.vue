<script setup>
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { Select, MultiSelect, Chip } from 'primevue'

defineProps({ isSingleSelect: { type: Boolean, required: true } })
const selectedModel = defineModel('selectedModel', { type: String, default: null })
const selectedModels = defineModel('selectedModels', { type: Array, default: null })
const modelsStore = useModelsStore()
const { availableModels } = storeToRefs(modelsStore)
const { getModelById } = modelsStore

const removeModel = (modelId) => {
  // Entferne das Model aus dem Array - Vue Reactivity kümmert sich um den Rest
  selectedModels.value = selectedModels.value.filter((id) => id !== modelId)
}
</script>

<template>
  <div v-if="isSingleSelect">
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
  </div>
  <div v-else>
    <MultiSelect
      v-model="selectedModels"
      :options="availableModels"
      filter
      showClear
      optionLabel="name"
      optionValue="id"
      placeholder="Select a Model"
      size="medium"
      :maxSelectedLabels="0"
      class="w-80"
      :selectedItemsLabel="`${selectedModels.length} ${selectedModels.length === 1 ? 'Model' : 'Models'} selected`"
      :selectionLimit="3"
    />
    <div class="flex gap-2 mt-2">
      <Chip
        v-for="model in selectedModels"
        :key="model"
        :label="getModelById(model)?.name ?? model"
        removable
        @remove="removeModel(model)"
      />
    </div>
  </div>
</template>
