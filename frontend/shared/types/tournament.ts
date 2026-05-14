import type { EventCategory, TournamentLevel, TournamentStatus } from './enums'

export interface Tournament {
  id: number
  name: string
  season_id: number
  event_category: EventCategory
  level: TournamentLevel
  group_name?: string
  location?: string
  tournament_date?: string
  status: TournamentStatus
  created_at: string
  updated_at: string
}

export interface TournamentCreate {
  name: string
  event_category: EventCategory
  level: TournamentLevel
  group_name?: string
  location?: string
  tournament_date?: string
}

export interface TournamentUpdate {
  name?: string
  event_category?: EventCategory
  level?: TournamentLevel
  group_name?: string
  location?: string
  tournament_date?: string
}
