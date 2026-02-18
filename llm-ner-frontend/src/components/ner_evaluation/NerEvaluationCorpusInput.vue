<script setup>
import { FloatLabel, Textarea, Button } from 'primevue'
import { ref, computed } from 'vue'
import { validateCorpus } from '@/utils/json_validation'
import { useToastUtils } from '@/utils/toast_utils'

const { handleSuccess, handleErrors } = useToastUtils()
const corpus = defineModel('corpus', { type: String, default: '' })

const validationErrors = ref([])
const validationSuccess = ref(false)
const isValid = computed(() => validationErrors.value.length === 0)

const validateInput = () => {
  validationSuccess.value = false
  validationErrors.value = []

  if (!corpus.value || corpus.value.trim() === '') {
    validationErrors.value = ['Bitte geben Sie einen Input-Corpus ein.']
    handleErrors(validationErrors.value)
    return false
  }

  validationErrors.value = validateCorpus(corpus.value)

  if (validationErrors.value.length === 0) {
    validationSuccess.value = true
    handleSuccess('Validierung erfolgreich! Der Input-Corpus entspricht dem erwarteten Schema.')
    return true
  } else {
    handleErrors(validationErrors.value)
    return false
  }
}

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
        label="Validate"
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
