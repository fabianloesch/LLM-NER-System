<script setup>
import { ref, computed, onMounted } from 'vue'
import { DataTable, Column, Button } from 'primevue'
import { useModelsStore } from '@/stores/models'
import router from '@/router'

// Get Model by Model Id
const modelsStore = useModelsStore()
const { getModelById } = modelsStore

const usageHistotry = ref([])
const isLoading = ref(false)
const error = ref(null)

async function fetchUsageHistory() {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch('http://127.0.0.1:8000/api/modelRuns')

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    usageHistotry.value = data.result
  } catch (err) {
    console.error('Fehler beim Laden des Usage-Historie:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchUsageHistory()
})

const groupedUsagesByDate = computed(() => {
  // Gruppieren nach Datum
  const grouped = usageHistotry.value.reduce((acc, item) => {
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

function routeToUsageDetails(usageRun) {
  router.push({
    name: 'usage',
    params: { usageId: usageRun._id },
  })
}
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">Usage History</div>
    <div v-for="group in groupedUsagesByDate" :key="group.date" class="max-w-[800px] mb-6">
      <DataTable
        :value="group.items"
        :show-headers="false"
        @row-click="(e) => routeToUsageDetails(e.data)"
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
        <Column field="model" style="width: 33%">
          <template #body="{ data }">
            {{ getModelById(data.model)?.name ?? data.model }}
          </template>
        </Column>
        <Column class="w-24 !text-end">
          <template #body="{ data }">
            <Button
              icon="pi pi-info"
              @click="routeToUsageDetails(data)"
              severity="secondary"
              rounded
            ></Button>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>
