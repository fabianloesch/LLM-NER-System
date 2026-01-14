<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Chip, Tag } from 'primevue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'

const route = useRoute()
const usageId = computed(() => route.params.usageId)

// Get NER Model Run
const modelRun = ref({
  _id: '',
  created_datetime_utc: '',
  text: '',
  entity_classes: [],
  model: '',
  entities: [],
})
const isLoading = ref(false)
const error = ref(null)

async function fetchNerRun(modelRunId) {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/modelRun/${modelRunId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    modelRun.value = data.result
  } catch (err) {
    console.error('Fehler beim Laden des Modeldurchlaufs:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (usageId.value) {
    fetchNerRun(usageId.value)
  }
})

// Get Model by Model Id
const modelsStore = useModelsStore()
const { getModelById } = storeToRefs(modelsStore)

// Dynamische Farbpalette
const colorPalette = [
  '#FFB3BA',
  '#BAFFC9',
  '#BAE1FF',
  '#FFDFBA',
  '#E0BBE4',
  '#FFD9E8',
  '#C9E4DE',
  '#B5EAD7',
  '#FFC8A2',
  '#D4A5A5',
  '#C7CEEA',
  '#FFDAC1',
  '#E2F0CB',
  '#B5B7D8',
  '#F9C2FF',
  '#C5F0C8',
  '#FFE4B5',
  '#FFFFBA',
]

// Dynamisches Color Mapping basierend auf Labels
const colorMap = computed(() => {
  const map = {}
  modelRun.value.entity_classes.forEach((label, index) => {
    map[label] = colorPalette[index % colorPalette.length]
  })
  return map
})

const textSegments = computed(() => {
  const segments = []
  const sortedEntities = [...modelRun.value.entities].sort((a, b) => a.start - b.start)
  let lastEnd = 0

  sortedEntities.forEach((entity) => {
    // Füge Text vor der Entität hinzu
    if (entity.start > lastEnd) {
      segments.push({
        text: modelRun.value.text.substring(lastEnd, entity.start),
        isEntity: false,
      })
    }

    // Füge die Entität hinzu
    segments.push({
      text: modelRun.value.text.substring(entity.start, entity.end),
      isEntity: true,
      label: entity.label,
    })

    lastEnd = entity.end
  })

  // Füge verbleibenden Text hinzu
  if (lastEnd < modelRun.value.text.length) {
    segments.push({
      text: modelRun.value.text.substring(lastEnd),
      isEntity: false,
    })
  }

  return segments
})

const getLabelColor = (label) => {
  return colorMap.value[label] || '#E0E0E0'
}

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
</script>

<template>
  <div class="card">
    <h2 class="font-semibold text-2xl mb-5">NER Result Display</h2>

    <!-- Metadaten -->
    <div class="flex gap-8 mb-5">
      <span class="flex items-center">
        <Tag severity="secondary" class="mr-1">
          <i class="pi pi-microchip-ai mr-1"></i>
          <span class="">Modell</span>
        </Tag>
        <span class="">{{ getModelById(modelRun.model)?.name ?? modelRun.model }}</span>
      </span>
      <span class="flex items-center">
        <Tag severity="secondary" class="mr-1">
          <i class="pi pi-calendar-clock mr-1"></i>
          <span class="">Erstellungsdatum</span>
        </Tag>
        <span class="">{{ formatDate(modelRun.created_datetime_utc) }}</span>
      </span>
    </div>

    <!-- Labels Legende -->
    <div class="mb-5">
      <div class="text-xl mb-2">Entitätsklassen:</div>
      <div class="flex flex-wrap gap-3">
        <Chip
          v-for="entityClass in modelRun.entity_classes"
          :key="entityClass"
          :label="entityClass"
          :style="{ backgroundColor: getLabelColor(entityClass) }"
        />
      </div>
    </div>

    <!-- Annotierter Text -->
    <div class="mb-5">
      <div class="text-xl mb-2">Text:</div>
      <div class="">
        <span
          v-for="(segment, index) in textSegments"
          :key="index"
          :class="[segment.isEntity ? 'px-1 rounded cursor-help' : '']"
          :style="segment.isEntity ? { backgroundColor: getLabelColor(segment.label) } : {}"
          :title="segment.isEntity ? segment.label : ''"
          >{{ segment.text }}</span
        >
      </div>
    </div>

    <!-- Entitäten Liste -->
    <div class="">
      <div class="text-xl mb-2">Erkannte Entitäten ({{ modelRun.entities.length }}):</div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        <div
          v-for="(entity, index) in modelRun.entities"
          :key="index"
          class="rounded-lg border border-white-300 p-4 shadow-sm hover:shadow-md transition-shadow border-l-4"
          :style="{ borderLeftColor: getLabelColor(entity.label) }"
        >
          <div class="mb-2">
            <Chip :label="entity.label" :style="{ backgroundColor: getLabelColor(entity.label) }" />
          </div>
          <div class="mb-2">"{{ modelRun.text.substring(entity.start, entity.end) }}"</div>
          <div class="text-xs">Position: {{ entity.start }} - {{ entity.end }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
