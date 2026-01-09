<script setup>
import { ref } from 'vue'

import AppMenuItem from './AppMenuItem.vue'

const model = ref([
  {
    label: 'Usage',
    items: [
      { label: 'New NER Run', icon: 'pi pi-fw pi-play-circle', to: '/usage/new' },
      { label: 'Usage History', icon: 'pi pi-fw pi-history', to: '/usage/history' },
    ],
  },
  {
    label: 'Evaluation',
    items: [
      { label: 'New NER Evaluation', icon: 'pi pi-fw pi-gauge', to: '/evaluation/new' },
      { label: 'Evaluation History', icon: 'pi pi-fw pi-history', to: '/evaluation/history' },
    ],
  },
  {
    label: 'Get Started',
    items: [
      {
        label: 'Documentation',
        icon: 'pi pi-fw pi-book',
        to: '/documentation',
      },
      {
        label: 'View Source',
        icon: 'pi pi-fw pi-github',
        url: 'https://github.com/fabianloesch/LLM-NER-System',
        target: '_blank',
      },
    ],
  },
])
</script>

<template>
  <ul class="layout-menu">
    <template v-for="(item, i) in model" :key="item">
      <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
      <li v-if="item.separator" class="menu-separator"></li>
    </template>
  </ul>
</template>

<style lang="scss" scoped></style>
