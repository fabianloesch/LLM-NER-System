<script setup>
import { FloatLabel, Textarea } from 'primevue'
import { defineModel } from 'vue'
const inputText = defineModel('inputText', { type: String })
</script>

<template>
  <div class="font-semibold text-xl mb-2">Text</div>
  <FloatLabel variant="on">
    <Textarea id="on_label" v-model="inputText" rows="12" cols="120" />
    <label for="on_label">Enter a Text</label>
  </FloatLabel>
</template>
