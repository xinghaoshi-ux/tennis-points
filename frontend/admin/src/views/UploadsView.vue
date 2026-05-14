<template>
  <div class="page-container">
    <div class="page-header">
      <h2>Excel 导入</h2>
      <el-tooltip content="即将上线" placement="top">
        <el-button disabled>下载模板</el-button>
      </el-tooltip>
    </div>

    <el-steps :active="step" finish-status="success" style="margin-bottom: 24px">
      <el-step title="选择赛事" />
      <el-step title="上传文件" />
      <el-step title="解析中" />
      <el-step title="预览确认" />
      <el-step title="完成" />
    </el-steps>

    <!-- Step 0: Select tournament -->
    <div v-if="step === 0">
      <el-select v-model="selectedTournamentId" placeholder="选择目标赛事" style="width: 300px" filterable>
        <el-option v-for="t in draftTournaments" :key="t.id" :label="t.name" :value="t.id" />
      </el-select>
      <el-button type="primary" :disabled="!selectedTournamentId" style="margin-left: 12px" @click="step = 1">
        下一步
      </el-button>
    </div>

    <!-- Step 1: Upload file -->
    <div v-if="step === 1">
      <el-upload
        drag
        :auto-upload="false"
        accept=".xlsx,.xls"
        :limit="1"
        :on-change="handleFileChange"
      >
        <el-icon style="font-size: 48px; color: #c0c4cc"><Upload /></el-icon>
        <div>将 Excel 文件拖到此处，或<em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip">仅支持 .xlsx / .xls 格式，最大 10MB</div>
        </template>
      </el-upload>
      <el-button type="primary" :disabled="!selectedFile" :loading="uploading" style="margin-top: 16px" @click="handleUpload">
        上传并解析
      </el-button>
    </div>

    <!-- Step 2: Parsing -->
    <div v-if="step === 2" style="text-align: center; padding: 40px">
      <el-icon class="is-loading" style="font-size: 32px; color: #409eff"><Loading /></el-icon>
      <p>正在解析文件，请稍候...</p>
    </div>

    <!-- Step 3: Preview -->
    <div v-if="step === 3">
      <div style="margin-bottom: 12px">
        <span>总行数：{{ previewRows.length }}</span>
        <span style="margin-left: 16px; color: #67c23a">正常：{{ normalCount }}</span>
        <span style="margin-left: 16px; color: #e6a23c">警告：{{ warningCount }}</span>
        <span style="margin-left: 16px; color: #f56c6c">错误：{{ errorCount }}</span>
      </div>
      <el-table :data="previewRows" border max-height="400" size="small">
        <el-table-column type="selection" width="40" :selectable="(row: any) => row.row_status !== 'error'" />
        <el-table-column prop="row_number" label="#" width="50" />
        <el-table-column prop="player1_name" label="选手1" width="100" />
        <el-table-column prop="player2_name" label="选手2" width="100" />
        <el-table-column prop="result_type" label="成绩" width="80" />
        <el-table-column prop="estimated_points" label="预估积分" width="80" />
        <el-table-column prop="row_status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.row_status === 'normal' ? 'success' : row.row_status === 'warning' ? 'warning' : 'danger'" size="small">
              {{ { normal: '正常', warning: '警告', error: '错误' }[row.row_status as string] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error_message" label="说明" />
      </el-table>
      <div style="margin-top: 16px; display: flex; gap: 12px">
        <el-button type="primary" :loading="confirming" @click="handleConfirm">确认导入</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </div>
    </div>

    <!-- Step 4: Done -->
    <div v-if="step === 4" style="text-align: center; padding: 40px">
      <el-icon style="font-size: 48px; color: #67c23a"><CircleCheck /></el-icon>
      <p>导入完成</p>
      <el-button @click="reset">继续导入</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Loading, CircleCheck } from '@element-plus/icons-vue'
import { uploadExcel, getUploadStatus, getUploadPreview, confirmImport, cancelUpload } from '@/api/uploads'
import { getTournaments } from '@/api/tournaments'
import { usePolling } from '@tha/shared/utils/polling'
import type { Tournament } from '@tha/shared/types/tournament'
import type { UploadPreviewRow } from '@tha/shared/types/upload'

const step = ref(0)
const draftTournaments = ref<Tournament[]>([])
const selectedTournamentId = ref<number | null>(null)
const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const confirming = ref(false)
const uploadId = ref<number | null>(null)
const previewRows = ref<UploadPreviewRow[]>([])

const normalCount = computed(() => previewRows.value.filter(r => r.row_status === 'normal').length)
const warningCount = computed(() => previewRows.value.filter(r => r.row_status === 'warning').length)
const errorCount = computed(() => previewRows.value.filter(r => r.row_status === 'error').length)

function handleFileChange(file: any) {
  selectedFile.value = file.raw
}

async function handleUpload() {
  if (!selectedFile.value || !selectedTournamentId.value) return
  uploading.value = true
  try {
    const res = await uploadExcel(selectedFile.value, selectedTournamentId.value)
    uploadId.value = res.data.id
    step.value = 2
    startPolling()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

const { start: startPolling, stop: stopPolling } = usePolling(async () => {
  if (!uploadId.value) return true
  const res = await getUploadStatus(uploadId.value)
  const status = res.data.status
  if (status === 'parsed') {
    stopPolling()
    const preview = await getUploadPreview(uploadId.value)
    previewRows.value = preview.data
    step.value = 3
    return true
  }
  if (status === 'parse_failed') {
    stopPolling()
    ElMessage.error(res.data.error_log || '解析失败')
    step.value = 1
    return true
  }
  return false
})

async function handleConfirm() {
  if (!uploadId.value) return
  confirming.value = true
  const confirmed = previewRows.value.filter(r => r.row_status !== 'error').map(r => r.row_number)
  const ignored = previewRows.value.filter(r => r.row_status === 'error').map(r => r.row_number)
  try {
    await confirmImport(uploadId.value, { confirmed_rows: confirmed, ignored_rows: ignored })
    step.value = 4
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '确认失败')
  } finally {
    confirming.value = false
  }
}

async function handleCancel() {
  if (!uploadId.value) return
  try {
    await cancelUpload(uploadId.value)
    ElMessage.info('已取消')
    reset()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '取消失败')
  }
}

function reset() {
  step.value = 0
  selectedFile.value = null
  uploadId.value = null
  previewRows.value = []
}

async function fetchTournaments() {
  try {
    const res = await getTournaments({ page: 1, page_size: 100, status: 'draft' })
    draftTournaments.value = res.data
  } catch { /* ignore */ }
}

onMounted(fetchTournaments)
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; font-size: 18px; }
</style>
