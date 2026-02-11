<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Chip, Tag, DataTable, Column, MultiSelect, Button } from 'primevue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { transformEvaluationData, metrics } from '@/utils/format_evaluation_data'
import { formatDate } from '@/utils/misc_utils'
import router from '@/router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'

const route = useRoute()
const evaluationId = computed(() => route.params.evaluationId)
onMounted(() => {
  if (evaluationId.value) {
    execute(evaluationId.value)
  }
})

const { data, loading, error, execute } = useApi(apiService.getEvaluationById, null)

// Entity Classes
const availableEntityClasses = computed(() => {
  if (!data.value?.entity_classes) return []
  return [...data.value.entity_classes, 'Overall'].sort((a, b) => {
    // 'Overall' immer an erster Stelle
    if (a === 'Overall') return -1
    if (b === 'Overall') return 1
    // Sonst alphabetisch sortieren
    return a.localeCompare(b)
  })
})
const selectedEntityClasses = ref([])
const sortedSelectedEntityClasses = computed(() => {
  return [...selectedEntityClasses.value].sort((a, b) => {
    // 'Overall' immer an erster Stelle
    if (a === 'Overall') return -1
    if (b === 'Overall') return 1
    // Sonst alphabetisch sortieren
    return a.localeCompare(b)
  })
})

// Models
const { getModelById } = storeToRefs(useModelsStore())
const availableModels = computed(() => {
  if (!data.value?.models) return []
  return data.value?.models
    .map((id) => ({
      id,
      name: getModelById.value(id)?.name ?? id,
    }))
    .sort((a, b) => a.name.localeCompare(b.name))
})
const selectedModels = ref([])

// Metrics
const availableMetrics = ref(metrics)
const selectedMetrics = ref(availableMetrics.value)

// Data

const transformedData = computed(() => {
  if (!data.value?.evaluations) return []
  return transformEvaluationData(data.value.evaluations)
})

const filteredEvaluationData = computed(() => {
  return (
    transformedData.value?.filter(
      (item) =>
        selectedModels.value.includes(item.model) &&
        selectedMetrics.value.some((m) => m.id === item.metric),
    ) ?? []
  )
})

// Berechne für jede Metrik und Spalte den höchsten Wert
const maxValues = computed(() => {
  const maxes = {}

  // Für jede Metrik
  selectedMetrics.value.forEach((metric) => {
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

const restart = () => {
  router.push({
    name: 'new-ner-evaluation',
    params: { evaluationId: evaluationId.value },
  })
}

// Initialisiere Filter sobald Daten geladen sind
watch(
  () => data.value,
  (newData) => {
    if (newData) {
      // Initialisiere selectedModels mit allen verfügbaren Models
      if (newData.models && selectedModels.value.length === 0) {
        selectedModels.value = [...newData.models]
      }

      // Initialisiere selectedEntityClasses mit allen verfügbaren Entity Classes
      if (newData.entity_classes && selectedEntityClasses.value.length === 0) {
        selectedEntityClasses.value = [...newData.entity_classes, 'Overall']
      }
    }
  },
  { immediate: true },
)
</script>

<template>
  <div v-if="!loading" class="card">
    <h2 class="font-semibold text-2xl mb-5">NER Evaluation Display</h2>

    <!-- Metadaten -->
    <div class="mb-6">
      <div class="flex items-center mb-3">
        <Tag severity="secondary" class="mr-2">
          <i class="pi pi-microchip-ai mr-1"></i>
          <span class="">Modelle</span>
        </Tag>
        <div class="flex gap-2">
          <Chip
            v-for="model in data?.models"
            :key="model"
            class=""
            :label="getModelById(model)?.name ?? model"
            :style="{ backgroundColor: 'var(--primary-color)', color: '#FFFFFF' }"
          />
        </div>
      </div>
      <span class="flex items-center">
        <Tag severity="secondary" class="mr-1">
          <i class="pi pi-calendar-clock mr-1"></i>
          <span class="">Erstellungsdatum</span>
        </Tag>
        <span class="">{{ formatDate(data?.created_datetime_utc) }}</span>
      </span>
    </div>

    <!-- Filter -->
    <div class="flex flex-wrap gap-3 mb-5">
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

    <div class="mb-5">
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
            {{ availableMetrics.find((m) => m.id === data.metric)?.name ?? data.metric }}
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
    </div>

    <!-- Restart Button -->
    <div>
      <Button label="Restart" icon="pi pi-refresh" iconPos="left" @click="restart" />
    </div>
  </div>
</template>

<style scoped>
:deep(.p-datatable-thead > tr > th) {
  background-color: transparent;
  color: var(--text-color);
}
</style>
