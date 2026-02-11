<script setup>
import { ref, computed, onMounted } from 'vue'
import { DataTable, Column, Button } from 'primevue'
import { useModelsStore } from '@/stores/models'
import router from '@/router'
import { formatDate } from '@/utils/misc_utils'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'

// Get Model by Model Id
const modelsStore = useModelsStore()
const { getModelById } = modelsStore

const { data, loading, error, execute } = useApi(apiService.getAllEvaluations, [])

onMounted(() => {
  execute()
})

const groupedEvaluationsByDate = computed(() => {
  // Gruppieren nach Datum
  const grouped = data.value.reduce((acc, item) => {
    const date = new Date(item.created_datetime_utc)
    const dateKey = date.toLocaleDateString('de-DE', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    })

    if (!acc[dateKey]) {
      acc[dateKey] = {
        date: dateKey,
        timestamp: date.getTime(), // Für Sortierung
        items: [],
      }
    }

    acc[dateKey].items.push(item)
    return acc
  }, {})

  // In Array umwandeln und nach Datum absteigend sortieren
  return Object.values(grouped)
    .sort((a, b) => b.timestamp - a.timestamp)
    .map((group) => ({
      date: group.date,
      items: group.items.sort(
        (a, b) => new Date(b.created_datetime_utc) - new Date(a.created_datetime_utc),
      ),
    }))
})

function routeToEvaluationDetails(evaluation) {
  router.push({
    name: 'evaluation',
    params: { evaluationId: evaluation._id },
  })
}
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">Evaluation History</div>
    <div v-for="group in groupedEvaluationsByDate" :key="group.date" class="max-w-[800px] mb-6">
      <DataTable
        :value="group.items"
        :show-headers="false"
        @row-click="(e) => routeToEvaluationDetails(e.data)"
        :rowHover="true"
        selectionMode="single"
        tableStyle="min-width: 50rem"
      >
        <template #header>
          <span class="text-xl font-bold">{{ group.date }}</span>
        </template>
        <Column field="created_datetime_utc" style="width: 33%">
          <template #body="{ data }">
            {{ formatDate(data.created_datetime_utc) ?? data.created_datetime_utc }}
          </template>
        </Column>
        <Column field="model" style="">
          <template #body="{ data }">
            <div>
              <div v-for="model in data.models.sort((m) => m.name)">
                {{ getModelById(model)?.name ?? model }}
              </div>
              <!-- {{ data.models.map((m) => getModelById(m).name).join(' | ') }} -->
            </div>
          </template>
        </Column>
        <Column class="w-24 !text-end">
          <template #body="{ data }">
            <Button
              icon="pi pi-info"
              @click="routeToEvaluationDetails(data)"
              severity="secondary"
              rounded
            ></Button>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>
