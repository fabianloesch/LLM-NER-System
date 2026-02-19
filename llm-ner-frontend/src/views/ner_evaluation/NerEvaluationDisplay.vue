<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from 'primevue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { metrics } from '@/utils/format_evaluation_data'
import router from '@/router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'
import NerEvaluationMetadataDisplay from '@/components/ner_evaluation/NerEvaluationMetadataDisplay.vue'
import NerEvaluationFilters from '@/components/ner_evaluation/NerEvaluationFilters.vue'
import NerEvaluationTable from '@/components/ner_evaluation/NerEvaluationTable.vue'

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
      <NerEvaluationMetadataDisplay
        :model_ids="data?.models"
        :created_datetime_utc="data?.created_datetime_utc"
      />
    </div>

    <!-- Filter -->
    <div class="mb-5">
      <NerEvaluationFilters
        :availableModels="availableModels"
        v-model:selectedModels="selectedModels"
        :availableMetrics="availableMetrics"
        v-model:selectedMetrics="selectedMetrics"
        :availableEntityClasses="availableEntityClasses"
        v-model:selectedEntityClasses="selectedEntityClasses"
      />
    </div>

    <div class="mb-5">
      <NerEvaluationTable
        :evaluations="data?.evaluations"
        :availableMetrics="availableMetrics"
        :selectedModels="selectedModels"
        :selectedMetrics="selectedMetrics"
        :selectedEntityClasses="selectedEntityClasses"
      />
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
