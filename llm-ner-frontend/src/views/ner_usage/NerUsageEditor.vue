<script setup>
import { Button } from 'primevue'
import { ref, onMounted, computed } from 'vue'
import router from '@/router'
import { useRoute } from 'vue-router'
import { useApi } from '@/service/UseLlmNerSystemApi'
import { apiService } from '@/service/LlmNerSystemService'
import NerUsageTextArea from '@/components/NerUsageTextArea.vue'
import NerUsageLabelSelector from '@/components/NerUsageLabelSelector.vue'
import NerUsageModelSelector from '@/components/NerUsageModelSelector.vue'

const route = useRoute()
const usageId = computed(() => route.params.usageId)

onMounted(() => {
  if (usageId.value) {
    executeGetModelRun(usageId.value)
  }
})

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
  console.log(requestBody)
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
  entity_classes: [],
  model: null,
  entities: null,
})

const {
  data: responseGetModelRun,
  loading: getModelRunIsLoading,
  error: getModelRunError,
  execute: executeGetModelRun,
} = useApi(apiService.getModelRunById, templateModelRun)
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Task Editor</div>
    <div class="mb-5">
      <NerUsageModelSelector v-model:selectedModel="templateModelRun.model" />
    </div>

    <div class="mb-5">
      <NerUsageLabelSelector v-model:entityClasses="templateModelRun.entity_classes" />
    </div>

    <div class="mb-5">
      <NerUsageTextArea v-model:inputText="templateModelRun.text" />
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
