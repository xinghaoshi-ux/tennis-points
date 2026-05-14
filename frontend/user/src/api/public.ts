import { createHttp } from '@tha/shared/utils/http'
import type { PaginatedResponse, ApiResponse } from '@tha/shared/types/api'
import type { RankingItem, PlayerPointsDetail } from '@tha/shared/types/ranking'

const http = createHttp()

export function getCurrentSeason() {
  return http.get<any, ApiResponse<any>>('/public/seasons/current')
}

export function getRankings(params?: { page?: number; page_size?: number; search?: string; department?: string }) {
  return http.get<any, PaginatedResponse<RankingItem>>('/public/rankings', { params })
}

export function getPlayerPoints(playerId: number) {
  return http.get<any, ApiResponse<PlayerPointsDetail>>(`/public/players/${playerId}/points`)
}

export function getDepartments() {
  return http.get<any, ApiResponse<string[]>>('/public/departments')
}
