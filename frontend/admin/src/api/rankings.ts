import { http } from '@/utils/http'
import type { PaginatedResponse, ApiResponse } from '@tha/shared/types/api'
import type { RankingItem, PlayerPointsDetail } from '@tha/shared/types/ranking'

export function getRankings(params?: { page?: number; page_size?: number; search?: string; department?: string }) {
  return http.get<any, PaginatedResponse<RankingItem>>('/admin/rankings', { params })
}

export function refreshRankings() {
  return http.post<any, ApiResponse<any>>('/admin/rankings/refresh')
}

export function getPlayerPoints(playerId: number) {
  return http.get<any, ApiResponse<PlayerPointsDetail>>(`/public/players/${playerId}/points`)
}
