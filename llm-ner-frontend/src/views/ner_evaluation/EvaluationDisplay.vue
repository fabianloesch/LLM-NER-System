<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Chip, Tag, DataTable, Column } from 'primevue'
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
  evaluations: {},
})
const isLoading = ref(false)
const error = ref(null)
const evaluationData = ref([])

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

watch(
  () => nerEvaluation.value.evaluations,
  (newEvaluations) => {
    if (newEvaluations && Object.keys(newEvaluations).length > 0) {
      evaluationData.value = transformEvaluationData(newEvaluations)
    }
  },
  { deep: true },
)
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

    <div class="max-w-[800px]">
      <DataTable
        :value="evaluationData"
        rowGroupMode="rowspan"
        groupRowsBy="model"
        sortMode="single"
        sortField="model"
        tableStyle="min-width: 50rem"
      >
        <Column field="model" header="Model" style="max-width: 60px">
          <template #body="{ data }">
            {{ getModelById(data.model)?.name ?? data.model }}
          </template>
        </Column>
        <Column field="metric" header="Metric"></Column>
        <Column field="overall" header="Overall"></Column>
      </DataTable>
    </div>
  </div>

  {{ evaluationData }}
</template>

<style scoped>
:deep(.p-datatable-thead > tr > th) {
  background-color: transparent !important;
  color: var(--text-color);
}
</style>
