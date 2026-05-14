import type { SourceType } from './enums'

export interface RankingItem {
  ranking: number
  player_id: number
  full_name: string
  department?: string
  age?: number
  total_points: number
  tournament_count: number
}

export interface PlayerPointsDetail {
  player: {
    id: number
    full_name: string
    department?: string
    gender?: string
  }
  summary: {
    individual_event: number
    team_share: number
    travel_bonus: number
    representative_team: number
    organizer_bonus: number
    donation_bonus: number
  }
  details: PointsRecord[]
}

export interface PointsRecord {
  id: number
  tournament_name: string
  source_type: SourceType
  points: number
  created_at: string
}
