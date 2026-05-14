import { http } from '@/utils/http'
import type { ApiResponse } from '@tha/shared/types/api'
import type { Upload, UploadPreviewRow, ConfirmImportRequest } from '@tha/shared/types/upload'

export function uploadExcel(file: File, tournamentId: number) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('tournament_id', String(tournamentId))
  return http.post<any, ApiResponse<Upload>>('/admin/uploads', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getUploadStatus(id: number) {
  return http.get<any, ApiResponse<Upload>>(`/admin/uploads/${id}`)
}

export function getUploadPreview(id: number) {
  return http.get<any, ApiResponse<UploadPreviewRow[]>>(`/admin/uploads/${id}/preview`)
}

export function confirmImport(id: number, data: ConfirmImportRequest) {
  return http.post<any, ApiResponse<any>>(`/admin/uploads/${id}/confirm`, data)
}

export function cancelUpload(id: number) {
  return http.post<any, ApiResponse<any>>(`/admin/uploads/${id}/cancel`)
}
