<script setup>
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import { formatDate } from '@/utils/misc_utils'
import { Tag } from 'primevue'

defineProps({ model_id: String, created_datetime_utc: String })

const modelsStore = useModelsStore()
const { getModelById } = storeToRefs(modelsStore)
</script>

<template>
  <div class="flex gap-8">
    <span class="flex items-center">
      <Tag severity="secondary" class="mr-1">
        <i class="pi pi-microchip-ai mr-1"></i>
        <span class="">Modell</span>
      </Tag>
      <span class="">{{ getModelById(model_id)?.name ?? model_id }}</span>
    </span>
    <span class="flex items-center">
      <Tag severity="secondary" class="mr-1">
        <i class="pi pi-calendar-clock mr-1"></i>
        <span class="">Erstellungsdatum</span>
      </Tag>
      <span class="">{{ formatDate(created_datetime_utc) }}</span>
    </span>
  </div>
</template>
