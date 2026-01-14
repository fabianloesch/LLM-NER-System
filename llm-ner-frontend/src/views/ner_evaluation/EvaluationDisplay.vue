<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Chip, Tag, DataTable, Column, MultiSelect } from 'primevue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { transformEvaluationData } from '@/utils/format_evaluation_data'

const route = useRoute()
const evaluationId = computed(() => route.params.evaluationId)

// Get NER Model Run
const nerEvaluation = ref({
  _id: '',
  created_datetime_utc: '',
  models: [],
  entity_classes: [],
  evaluations: {},
})
const isLoading = ref(false)
const error = ref(null)
const evaluationData = ref([])

// Verfügbare KPIs
const availableMetrics = ref([
  {
    id: 'precision',
    name: 'Precision',
  },
  {
    id: 'recall',
    name: 'Recall',
  },
  {
    id: 'f1_score',
    name: 'F1-Score',
  },
])

async function fetchNerEvaluation(evaluationId) {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/modelEvaluation/${evaluationId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    nerEvaluation.value = data.result
    selectedEntityClasses.value = [...data.result.entity_classes]
    selectedModels.value = [...data.result.models]
    selectedMetrics.value = [...availableMetrics]
  } catch (err) {
    console.error('Fehler beim Laden der Evaluation:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (evaluationId.value) {
    fetchNerEvaluation(evaluationId.value)
  }
})

// Get Model by Model Id
const modelsStore = useModelsStore()
const { getModelById } = storeToRefs(modelsStore)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Transform Shape of Evaluation Data
watch(
  () => nerEvaluation.value.evaluations,
  (newEvaluations) => {
    if (newEvaluations && Object.keys(newEvaluations).length > 0) {
      evaluationData.value = transformEvaluationData(newEvaluations)
    }
  },
  { deep: true },
)

// Selected Entity Classes
const selectedEntityClasses = ref([])
// Alphabetisch sortierte Entity Classes für die Tabelle
const sortedSelectedEntityClasses = computed(() => {
  return [...selectedEntityClasses.value].sort()
})

// Selected Models
const availableModels = computed(() =>
  nerEvaluation.value.models.map((id) => ({
    id,
    name: getModelById.value(id)?.name ?? id,
  })),
)
const selectedModels = ref([])

// Selected Metrics
const selectedMetrics = ref(availableMetrics.value)

// Gefilterte Evaluation Daten
const filteredEvaluationData = computed(() => {
  return evaluationData.value.filter(
    (item) =>
      selectedModels.value.includes(item.model) &&
      selectedMetrics.value.some((m) => m.id === item.metric),
  )
})
</script>

<template>
  <div class="card">
    <h2 class="font-semibold text-2xl mb-5">NER Evaluation Display</h2>

    <!-- Metadaten -->
    <div class="mb-5">
      <div class="flex items-center mb-3">
        <Tag severity="secondary" class="mr-2">
          <i class="pi pi-microchip-ai mr-1"></i>
          <span class="">Modelle</span>
        </Tag>
        <div class="flex gap-2">
          <Chip
            v-for="model in nerEvaluation.models"
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
        <span class="">{{ formatDate(nerEvaluation.created_datetime_utc) }}</span>
      </span>
    </div>

    <!-- Filter -->
    <div class="">
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
        :selectedItemsLabel="`${selectedMetrics.length} ${selectedMetrics.length === 1 ? 'KPI' : 'KPIs'} selected`"
      />

      <!-- Entity Classes Filter -->
      <MultiSelect
        v-model="selectedEntityClasses"
        :options="nerEvaluation.entity_classes"
        showClear
        placeholder="No Entity Label selected"
        size="medium"
        :maxSelectedLabels="3"
        :selectedItemsLabel="`${selectedEntityClasses.length} ${selectedEntityClasses.length === 1 ? 'Label' : 'Labels'} selected`"
      />
    </div>

    <div class="overflow-x-auto">
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
            {{ getModelById(data.model)?.name ?? data.model }}
          </template>
        </Column>
        <Column field="metric" header="Metric" style="width: 120px">
          <template #body="{ data }">
            {{ availableMetrics.find((m) => m.id === data.metric)?.name ?? data.metric }}
          </template>
        </Column>
        <Column field="overall" header="Overall" style="width: 100px"></Column>
        <Column
          v-for="entityClass in sortedSelectedEntityClasses"
          :key="entityClass"
          :field="entityClass"
          :header="entityClass"
          style="width: 120px; min-width: 100px"
        ></Column>
      </DataTable>
    </div>
  </div>
</template>

<style scoped>
:deep(.p-datatable-thead > tr > th) {
  background-color: transparent;
  color: var(--text-color);
}
</style>
