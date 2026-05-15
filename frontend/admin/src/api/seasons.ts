import { http } from '@/utils/http'
import type { ApiResponse, PaginatedResponse } from '@tha/shared/types/api'
import type { Season, SeasonCreate, SeasonUpdate } from '@tha/shared/types/season'

export function getSeasons(params?: { page?: number; page_size?: number }) {
  return http.get<any, PaginatedResponse<Season>>('/admin/seasons', { params })
}

export function createSeason(data: SeasonCreate) {
  return http.post<any, ApiResponse<Season>>('/admin/seasons', data)
}

export function updateSeason(id: number, data: SeasonUpdate) {
  return http.put<any, ApiResponse<Season>>(`/admin/seasons/${id}`, data)
}

export function activateSeason(id: number) {
  return http.post<any, ApiResponse<Season>>(`/admin/seasons/${id}/activate`)
}

export function closeSeason(id: number) {
  return http.post<any, ApiResponse<Season>>(`/admin/seasons/${id}/close`)
}

export function deleteSeason(id: number) {
  return http.delete<any, any>(`/admin/seasons/${id}`)
}
