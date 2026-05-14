import { createHttp } from '@tha/shared/utils/http'
import { ElMessage } from 'element-plus'
import router from '@/router'

const TOKEN_KEY = 'tha_admin_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export const http = createHttp({
  getToken,
  onAuthError: () => {
    removeToken()
    router.push('/login')
  },
  onError: (message: string) => {
    ElMessage.error(message)
  },
})
