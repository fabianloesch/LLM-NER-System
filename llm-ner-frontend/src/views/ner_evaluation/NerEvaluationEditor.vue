<script setup>
import { Button } from 'primevue'
import { ref, computed, onMounted, watch } from 'vue'
import router from '@/router'
import { useToast } from 'primevue/usetoast'
import { useRoute } from 'vue-router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'
import LLmSelector from '@/components/LLmSelector.vue'
import CorpusEditor from '@/components/ner_evaluation/NerEvaluationCorpusInput.vue'

const toast = useToast()
const route = useRoute()
const evaluationId = computed(() => route.params.evaluationId)

// Reference to CorpusEditor component
const corpusEditorRef = ref(null)

// Start NER Run
const {
  data: responsePostEvaluation,
  loading: postEvaluationIsLoading,
  error: postEvaluationError,
  execute: executeCreateEvaluation,
} = useApi(apiService.createEvaluation, null)

async function submit() {
  // Call validation from child component
  const isValid = corpusEditorRef.value?.validateInput()

  if (!isValid) {
    return
  }

  if (inputData.value.models.length === 0) {
    showError('Bitte wählen Sie mindestens ein Modell aus')
    return
  }

  const requestBody = {
    corpus: JSON.parse(inputData.value.corpus),
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

function showError(details) {
  toast.add({
    severity: 'error',
    summary: 'Error Message',
    detail: details,
    life: 5000,
  })
}

// Handle validation events from child
function handleValidationSuccess(message) {
  showSuccess(message)
}

function handleValidationError(errors) {
  showError(errors.join(' '))
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
      <LLmSelector :isSingleSelect="false" v-model:selectedModels="inputData.models" />
    </div>

    <div class="mb-5">
      <CorpusEditor
        ref="corpusEditorRef"
        v-model:corpus="inputData.corpus"
        @validationSuccess="handleValidationSuccess"
        @validationError="handleValidationError"
      />
    </div>

    <div class="mt-6">
      <Button
        label="Start NER"
        icon="pi pi-play-circle"
        iconPos="left"
        :loading="postEvaluationIsLoading"
        :disabled="!corpusEditorRef?.isValid || inputData.models.length === 0"
        @click="submit"
      />
    </div>
  </div>
</template>
