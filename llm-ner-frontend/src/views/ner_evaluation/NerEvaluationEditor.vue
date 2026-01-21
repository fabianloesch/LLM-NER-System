<script setup>
import { FloatLabel, Textarea, Chip, Button, MultiSelect, Message } from 'primevue'
import { ref, computed, onMounted } from 'vue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { validateCorpus } from '@/utils/json_validation'
import { useToast } from 'primevue/usetoast'
import { useRoute } from 'vue-router'

const toast = useToast()
const modelsStore = useModelsStore()
const route = useRoute()
const evaluationId = computed(() => route.params.evaluationId)

// Select Model
const { availableModels, getModelById } = storeToRefs(modelsStore)
const selectedModels = ref([])
const removeModel = (modelId) => {
  const index = selectedModels.value.indexOf(modelId)
  if (index > -1) {
    selectedModels.value.splice(index, 1)
  }
}

// Enter Text
const inputCorpus = ref([])

// Validation
const validationErrors = ref([])
const validationSuccess = ref(false)
const isValid = computed(() => validationErrors.value.length === 0)

function validateInput() {
  validationSuccess.value = false

  if (!inputCorpus.value || inputCorpus.value.trim() === '') {
    validationErrors.value = ['Bitte geben Sie einen Input-Corpus ein.']
    showError(validationErrors.value.join(' '))
    return false
  }

  validationErrors.value = validateCorpus(inputCorpus.value)

  if (validationErrors.value.length === 0) {
    validationSuccess.value = true
    showSuccess('Validierung erfolgreich! Der Input-Corpus entspricht dem erwarteten Schema.')
  } else {
    showError(validationErrors.value.join(' '))
  }

  return validationErrors.value.length === 0
}

// Start NER Evaluation
const isLoading = ref(false)
const error = ref(null)
const evaluationResult = ref(null)

async function postNerEvaluation() {
  isLoading.value = true
  error.value = null

  const myHeaders = new Headers()
  myHeaders.append('Content-Type', 'application/json')

  const raw = JSON.stringify({
    corpus: JSON.parse(inputCorpus.value), // Parse the JSON before sending
    llm_ids: selectedModels.value,
  })

  const requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/modelEvaluation', requestOptions)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    evaluationResult.value = data.result
  } catch (err) {
    console.error('Fehler beim Start der NER-Evaluation', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

async function submit() {
  if (!validateInput()) {
    return
  }

  if (selectedModels.value.length === 0) {
    validationErrors.value = ['Bitte wählen Sie mindestens ein Modell aus']
    return
  }

  await postNerEvaluation()

  if (evaluationResult.value?._id) {
    router.push({
      name: 'evaluation',
      params: { evaluationId: evaluationResult.value._id },
    })
  }
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

async function fetchNerEvaluation(evaluationId) {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/modelEvaluation/${evaluationId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    selectedModels.value = [...data.result.models]
    inputCorpus.value = JSON.stringify(data.result.corpus, null, 2)
  } catch (err) {
    console.error('Fehler beim Laden der Evaluation:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (evaluationId.value) {
    fetchNerEvaluation(evaluationId.value)
  }
})
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Evaluation Editor</div>

    <!-- API Error -->
    <div v-if="error" class="mb-5">
      <Message severity="error" :closable="false"> API-Fehler: {{ error }} </Message>
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Model</div>
      <MultiSelect
        v-model="selectedModels"
        :options="availableModels"
        filter
        showClear
        optionLabel="name"
        optionValue="id"
        placeholder="Select a Model"
        size="medium"
        :maxSelectedLabels="0"
        class="w-80"
        :selectedItemsLabel="`${selectedModels.length} ${selectedModels.length === 1 ? 'Model' : 'Models'} selected`"
        :selectionLimit="3"
      />
      <div class="flex gap-2 mt-2">
        <Chip
          v-for="model in selectedModels"
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
          v-model="inputCorpus"
          rows="12"
          cols="120"
          :class="{ 'p-invalid': !isValid && inputCorpus }"
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
        :loading="isLoading"
        :disabled="!isValid || selectedModels.length === 0"
        @click="submit"
      />
    </div>
  </div>
</template>
