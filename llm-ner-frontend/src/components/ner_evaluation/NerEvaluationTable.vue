<script setup>
import { DataTable, Column } from 'primevue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import { transformEvaluationData } from '@/utils/format_evaluation_data'

const props = defineProps({
  evaluations: Object,
  selectedModels: Array,
  availableMetrics: Array,
  selectedMetrics: Array,
  selectedEntityClasses: Array,
})
const modelsStore = useModelsStore()
const { getModelById } = storeToRefs(modelsStore)

// Data
const transformedData = computed(() => {
  if (!props.evaluations) return []
  return transformEvaluationData(props.evaluations)
})

const filteredEvaluationData = computed(() => {
  return (
    transformedData.value?.filter(
      (item) =>
        props.selectedModels.includes(item.model) &&
        props.selectedMetrics.some((m) => m.id === item.metric),
    ) ?? []
  )
})

const sortedSelectedEntityClasses = computed(() => {
  return [...props.selectedEntityClasses].sort((a, b) => {
    // 'Overall' immer an erster Stelle
    if (a === 'Overall') return -1
    if (b === 'Overall') return 1
    // Sonst alphabetisch sortieren
    return a.localeCompare(b)
  })
})

// Berechne für jede Metrik und Spalte den höchsten Wert
const maxValues = computed(() => {
  const maxes = {}

  // Für jede Metrik
  props.selectedMetrics.forEach((metric) => {
    maxes[metric.id] = {}

    // Höchster Wert für jede Entity Class
    sortedSelectedEntityClasses.value.forEach((entityClass) => {
      const values = filteredEvaluationData.value
        .filter((item) => item.metric === metric.id)
        .map((item) => parseFloat(item[entityClass]))
        .filter((val) => !isNaN(val))

      if (values.length > 0) {
        maxes[metric.id][entityClass] = Math.max(...values)
      }
    })
  })

  return maxes
})

// Prüfe ob ein Wert der höchste ist
const isMaxValue = (metricId, column, value) => {
  const parsedValue = parseFloat(value)
  if (isNaN(parsedValue)) return false

  return maxValues.value[metricId]?.[column] === parsedValue
}
</script>

<template>
  <DataTable
    :value="filteredEvaluationData"
    rowGroupMode="rowspan"
    groupRowsBy="model"
    sortMode="single"
    sortField="model"
    tableStyle="width: auto; min-width: 600px;"
  >
    <Column field="model" header="Model" style="width: 200px">
      <template #body="{ data }">
        {{ getModelById(data?.model)?.name ?? data.model }}
      </template>
    </Column>
    <Column field="metric" header="Metric" style="width: 120px">
      <template #body="{ data }">
        {{ props.availableMetrics.find((m) => m.id === data.metric)?.name ?? data.metric }}
      </template>
    </Column>
    <Column
      v-for="entityClass in sortedSelectedEntityClasses"
      :key="entityClass"
      :field="entityClass"
      :header="entityClass"
      style="width: 120px; min-width: 100px"
    >
      <template #body="{ data }">
        <span :class="{ 'font-bold': isMaxValue(data.metric, entityClass, data[entityClass]) }">
          {{ data[entityClass] }}
        </span>
      </template>
    </Column>
  </DataTable>
</template>
