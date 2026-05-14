import { http } from '@/utils/http'
import type { ApiResponse } from '@tha/shared/types/api'
import type { PointsRule, PointsRuleCreate, PointsRuleUpdate } from '@tha/shared/types/pointsRule'

export function getPointsRules(params?: { season_id?: number; rule_type?: string }) {
  return http.get<any, ApiResponse<PointsRule[]>>('/admin/points-rules', { params })
}

export function createPointsRule(data: PointsRuleCreate) {
  return http.post<any, ApiResponse<PointsRule>>('/admin/points-rules', data)
}

export function updatePointsRule(id: number, data: PointsRuleUpdate) {
  return http.put<any, ApiResponse<PointsRule>>(`/admin/points-rules/${id}`, data)
}

export function deletePointsRule(id: number) {
  return http.delete<any, ApiResponse<any>>(`/admin/points-rules/${id}`)
}
