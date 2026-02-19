import AppLayout from '@/layout/AppLayout.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '/',
          redirect: '/usage/new',
        },
        {
          path: '/usage',
          redirect: '/usage/new',
        },
        {
          path: '/usage/new/:usageId?',
          name: 'new-ner-run',
          component: () => import('@/views/ner_usage/NerUsageEditor.vue'),
        },
        {
          path: '/usage/:usageId',
          name: 'usage',
          component: () => import('@/views/ner_usage/NerUsageDisplay.vue'),
        },
        {
          path: '/usage/history',
          name: 'usage-history',
          component: () => import('@/views/ner_usage/NerUsageHistory.vue'),
        },
        {
          path: '/evaluation/new/:evaluationId?',
          name: 'new-ner-evaluation',
          component: () => import('@/views/ner_evaluation/NerEvaluationEditor.vue'),
        },
        {
          path: '/evaluation/:evaluationId',
          name: 'evaluation',
          component: () => import('@/views/ner_evaluation/NerEvaluationDisplay.vue'),
        },
        {
          path: '/evaluation/history',
          name: 'evaluation-history',
          component: () => import('@/views/ner_evaluation/NerEvaluationHistory.vue'),
        },
        {
          path: '/documentation',
          name: 'documentation',
          component: () => import('@/views/misc/Documentation.vue'),
        },
      ],
    },
  ],
})

export default router
