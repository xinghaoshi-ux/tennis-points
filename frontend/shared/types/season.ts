import type { SeasonStatus } from './enums'

export interface Season {
  id: number
  name: string
  start_date: string
  end_date: string
  status: SeasonStatus
  created_at: string
  updated_at: string
}

export interface SeasonCreate {
  name: string
  start_date: string
  end_date: string
}

export interface SeasonUpdate {
  name?: string
  start_date?: string
  end_date?: string
}
