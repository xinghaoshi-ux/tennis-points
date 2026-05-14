import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getMe } from '@/api/auth'
import { setToken, removeToken, getToken } from '@/utils/http'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<{ id: number; username: string; display_name: string } | null>(null)
  const isAuthenticated = computed(() => !!getToken())

  async function login(username: string, password: string) {
    const res = await loginApi({ username, password })
    setToken(res.data.access_token)
    user.value = res.data.user
  }

  async function fetchMe() {
    try {
      const res = await getMe()
      user.value = res.data
    } catch {
      logout()
    }
  }

  function logout() {
    removeToken()
    user.value = null
    router.push('/login')
  }

  return { user, isAuthenticated, login, fetchMe, logout }
})
