<script setup>
import { FloatLabel, Textarea, Button } from 'primevue'
import { ref, computed } from 'vue'
import { validateCorpus } from '@/utils/json_validation'

const corpus = defineModel('corpus', { type: String, default: '' })

const emit = defineEmits(['validationSuccess', 'validationError'])

const validationErrors = ref([])
const validationSuccess = ref(false)
const isValid = computed(() => validationErrors.value.length === 0)

const handleInput = () => {
  validationSuccess.value = false
  validationErrors.value = []
}

const validateInput = () => {
  validationSuccess.value = false
  validationErrors.value = []

  if (!corpus.value || corpus.value.trim() === '') {
    validationErrors.value = ['Bitte geben Sie einen Input-Corpus ein.']
    emit('validationError', validationErrors.value)
    return false
  }

  validationErrors.value = validateCorpus(corpus.value)

  if (validationErrors.value.length === 0) {
    validationSuccess.value = true
    emit(
      'validationSuccess',
      'Validierung erfolgreich! Der Input-Corpus entspricht dem erwarteten Schema.',
    )
    return true
  } else {
    emit('validationError', validationErrors.value)
    return false
  }
}

// Expose validate function for parent to call
defineExpose({
  validateInput,
  isValid,
})
</script>

<template>
  <div>
    <div class="font-semibold text-xl mb-2">Corpus</div>
    <FloatLabel variant="on">
      <Textarea
        id="on_label"
        v-model="corpus"
        rows="12"
        cols="120"
        :class="{ 'p-invalid': !isValid && corpus }"
        @input="handleInput"
      />
      <label for="on_label">Enter JSON Corpus</label>
    </FloatLabel>
    <div class="flex items-center">
      <Button
        label="Validieren"
        icon="pi pi-check"
        iconPos="left"
        severity="secondary"
        @click="validateInput"
        class="mr-2"
      />
      <small class="text-gray-500 block">
        Format: [{"id": 1, "text": "...", "label": [[start, end, "type"], ...]}]
      </small>
    </div>
  </div>
</template>
