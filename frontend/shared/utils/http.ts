import axios, { type AxiosInstance, type AxiosError } from 'axios'
import type { ApiError } from '../types/api'

export interface HttpOptions {
  getToken?: () => string | null
  onAuthError?: () => void
  onError?: (message: string) => void
}

export function createHttp(options: HttpOptions = {}): AxiosInstance {
  const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    timeout: 15000,
    headers: { 'Content-Type': 'application/json' },
  })

  instance.interceptors.request.use((config) => {
    if (options.getToken) {
      const token = options.getToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  })

  instance.interceptors.response.use(
    (response) => response.data,
    (error: AxiosError<ApiError>) => {
      if (!error.response) {
        options.onError?.('网络异常，请检查网络连接')
        return Promise.reject(error)
      }

      const { status, data } = error.response
      const code = data?.code

      if (status === 401 || code === 'AUTH_TOKEN_MISSING' || code === 'AUTH_TOKEN_EXPIRED' || code === 'AUTH_TOKEN_INVALID') {
        options.onAuthError?.()
        return Promise.reject(error)
      }

      if (status === 429 || code === 'RATE_LIMITED') {
        options.onError?.('操作过于频繁，请稍后重试')
        return Promise.reject(error)
      }

      if (status >= 500) {
        options.onError?.('系统异常，请稍后重试')
        return Promise.reject(error)
      }

      return Promise.reject(error)
    }
  )

  return instance
}
