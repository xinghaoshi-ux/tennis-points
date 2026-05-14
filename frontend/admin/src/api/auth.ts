import { http } from '@/utils/http'
import type { ApiResponse } from '@tha/shared/types/api'

interface LoginRequest {
  username: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: { id: number; username: string; display_name: string }
}

interface UserInfo {
  id: number
  username: string
  display_name: string
}

export function login(data: LoginRequest) {
  return http.post<any, ApiResponse<LoginResponse>>('/admin/auth/login', data)
}

export function getMe() {
  return http.get<any, ApiResponse<UserInfo>>('/admin/auth/me')
}
