import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Ranking', component: () => import('@/views/RankingView.vue') },
  ],
})

export default router
