import { http } from '@/utils/http'
import type { ApiResponse, PaginatedResponse } from '@tha/shared/types/api'
import type { Player, PlayerCreate, PlayerUpdate } from '@tha/shared/types/player'

export function getPlayers(params?: { page?: number; page_size?: number; search?: string; department?: string }) {
  return http.get<any, PaginatedResponse<Player>>('/admin/players', { params })
}

export function getPlayer(id: number) {
  return http.get<any, ApiResponse<Player>>(`/admin/players/${id}`)
}

export function createPlayer(data: PlayerCreate) {
  return http.post<any, ApiResponse<Player>>('/admin/players', data)
}

export function updatePlayer(id: number, data: PlayerUpdate) {
  return http.put<any, ApiResponse<Player>>(`/admin/players/${id}`, data)
}

export function deletePlayer(id: number) {
  return http.delete<any, any>(`/admin/players/${id}`)
}
