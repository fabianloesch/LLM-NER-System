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
        <span>Model</span>
      </Tag>
      <span>{{ getModelById(model_id)?.name ?? model_id }}</span>
    </span>
    <span class="flex items-center">
      <Tag severity="secondary" class="mr-1">
        <i class="pi pi-calendar-clock mr-1"></i>
        <span>Creation Date</span>
      </Tag>
      <span>{{ formatDate(created_datetime_utc) }}</span>
    </span>
  </div>
</template>
