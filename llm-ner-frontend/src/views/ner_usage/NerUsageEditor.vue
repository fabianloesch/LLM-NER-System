<script setup>
import { Select, FloatLabel, Textarea, Chip, InputGroup, Button, InputText } from 'primevue'
import { ref, onMounted, computed } from 'vue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { useRoute } from 'vue-router'

const modelsStore = useModelsStore()
const route = useRoute()
const usageId = computed(() => route.params.usageId)

// Select Model
const { availableModels } = storeToRefs(modelsStore)
const selectedModel = ref(null)

// Remove Label
const entityclasses = ref([])
const removeEntityClass = (entityClass) => {
  const index = entityclasses.value.indexOf(entityClass)
  if (index > -1) {
    entityclasses.value.splice(index, 1)
  }
}

// Add Label
const newEntity = ref(null)
const addEntityClass = () => {
  entityclasses.value.push(newEntity.value)
  newEntity.value = null
}

// Enter Text
const inputText = ref(null)

// Start NER Run
const isLoading = ref(false)
const error = ref(null)

const nerResult = ref(null)

async function postNerModelRun() {
  isLoading.value = true
  error.value = null

  const myHeaders = new Headers()
  myHeaders.append('Content-Type', 'application/json')

  const raw = JSON.stringify({
    text: inputText.value,
    entity_classes: entityclasses.value,
    llm_id: selectedModel.value,
  })

  const requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/modelRun', requestOptions)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    nerResult.value = data.result
  } catch (err) {
    console.error('Fehler beim Start des NER-Durchlaufs', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

async function submit() {
  await postNerModelRun()
  // const id = nerResult.value._id
  router.push({
    name: 'usage',
    params: { usageId: nerResult.value._id },
  })
}

const templateModelRun = ref({})

async function fetchNerRun(modelRunId) {
  isLoading.value = true
  error.value = null

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/modelRun/${modelRunId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    templateModelRun.value = data.result
    inputText.value = data.result.text
    selectedModel.value = data.result.model
    entityclasses.value = data.result.entity_classes
  } catch (err) {
    console.error('Fehler beim Laden des Modeldurchlaufs:', err)
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (usageId.value) {
    fetchNerRun(usageId.value)
  }
})
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Usage Editor</div>
    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Model</div>
      <Select
        v-model="selectedModel"
        :options="availableModels"
        showClear
        filter
        optionLabel="name"
        optionValue="id"
        placeholder="Select a Model"
        size="medium"
        class="w-80"
      />
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Labels</div>
      <div class="w-80 mb-2">
        <InputGroup>
          <InputText
            placeholder="Add an Entity Label"
            v-model="newEntity"
            @keyup.enter="addEntityClass"
          />
          <Button label="Add" @click="addEntityClass" />
        </InputGroup>
      </div>
      <div>
        <Chip v-for="entityClass in entityclasses" :label="entityClass" removable>
          <template #removeicon>
            <i class="pi pi-times-circle" @click="removeEntityClass(entityClass)" />
          </template>
        </Chip>
      </div>
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Text</div>
      <FloatLabel variant="on">
        <Textarea id="on_label" v-model="inputText" rows="12" cols="120" />
        <label for="on_label">Enter a Text</label>
      </FloatLabel>
    </div>

    <div>
      <Button
        label="Start NER"
        icon="pi pi-play-circle"
        iconPos="left"
        :loading="isLoading"
        @click="submit()"
      />
    </div>
  </div>
</template>
