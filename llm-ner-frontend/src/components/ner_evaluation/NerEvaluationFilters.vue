<script setup>
import { MultiSelect } from 'primevue'

defineProps({ availableModels: Array, availableMetrics: Array, availableEntityClasses: Array })
const selectedModels = defineModel('selectedModels', { type: Array, default: [] })
const selectedMetrics = defineModel('selectedMetrics', { type: Array, default: [] })
const selectedEntityClasses = defineModel('selectedEntityClasses', { type: Array, default: [] })
</script>

<template>
  <div class="flex flex-wrap gap-3">
    <!-- Models Filter -->
    <MultiSelect
      v-model="selectedModels"
      :options="availableModels"
      optionLabel="name"
      optionValue="id"
      showClear
      placeholder="No Model selected"
      size="medium"
      :maxSelectedLabels="1"
      class="w-80"
      :selectedItemsLabel="`${selectedModels.length} ${selectedModels.length === 1 ? 'Model' : 'Models'} selected`"
    />

    <!-- Metrics Filter -->
    <MultiSelect
      v-model="selectedMetrics"
      :options="availableMetrics"
      optionLabel="name"
      showClear
      placeholder="No KPI selected"
      size="medium"
      :maxSelectedLabels="3"
      class="w-80"
      :selectedItemsLabel="`${selectedMetrics.length} ${selectedMetrics.length === 1 ? 'KPI' : 'KPIs'} selected`"
    />

    <!-- Entity Classes Filter -->
    <MultiSelect
      v-model="selectedEntityClasses"
      :options="availableEntityClasses"
      showClear
      placeholder="No Entity Label selected"
      size="medium"
      :maxSelectedLabels="3"
      class="w-80"
      :selectedItemsLabel="`${selectedEntityClasses.length} ${selectedEntityClasses.length === 1 ? 'Label' : 'Labels'} selected`"
    />
  </div>
</template>
