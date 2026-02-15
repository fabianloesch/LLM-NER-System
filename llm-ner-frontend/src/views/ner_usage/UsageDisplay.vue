<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from 'primevue'
import router from '@/router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'
import NerUsageMetadataDisplay from '@/components/ner_usage/NerUsageMetadataDisplay.vue'
import NerUsageLabelLegend from '@/components/ner_usage/NerUsageLabelLegend.vue'
import NerUsageAnnotatedText from '@/components/ner_usage/NerUsageAnnotatedText.vue'
import NerUsageEntitiesDetailed from '@/components/ner_usage/NerUsageEntitiesDetailed.vue'

const route = useRoute()
const usageId = computed(() => route.params.usageId)

// Get NER Model Run
const { data, loading, error, execute } = useApi(apiService.getModelRunById, null)

onMounted(() => {
  if (usageId.value) {
    execute(usageId.value)
  }
})

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
  data.value.entity_classes.forEach((label, index) => {
    map[label] = colorPalette[index % colorPalette.length]
  })
  return map
})

const getLabelColor = (label) => {
  return colorMap.value[label] || '#E0E0E0'
}

const restart = () => {
  router.push({
    name: 'new-ner-run',
    params: { usageId: usageId.value },
  })
}
</script>

<template>
  <div v-if="data" class="card">
    <h2 class="font-semibold text-2xl mb-5">NER Result Display</h2>

    <!-- Metadaten -->
    <div class="mb-5">
      <NerUsageMetadataDisplay
        :model_id="data.model"
        :created_datetime_utc="data.created_datetime_utc"
      />
    </div>

    <!-- Labels Legende -->
    <div class="mb-5">
      <NerUsageLabelLegend :entity_classes="data.entity_classes" :getLabelColor="getLabelColor" />
    </div>

    <!-- Annotierter Text -->
    <div class="mb-5">
      <NerUsageAnnotatedText
        :text="data.text"
        :entities="data.entities"
        :getLabelColor="getLabelColor"
      />
    </div>

    <!-- Entitäten Liste -->
    <div class="mb-5">
      <NerUsageEntitiesDetailed
        :text="data.text"
        :entities="data.entities"
        :getLabelColor="getLabelColor"
      />
    </div>

    <!-- Restart Button -->
    <div>
      <Button label="Restart" icon="pi pi-refresh" iconPos="left" @click="restart" />
    </div>
  </div>
</template>
