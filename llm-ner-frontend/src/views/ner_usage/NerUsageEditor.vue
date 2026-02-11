<script setup>
import { Select, FloatLabel, Textarea, Chip, InputGroup, Button, InputText } from 'primevue'
import { ref, onMounted, computed } from 'vue'
import { useModelsStore } from '@/stores/models'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { useRoute } from 'vue-router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'

const modelsStore = useModelsStore()
const route = useRoute()
const usageId = computed(() => route.params.usageId)

// Select Model
const { availableModels } = storeToRefs(modelsStore)

// Remove Label
const removeEntityClass = (entityClass) => {
  const index = templateModelRun.value.entity_classes.indexOf(entityClass)
  if (index > -1) {
    templateModelRun.value.entity_classes.splice(index, 1)
  }
}

// Add Label
const newEntity = ref(null)
const addEntityClass = () => {
  templateModelRun.value.entity_classes.push(newEntity.value)
  newEntity.value = null
}

// Start NER Run
const {
  data: responsePostModelRun,
  loading: postModelRunIsLoading,
  error: postModelRunError,
  execute: executeCreateModelRun,
} = useApi(apiService.createModelRun, null)

async function submit() {
  const requestBody = {
    text: templateModelRun.value.text,
    entity_classes: templateModelRun.value.entity_classes,
    llm_id: templateModelRun.value.model,
  }
  await executeCreateModelRun(requestBody)
  router.push({
    name: 'usage',
    params: { usageId: responsePostModelRun.value._id },
  })
}

// Get Model Run As Template
const templateModelRun = ref({
  _id: null,
  created_datetime_utc: null,
  text: null,
  entity_classes: null,
  model: null,
  entities: null,
})

const {
  data: responseGetModelRun,
  loading: getModelRunIsLoading,
  error: getModelRunError,
  execute: executeGetModelRun,
} = useApi(apiService.getModelRunById, templateModelRun)

onMounted(() => {
  if (usageId.value) {
    executeGetModelRun(usageId.value)
  }
})
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Task Editor</div>
    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Model</div>
      <Select
        v-model="templateModelRun.model"
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
        <Chip v-for="entityClass in templateModelRun.entity_classes" :label="entityClass" removable>
          <template #removeicon>
            <i class="pi pi-times-circle" @click="removeEntityClass(entityClass)" />
          </template>
        </Chip>
      </div>
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Text</div>
      <FloatLabel variant="on">
        <Textarea id="on_label" v-model="templateModelRun.text" rows="12" cols="120" />
        <label for="on_label">Enter a Text</label>
      </FloatLabel>
    </div>

    <div>
      <Button
        label="Start NER"
        icon="pi pi-play-circle"
        iconPos="left"
        :loading="postModelRunIsLoading"
        @click="submit()"
      />
    </div>
  </div>
</template>
