<script setup>
import { FloatLabel, Textarea, Chip, Button, MultiSelect, Message } from 'primevue'
import { ref, computed, onMounted, watch } from 'vue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { validateCorpus } from '@/utils/json_validation'
import { useToast } from 'primevue/usetoast'
import { useRoute } from 'vue-router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'

const toast = useToast()
const modelsStore = useModelsStore()
const route = useRoute()
const evaluationId = computed(() => route.params.evaluationId)

// Select Model
const { availableModels, getModelById } = storeToRefs(modelsStore)
const removeModel = (modelId) => {
  const index = inputData.value.models.indexOf(modelId)
  if (index > -1) {
    inputData.value.models.splice(index, 1)
  }
}

// Validation
const validationErrors = ref([])
const validationSuccess = ref(false)
const isValid = computed(() => validationErrors.value.length === 0)

function validateInput() {
  validationSuccess.value = false

  if (!inputData.value.corpus || inputData.value.corpus.trim() === '') {
    validationErrors.value = ['Bitte geben Sie einen Input-Corpus ein.']
    showError(validationErrors.value.join(' '))
    return false
  }

  validationErrors.value = validateCorpus(inputData.value.corpus)

  if (validationErrors.value.length === 0) {
    validationSuccess.value = true
    showSuccess('Validierung erfolgreich! Der Input-Corpus entspricht dem erwarteten Schema.')
  } else {
    showError(validationErrors.value.join(' '))
  }

  return validationErrors.value.length === 0
}

// Start NER Run
const {
  data: responsePostEvaluation,
  loading: postEvaluationIsLoading,
  error: postEvaluationError,
  execute: executeCreateEvaluation,
} = useApi(apiService.createEvaluation, null)

async function submit() {
  if (!validateInput()) {
    return
  }

  if (inputData.value.models.length === 0) {
    validationErrors.value = ['Bitte wählen Sie mindestens ein Modell aus']
    return
  }

  const requestBody = {
    corpus: JSON.parse(inputData.value.corpus), // Parse the JSON before sending
    llm_ids: inputData.value.models,
  }

  await executeCreateEvaluation(requestBody)
  router.push({
    name: 'evaluation',
    params: { evaluationId: responsePostEvaluation.value._id },
  })
}

function showSuccess(details) {
  toast.add({
    severity: 'success',
    summary: 'Success Message',
    detail: details,
    life: 5000,
  })
}

function showInfo() {
  toast.add({ severity: 'info', summary: 'Info Message', detail: 'Message Detail', life: 5000 })
}

function showWarn() {
  toast.add({ severity: 'warn', summary: 'Warn Message', detail: 'Message Detail', life: 5000 })
}

function showError(details) {
  toast.add({ severity: 'error', summary: 'Error Message', detail: details, life: 5000 })
}

// Get Model Run As Template
const inputData = ref({
  models: [],
  corpus: '',
})

const {
  data: responseGetEvaluation,
  loading: getEvaluationIsLoading,
  error: getEvaluationError,
  execute: executeGetEvaluation,
} = useApi(apiService.getEvaluationById, null)

// Watch für die API Response, um die Daten zu transformieren
watch(
  () => responseGetEvaluation.value,
  (newData) => {
    if (newData) {
      inputData.value = {
        models: newData.models || [],
        corpus: newData.corpus ? JSON.stringify(newData.corpus, null, 2) : '',
      }
    }
  },
)

onMounted(() => {
  if (evaluationId.value) {
    executeGetEvaluation(evaluationId.value)
  }
})
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Evaluation Editor</div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Model</div>
      <MultiSelect
        v-model="inputData.models"
        :options="availableModels"
        filter
        showClear
        optionLabel="name"
        optionValue="id"
        placeholder="Select a Model"
        size="medium"
        :maxSelectedLabels="0"
        class="w-80"
        :selectedItemsLabel="`${inputData.models.length} ${inputData.models.length === 1 ? 'Model' : 'Models'} selected`"
        :selectionLimit="3"
      />
      <div class="flex gap-2 mt-2">
        <Chip
          v-for="model in inputData.models"
          :key="model"
          :label="getModelById(model)?.name ?? model"
          removable
        >
          <template #removeicon>
            <i class="pi pi-times-circle" @click="removeModel(model)" />
          </template>
        </Chip>
      </div>
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Corpus</div>
      <FloatLabel variant="on">
        <Textarea
          id="on_label"
          v-model="inputData.corpus"
          rows="12"
          cols="120"
          :class="{ 'p-invalid': !isValid && inputData.corpus }"
          @input="validationSuccess = false"
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

    <div class="mt-6">
      <Button
        label="Start NER"
        icon="pi pi-play-circle"
        iconPos="left"
        :loading="postEvaluationIsLoading"
        :disabled="!isValid || inputData.models.length === 0"
        @click="submit"
      />
    </div>
  </div>
</template>
