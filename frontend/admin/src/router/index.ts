import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/http'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/dashboard' },
        { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
        { path: 'seasons', name: 'Seasons', component: () => import('@/views/SeasonsView.vue') },
        { path: 'players', name: 'Players', component: () => import('@/views/PlayersView.vue') },
        { path: 'tournaments', name: 'Tournaments', component: () => import('@/views/TournamentsView.vue') },
        { path: 'points-rules', name: 'PointsRules', component: () => import('@/views/PointsRulesView.vue') },
        { path: 'uploads', name: 'Uploads', component: () => import('@/views/UploadsView.vue') },
        { path: 'rankings', name: 'Rankings', component: () => import('@/views/RankingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth !== false && !getToken()) {
    return '/login'
  }
})

export default router
