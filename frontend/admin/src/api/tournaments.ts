import { http } from '@/utils/http'
import type { ApiResponse, PaginatedResponse } from '@tha/shared/types/api'
import type { Tournament, TournamentCreate, TournamentUpdate } from '@tha/shared/types/tournament'

export function getTournaments(params?: { page?: number; page_size?: number; status?: string; season_id?: number }) {
  return http.get<any, PaginatedResponse<Tournament>>('/admin/tournaments', { params })
}

export function getTournament(id: number) {
  return http.get<any, ApiResponse<Tournament>>(`/admin/tournaments/${id}`)
}

export function createTournament(data: TournamentCreate) {
  return http.post<any, ApiResponse<Tournament>>('/admin/tournaments', data)
}

export function updateTournament(id: number, data: TournamentUpdate) {
  return http.put<any, ApiResponse<Tournament>>(`/admin/tournaments/${id}`, data)
}

export function generatePoints(id: number) {
  return http.post<any, ApiResponse<any>>(`/admin/tournaments/${id}/generate-points`)
}

export function revokePublish(id: number) {
  return http.post<any, ApiResponse<any>>(`/admin/tournaments/${id}/revoke-publish`)
}
