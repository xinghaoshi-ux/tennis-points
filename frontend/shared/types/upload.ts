import type { UploadStatus, RowStatus } from './enums'

export interface Upload {
  id: number
  tournament_id: number
  filename: string
  status: UploadStatus
  total_rows?: number
  valid_rows?: number
  error_rows?: number
  error_log?: string
  uploaded_by: number
  created_at: string
}

export interface UploadPreviewRow {
  row_number: number
  tournament_name?: string
  level?: string
  group_name?: string
  result_type?: string
  player1_name?: string
  player1_id?: number
  player1_matched: boolean
  player2_name?: string
  player2_id?: number
  player2_matched: boolean
  is_cross_province?: boolean
  is_cross_border?: boolean
  estimated_points?: number
  row_status: RowStatus
  error_message?: string
}

export interface ConfirmImportRequest {
  confirmed_rows: number[]
  ignored_rows: number[]
}
