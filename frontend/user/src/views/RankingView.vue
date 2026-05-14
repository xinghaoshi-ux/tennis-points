<template>
  <div class="ranking-page">
    <header class="ranking-header">
      <h1>THA 年度积分排行榜</h1>
      <p v-if="seasonName" class="season-info">{{ seasonName }}</p>
    </header>

    <div class="filter-section">
      <input
        v-model="searchText"
        class="search-input"
        placeholder="搜索选手姓名"
        @input="debouncedSearch"
      />
      <select v-model="filterDept" class="dept-select" @change="handleFilter">
        <option value="">全部院系</option>
        <option v-for="d in departments" :key="d" :value="d">{{ d }}</option>
      </select>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <div v-else-if="rankings.length === 0" class="empty-state">
      <p>暂无排行数据</p>
    </div>

    <template v-else>
      <!-- Desktop table -->
      <table class="ranking-table desktop-only">
        <thead>
          <tr>
            <th>排名</th>
            <th>姓名</th>
            <th>院系</th>
            <th>总积分</th>
            <th>参赛次数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in rankings" :key="item.player_id" @click="showDetail(item.player_id)">
            <td class="rank-cell">{{ item.ranking }}</td>
            <td class="name-cell">{{ item.full_name }}</td>
            <td>{{ item.department || '-' }}</td>
            <td class="points-cell">{{ item.total_points }}</td>
            <td>{{ item.tournament_count }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Mobile cards -->
      <div class="card-list mobile-only">
        <div v-for="item in rankings" :key="item.player_id" class="ranking-card" @click="showDetail(item.player_id)">
          <div class="card-rank">#{{ item.ranking }}</div>
          <div class="card-info">
            <div class="card-name">{{ item.full_name }}</div>
            <div class="card-dept">{{ item.department || '-' }}</div>
          </div>
          <div class="card-points">{{ item.total_points }} 分</div>
        </div>
      </div>

      <div v-if="total > pageSize" class="pagination">
        <button :disabled="page <= 1" @click="page--; fetchData()">上一页</button>
        <span>{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
        <button :disabled="page >= Math.ceil(total / pageSize)" @click="page++; fetchData()">下一页</button>
      </div>
    </template>

    <!-- Player detail modal -->
    <div v-if="detailVisible" class="modal-overlay" @click.self="detailVisible = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ playerDetail?.player.full_name }}</h2>
          <button class="modal-close" @click="detailVisible = false">&times;</button>
        </div>
        <div v-if="playerDetail" class="modal-body">
          <div class="summary-grid">
            <div class="summary-item">
              <span class="summary-label">个人赛事</span>
              <span class="summary-value">{{ playerDetail.summary.individual_event }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">团体分摊</span>
              <span class="summary-value">{{ playerDetail.summary.team_share }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">差旅加分</span>
              <span class="summary-value">{{ playerDetail.summary.travel_bonus }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">代表队</span>
              <span class="summary-value">{{ playerDetail.summary.representative_team }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">组织者加分</span>
              <span class="summary-value">{{ playerDetail.summary.organizer_bonus }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">捐赠加分</span>
              <span class="summary-value">{{ playerDetail.summary.donation_bonus }}</span>
            </div>
          </div>
          <h3 style="margin: 16px 0 8px">积分明细</h3>
          <div class="detail-list">
            <div v-for="d in playerDetail.details" :key="d.id" class="detail-item">
              <span class="detail-name">{{ d.tournament_name }}</span>
              <span class="detail-points">+{{ d.points }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getRankings, getPlayerPoints, getCurrentSeason, getDepartments } from '@/api/public'
import { debounce } from '@tha/shared/utils/debounce'
import type { RankingItem, PlayerPointsDetail } from '@tha/shared/types/ranking'

const loading = ref(false)
const rankings = ref<RankingItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const searchText = ref('')
const filterDept = ref('')
const departments = ref<string[]>([])
const seasonName = ref('')
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

const debouncedSearch = debounce(() => { page.value = 1; fetchData() })
function handleFilter() { page.value = 1; fetchData() }

async function showDetail(playerId: number) {
  try {
    const res = await getPlayerPoints(playerId)
    playerDetail.value = res.data
    detailVisible.value = true
  } catch { /* ignore */ }
}

onMounted(async () => {
  try {
    const seasonRes = await getCurrentSeason()
    seasonName.value = seasonRes.data?.name || ''
  } catch { /* ignore */ }
  try {
    const deptRes = await getDepartments()
    departments.value = deptRes.data || []
  } catch { /* ignore */ }
  fetchData()
})
</script>
