<script setup>
import { Chip } from 'primevue'
const props = defineProps({ text: String, entities: Array, getLabelColor: Function })
</script>

<template>
  <div class="text-xl mb-2">Recognized Entities ({{ entities.length }}):</div>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
    <div
      v-for="(entity, index) in entities"
      :key="index"
      class="rounded-lg border border-white-300 p-4 shadow-sm hover:shadow-md transition-shadow border-l-4"
      :style="{ borderLeftColor: getLabelColor(entity.label) }"
    >
      <div class="mb-2">
        <Chip :label="entity.label" :style="{ backgroundColor: getLabelColor(entity.label) }" />
      </div>
      <div class="mb-2">"{{ text.substring(entity.start, entity.end) }}"</div>
      <div class="text-xs">Position: {{ entity.start }} - {{ entity.end }}</div>
    </div>
  </div>
</template>
