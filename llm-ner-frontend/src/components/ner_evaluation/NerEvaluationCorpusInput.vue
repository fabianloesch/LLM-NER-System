<script setup>
import { FloatLabel, Textarea, Button } from 'primevue'
import { ref, computed } from 'vue'
import { validateCorpus } from '@/utils/json_validation'
import { handleErrors, handleSuccess } from '@/utils/toast_utils'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const corpus = defineModel('corpus', { type: String, default: '' })

const validationErrors = ref([])
const validationSuccess = ref(false)
const isValid = computed(() => validationErrors.value.length === 0)

const validateInput = () => {
  validationSuccess.value = false
  validationErrors.value = []

  if (!corpus.value || corpus.value.trim() === '') {
    validationErrors.value = ['Bitte geben Sie einen Input-Corpus ein.']
    handleErrors(toast, validationErrors.value)
    return false
  }

  validationErrors.value = validateCorpus(corpus.value)

  if (validationErrors.value.length === 0) {
    validationSuccess.value = true
    handleSuccess(
      toast,
      'Validierung erfolgreich! Der Input-Corpus entspricht dem erwarteten Schema.',
    )
    return true
  } else {
    handleErrors(toast, validationErrors.value)
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
      <Textarea id="on_label" v-model="corpus" rows="12" cols="120" :invalid="!isValid" />
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
  {{ validationErrors.join(',') }}
</template>
