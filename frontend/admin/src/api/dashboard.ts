import { http } from '@/utils/http'
import type { ApiResponse } from '@tha/shared/types/api'
import type { DashboardData } from '@tha/shared/types/dashboard'

export function getDashboard() {
  return http.get<any, ApiResponse<DashboardData>>('/admin/dashboard')
}
