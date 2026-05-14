export interface DashboardData {
  current_season?: {
    id: number
    name: string
    status: string
  }
  player_count: number
  tournament_count: number
  points_record_count: number
  recent_uploads: RecentUpload[]
}

export interface RecentUpload {
  id: number
  filename: string
  status: string
  created_at: string
  tournament_name?: string
}
