import type { RuleType, TournamentLevel, ResultType } from './enums'

export interface PointsRule {
  id: number
  season_id: number
  rule_type: RuleType
  event_level?: TournamentLevel
  group_name?: string
  result_type?: ResultType
  points: number
  description?: string
  created_at: string
  updated_at: string
}

export interface PointsRuleCreate {
  rule_type: RuleType
  event_level?: TournamentLevel
  group_name?: string
  result_type?: ResultType
  points: number
  description?: string
}

export interface PointsRuleUpdate {
  rule_type?: RuleType
  event_level?: TournamentLevel
  group_name?: string
  result_type?: ResultType
  points?: number
  description?: string
}
