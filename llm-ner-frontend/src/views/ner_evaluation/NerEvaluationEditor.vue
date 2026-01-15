<script setup>
import { FloatLabel, Textarea, Chip, Button, MultiSelect, Message } from 'primevue'
import { ref, computed } from 'vue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { validateCorpus } from '@/utils/json_validation'
import { useToast } from 'primevue/usetoast'
const toast = useToast()

const modelsStore = useModelsStore()

// Select Model
const { availableModels, getModelById } = storeToRefs(modelsStore)
const selectedModels = ref(['openai/gpt-4.1-nano', 'google/gemini-2.0-flash-001'])
const removeModel = (modelId) => {
  const index = selectedModels.value.indexOf(modelId)
  if (index > -1) {
    selectedModels.value.splice(index, 1)
  }
}

// Enter Text
const inputCorpus = ref(`[
  {
    "id": 1,
    "text": "Der Patient sollte bei Asthma bronchiale Formoterol/Beclometason 6/100 µg als Dosieraerosol morgens und abends inhalativ versuchen.",
    "label": [
      [41, 64, "Drug"],
      [65, 73, "Strength"],
      [78, 91, "Form"],
      [92, 110, "Frequency"],
      [111, 120, "Form"]
    ]
  },
  {
    "id": 2,
    "text": "Wegen Ihrer erhöhten Zucker-Werte ist neben Metformin 1000 mg zweimal täglich auch Empagliflozin 10 mg einmal täglich - beides als Tablette - erforderlich.",
    "label": [
      [44, 53, "Drug"],
      [54, 61, "Strength"],
      [62, 77, "Frequency"],
      [83, 96, "Drug"],
      [97, 102, "Strength"],
      [103, 117, "Frequency"],
      [131, 139, "Form"]
    ]
  },
  {
    "id": 3,
    "text": "Nach aktueller ESC-Leitlinie müssen wir bei einem Ziel-LDL-Cholesterin von < 55 mg/dl neben Atorvastatin 80 mg abends oral außerdem Ezetimib 10 mg einmal täglich als Tablette nehmen. Bei Ezetimib ist egal, ob Sie es morgens oder abends schlucken. Wenn Sie sich für abends entscheiden, gibt es Kombinationsmittel mit 80/10 mg 0-0-1 als Tablette. Dann sind es nicht mehr 2 Tabletten.",
    "label": [
      [92, 104, "Drug"],
      [105, 110, "Strength"],
      [111, 117, "Frequency"],
      [132, 140, "Drug"],
      [141, 146, "Strength"],
      [147, 161, "Frequency"],
      [166, 174, "Form"],
      [187, 195, "Drug"],
      [216, 235, "Frequency"],
      [265, 271, "Frequency"],
      [316, 324, "Strength"],
      [335, 343, "Form"],
      [369, 370, "Dosage"],
      [371, 380, "Form"]
    ]
  },
  {
    "id": 4,
    "text": "Das Eplerenon ist wegen Ihrer Herzinsuffizienz. Da können wir jetzt auf 50 mg p.o. 1-0-0 augmentieren.",
    "label": [
      [4, 13, "Drug"],
      [72, 77, "Strength"]
    ]
  },
  {
    "id": 5,
    "text": "Nach dieser hypertensiven Entgleisung empfehlen wir zunächst eine Therapie mit Olmesartan/Amlodipin 20/5 mg in oraler Applikation. Hierfür kann beispielsweise das Kombinationspräparat Sevikar 20/5 mg verwendet werden. Die Einnahme erfolgt stets in der Früh um ca. 8.00 Uhr.",
    "label": [
      [79, 99, "Drug"],
      [100, 107, "Strength"],
      [184, 191, "Drug"],
      [192, 199, "Strength"],
      [245, 256, "Frequency"]
    ]
  },
  {
    "id": 6,
    "text": "Zur Optimierung der Herzinsuffizienztherapie wurde die Dosis von Sacubitril/Valsartan auf 97/103 mg in Tablettenform mit Einnahme am Morgen und am Abend erweitert.",
    "label": [
      [65, 85, "Drug"],
      [90, 99, "Strength"],
      [103, 116, "Form"],
      [130, 152, "Frequency"]
    ]
  }]`)

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
