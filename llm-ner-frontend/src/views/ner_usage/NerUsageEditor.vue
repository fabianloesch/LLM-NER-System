<script setup>
import { Select, FloatLabel, Textarea, Chip, InputGroup, Button, InputText } from 'primevue'
</script>

<template>
  <div class="card">
    <div class="font-semibold text-2xl mb-5">NER Usage Editor</div>
    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Model</div>
      <Select
        v-model="selectedCity"
        :options="cities"
        showClear
        optionLabel="name"
        placeholder="Select a Model"
        size="medium"
        class="w-80"
      />
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Labels</div>
      <div class="w-80 mb-2">
        <InputGroup>
          <InputText placeholder="Add an Entity Label" />
          <Button label="Add" />
        </InputGroup>
      </div>
      <div>
        <Chip label="Action" removable />
        <Chip label="Comedy" removable />
        <Chip label="Mystery" removable />
        <Chip label="Thriller" removable />
      </div>
    </div>

    <div class="mb-5">
      <div class="font-semibold text-xl mb-2">Text</div>
      <FloatLabel variant="on">
        <Textarea id="on_label" v-model="value3" rows="12" cols="120" />
        <label for="on_label">Enter a Text</label>
      </FloatLabel>
    </div>

    <div>
      <Button label="Start NER" icon="pi pi-play-circle" iconPos="left" />
    </div>
  </div>
</template>
