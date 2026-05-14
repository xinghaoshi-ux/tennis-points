<template>
  <div class="page-container">
    <h2 style="margin-bottom: 24px">仪表盘</h2>

    <el-row :gutter="16" style="margin-bottom: 24px">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-label">当前赛季</div>
          <div class="stat-value">{{ dashboard?.current_season?.name || '无' }}</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-label">选手总数</div>
          <div class="stat-value">{{ dashboard?.player_count ?? '-' }}</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-label">赛事总数</div>
          <div class="stat-value">{{ dashboard?.tournament_count ?? '-' }}</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-label">积分记录</div>
          <div class="stat-value">{{ dashboard?.points_record_count ?? '-' }}</div>
        </div>
      </el-col>
    </el-row>

    <div class="section">
      <h3>最近上传</h3>
      <el-table :data="dashboard?.recent_uploads || []" border size="small" v-loading="loading">
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="tournament_name" label="赛事" width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboard } from '@/api/dashboard'
import type { DashboardData } from '@tha/shared/types/dashboard'

const loading = ref(false)
const dashboard = ref<DashboardData | null>(null)

async function fetchData() {
  loading.value = true
  try {
    const res = await getDashboard()
    dashboard.value = res.data
  } finally { loading.value = false }
}

onMounted(fetchData)
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.stat-card {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}
.stat-label { font-size: 14px; color: #909399; margin-bottom: 8px; }
.stat-value { font-size: 24px; font-weight: 600; color: #303133; }
.section { margin-top: 8px; }
.section h3 { font-size: 16px; margin-bottom: 12px; }
</style>
