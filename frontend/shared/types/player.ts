import type { Gender, PlayerStatus } from './enums'

export interface Player {
  id: number
  full_name: string
  gender?: Gender
  birth_date?: string
  department?: string
  status: PlayerStatus
  created_at: string
  updated_at: string
}

export interface PlayerCreate {
  full_name: string
  gender?: Gender
  birth_date?: string
  department?: string
}

export interface PlayerUpdate {
  full_name?: string
  gender?: Gender
  birth_date?: string
  department?: string
  status?: PlayerStatus
}
