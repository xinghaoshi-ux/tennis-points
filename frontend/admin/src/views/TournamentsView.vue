<template>
  <div class="page-container">
    <div class="page-header">
      <h2>赛事管理</h2>
      <el-button type="primary" @click="openCreate">新建赛事</el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 140px" @change="fetchData">
        <el-option label="草稿" value="draft" />
        <el-option label="已完成" value="completed" />
        <el-option label="已发布" value="published" />
      </el-select>
    </div>

    <el-table :data="tournaments" v-loading="loading" border style="margin-top: 16px">
      <el-table-column prop="name" label="赛事名称" />
      <el-table-column prop="level" label="级别" width="100" />
      <el-table-column prop="event_category" label="类别" width="140">
        <template #default="{ row }">{{ categoryLabel(row.event_category) }}</template>
      </el-table-column>
      <el-table-column prop="group_name" label="组别" width="80" />
      <el-table-column prop="location" label="地点" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="tStatusType(row.status)">{{ tStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="320">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)" :disabled="row.status !== 'draft'">编辑</el-button>
          <el-button size="small" type="primary" @click="handleGenerate(row)" v-if="row.status === 'completed' || row.status === 'published'">生成积分</el-button>
          <el-button size="small" type="warning" @click="handleRevoke(row)" v-if="row.status === 'published'">撤回发布</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑赛事' : '新建赛事'" width="520px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="类别" prop="event_category">
          <el-select v-model="form.event_category" style="width: 100%">
            <el-option label="个人双打" value="individual_doubles" />
            <el-option label="团体" value="team" />
            <el-option label="代表队" value="representative" />
            <el-option label="加分" value="bonus" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别" prop="level">
          <el-select v-model="form.level" style="width: 100%">
            <el-option v-for="l in levels" :key="l" :label="l" :value="l" />
          </el-select>
        </el-form-item>
        <el-form-item label="组别">
          <el-input v-model="form.group_name" placeholder="如：甲组、乙组" />
        </el-form-item>
        <el-form-item label="地点">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="form.tournament_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { getTournaments, createTournament, updateTournament, generatePoints, revokePublish, deleteTournament } from '@/api/tournaments'
import type { Tournament } from '@tha/shared/types/tournament'

const levels = ['THA1000', 'THA800', 'THA500', 'THA200', 'THA_S', 'THA_A', 'THA_B', 'representative', 'bonus']
const loading = ref(false)
const tournaments = ref<Tournament[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const filterStatus = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({ name: '', event_category: '', level: '', group_name: '', location: '', tournament_date: '' })
const rules = {
  name: [{ required: true, message: '请输入赛事名称', trigger: 'blur' }],
  event_category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  level: [{ required: true, message: '请选择级别', trigger: 'change' }],
}

function categoryLabel(c: string) {
  return { individual_doubles: '个人双打', team: '团体', representative: '代表队', bonus: '加分' }[c] || c
}
function tStatusType(s: string) { return { draft: 'warning', completed: 'success', published: '' }[s] || 'info' }
function tStatusLabel(s: string) { return { draft: '草稿', completed: '已完成', published: '已发布' }[s] || s }

async function fetchData() {
  loading.value = true
  try {
    const res = await getTournaments({ page: page.value, page_size: pageSize, status: filterStatus.value || undefined })
    tournaments.value = res.data
    total.value = res.total
  } finally { loading.value = false }
}

function handlePageChange(p: number) { page.value = p; fetchData() }

function openCreate() {
  isEdit.value = false; editId.value = null
  Object.assign(form, { name: '', event_category: '', level: '', group_name: '', location: '', tournament_date: '' })
  dialogVisible.value = true
}

function openEdit(row: Tournament) {
  isEdit.value = true; editId.value = row.id
  Object.assign(form, { name: row.name, event_category: row.event_category, level: row.level, group_name: row.group_name || '', location: row.location || '', tournament_date: row.tournament_date || '' })
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  const data: any = { name: form.name, event_category: form.event_category, level: form.level }
  if (form.group_name) data.group_name = form.group_name
  if (form.location) data.location = form.location
  if (form.tournament_date) data.tournament_date = form.tournament_date
  try {
    if (isEdit.value && editId.value) { await updateTournament(editId.value, data) }
    else { await createTournament(data) }
    ElMessage.success('操作成功')
    dialogVisible.value = false
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '操作失败') }
  finally { submitting.value = false }
}

async function handleGenerate(row: Tournament) {
  await ElMessageBox.confirm('确认为此赛事生成积分？', '确认')
  try {
    await generatePoints(row.id)
    ElMessage.success('积分生成已触发')
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '操作失败') }
}

async function handleRevoke(row: Tournament) {
  await ElMessageBox.confirm('撤回发布将删除已生成的积分记录，确认？', '确认撤回')
  try {
    await revokePublish(row.id)
    ElMessage.success('已撤回发布')
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '操作失败') }
}

async function handleDelete(row: Tournament) {
  await ElMessageBox.confirm(`确认删除赛事"${row.name}"？相关积分和导入记录也会被删除。`, '确认删除', { type: 'warning' })
  try {
    await deleteTournament(row.id)
    ElMessage.success('赛事已删除')
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '删除失败') }
}

onMounted(fetchData)
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
.filter-bar { display: flex; gap: 12px; }
</style>
