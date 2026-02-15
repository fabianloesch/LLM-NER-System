<script setup>
import { computed } from 'vue'
const props = defineProps({ text: String, entities: Array, getLabelColor: Function })
const text = props.text
const entities = props.entities

const textSegments = computed(() => {
  const segments = []
  if (props.entities === null) return segments
  const sortedEntities = [...entities].sort((a, b) => a.start - b.start)
  let lastEnd = 0

  sortedEntities.forEach((entity) => {
    // Füge Text vor der Entität hinzu
    if (entity.start > lastEnd) {
      segments.push({
        text: text.substring(lastEnd, entity.start),
        isEntity: false,
      })
    }

    // Füge die Entität hinzu
    segments.push({
      text: text.substring(entity.start, entity.end),
      isEntity: true,
      label: entity.label,
    })

    lastEnd = entity.end
  })

  // Füge verbleibenden Text hinzu
  if (lastEnd < text.length) {
    segments.push({
      text: text.substring(lastEnd),
      isEntity: false,
    })
  }

  return segments
})
</script>

<template>
  <div class="text-xl mb-2">Text:</div>
  <div>
    <span
      v-for="(segment, index) in textSegments"
      :key="index"
      :class="[segment.isEntity ? 'px-1 rounded cursor-help' : '']"
      :style="segment.isEntity ? { backgroundColor: getLabelColor(segment.label) } : {}"
      :title="segment.isEntity ? segment.label : ''"
      >{{ segment.text }}</span
    >
  </div>
</template>
