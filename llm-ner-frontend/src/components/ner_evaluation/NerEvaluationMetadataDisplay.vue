<script setup>
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { formatDate } from '@/utils/misc_utils'
import { Tag, Chip } from 'primevue'

defineProps({ model_ids: Array, created_datetime_utc: String })

const modelsStore = useModelsStore()
const { getModelById } = storeToRefs(modelsStore)
</script>

<template>
  <div class="flex items-center mb-3">
    <Tag severity="secondary" class="mr-2">
      <i class="pi pi-microchip-ai mr-1"></i>
      <span class="">Modelle</span>
    </Tag>
    <div class="flex gap-2">
      <Chip
        v-for="model in model_ids"
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
    <span class="">{{ formatDate(created_datetime_utc) }}</span>
  </span>
</template>
