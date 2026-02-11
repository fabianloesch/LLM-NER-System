<script setup>
import { InputGroup, InputText, Button, Chip } from 'primevue'
import { defineModel, ref } from 'vue'

const entityClasses = defineModel('entityClasses', { type: Array })

// Add Label
const newEntity = ref(null)
const addEntityClass = () => {
  entityClasses.value.push(newEntity.value)
  newEntity.value = null
}

// Remove Label
const removeEntityClass = (entityClass) => {
  const index = entityClasses.value.indexOf(entityClass)
  if (index > -1) {
    entityClasses.value.splice(index, 1)
  }
}
</script>

<template>
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
    <Chip v-for="entityClass in entityClasses" :label="entityClass" removable>
      <template #removeicon>
        <i class="pi pi-times-circle" @click="removeEntityClass(entityClass)" />
      </template>
    </Chip>
  </div>
</template>
