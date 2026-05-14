<template>
  <div class="page-container">
    <div class="page-header">
      <h2>排行榜管理</h2>
      <div>
        <el-tooltip content="即将上线" placement="top">
          <el-button disabled>导出排行榜</el-button>
        </el-tooltip>
        <el-button type="primary" :loading="refreshing" @click="handleRefresh">刷新排行榜</el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-input v-model="searchText" placeholder="搜索选手" clearable style="width: 200px" @input="debouncedSearch" />
      <el-select v-model="filterDept" placeholder="院系筛选" clearable style="width: 160px" @change="fetchData">
        <el-option v-for="d in departments" :key="d" :label="d" :value="d" />
      </el-select>
    </div>

    <el-table :data="rankings" v-loading="loading" border style="margin-top: 16px">
      <el-table-column prop="ranking" label="排名" width="70" />
      <el-table-column prop="full_name" label="姓名" width="120">
        <template #default="{ row }">
          <el-link type="primary" @click="showPlayerDetail(row.player_id)">{{ row.full_name }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="department" label="院系" />
      <el-table-column prop="total_points" label="总积分" width="100" />
      <el-table-column prop="tournament_count" label="参赛次数" width="100" />
    </el-table>

    <el-pagination
      v-if="total > pageSize"
      :current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      style="margin-top: 16px; justify-content: flex-end"
      @current-change="handlePageChange"
    />

    <el-dialog v-model="detailVisible" title="选手积分详情" width="600px">
      <div v-if="playerDetail">
        <h3>{{ playerDetail.player.full_name }} - {{ playerDetail.player.department }}</h3>
        <el-descriptions :column="3" border size="small" style="margin-bottom: 16px">
          <el-descriptions-item label="个人赛事">{{ playerDetail.summary.individual_event }}</el-descriptions-item>
          <el-descriptions-item label="团体分摊">{{ playerDetail.summary.team_share }}</el-descriptions-item>
          <el-descriptions-item label="差旅加分">{{ playerDetail.summary.travel_bonus }}</el-descriptions-item>
          <el-descriptions-item label="代表队">{{ playerDetail.summary.representative_team }}</el-descriptions-item>
          <el-descriptions-item label="组织者加分">{{ playerDetail.summary.organizer_bonus }}</el-descriptions-item>
          <el-descriptions-item label="捐赠加分">{{ playerDetail.summary.donation_bonus }}</el-descriptions-item>
        </el-descriptions>
        <el-table :data="playerDetail.details" border size="small" max-height="300">
          <el-table-column prop="tournament_name" label="赛事" />
          <el-table-column prop="source_type" label="类型" width="120" />
          <el-table-column prop="points" label="积分" width="80" />
          <el-table-column prop="created_at" label="时间" width="120" />
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRankings, refreshRankings, getPlayerPoints } from '@/api/rankings'
import { debounce } from '@tha/shared/utils/debounce'
import type { RankingItem, PlayerPointsDetail } from '@tha/shared/types/ranking'

const loading = ref(false)
const refreshing = ref(false)
const rankings = ref<RankingItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const searchText = ref('')
const filterDept = ref('')
const departments = ref<string[]>([])
const detailVisible = ref(false)
const playerDetail = ref<PlayerPointsDetail | null>(null)

async function fetchData() {
  loading.value = true
  try {
    const res = await getRankings({ page: page.value, page_size: pageSize, search: searchText.value || undefined, department: filterDept.value || undefined })
    rankings.value = res.data
    total.value = res.total
  } finally { loading.value = false }
}

async function fetchDepartments() {
  try {
    const { http } = await import('@/utils/http')
    const res = await http.get<any, any>('/public/departments')
    departments.value = res.data || []
  } catch { /* ignore */ }
}

const debouncedSearch = debounce(() => { page.value = 1; fetchData() })
function handlePageChange(p: number) { page.value = p; fetchData() }

async function handleRefresh() {
  refreshing.value = true
  try {
    await refreshRankings()
    ElMessage.success('排行榜已刷新')
    await fetchData()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '刷新失败')
  } finally { refreshing.value = false }
}

async function showPlayerDetail(playerId: number) {
  try {
    const res = await getPlayerPoints(playerId)
    playerDetail.value = res.data
    detailVisible.value = true
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '获取详情失败')
  }
}

onMounted(() => { fetchData(); fetchDepartments() })
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
.filter-bar { display: flex; gap: 12px; }
</style>
