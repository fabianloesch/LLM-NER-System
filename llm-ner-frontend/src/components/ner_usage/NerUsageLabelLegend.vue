<script setup>
import { Chip } from 'primevue'
defineProps({ entity_classes: Array, getLabelColor: Function })
</script>

<template>
  <div class="text-xl mb-2">Entity Classes:</div>
  <div class="flex flex-wrap gap-3">
    <Chip
      v-for="entityClass in entity_classes"
      :key="entityClass"
      :label="entityClass"
      :style="{ backgroundColor: getLabelColor(entityClass) }"
    />
  </div>
</template>
