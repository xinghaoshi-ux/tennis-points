<template>
  <div class="page-container">
    <div class="page-header">
      <h2>赛季管理</h2>
      <el-button type="primary" @click="openCreate">新建赛季</el-button>
    </div>

    <el-table :data="seasons" v-loading="loading" border>
      <el-table-column prop="name" label="赛季名称" />
      <el-table-column prop="start_date" label="开始日期" width="120" />
      <el-table-column prop="end_date" label="结束日期" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)" :disabled="row.status !== 'draft'">编辑</el-button>
          <el-button size="small" type="success" @click="handleActivate(row)" v-if="row.status === 'draft'">激活</el-button>
          <el-button size="small" type="warning" @click="handleClose(row)" v-if="row.status === 'active'">关闭</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑赛季' : '新建赛季'" width="480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
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
import { getSeasons, createSeason, updateSeason, activateSeason, closeSeason, deleteSeason } from '@/api/seasons'
import type { Season } from '@tha/shared/types/season'

const loading = ref(false)
const seasons = ref<Season[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({ name: '', start_date: '', end_date: '' })
const rules = {
  name: [{ required: true, message: '请输入赛季名称', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
}

function statusType(status: string) {
  return status === 'active' ? 'success' : status === 'closed' ? 'info' : 'warning'
}
function statusLabel(status: string) {
  return { draft: '草稿', active: '活跃', closed: '已关闭' }[status] || status
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getSeasons({ page: 1, page_size: 50 })
    seasons.value = res.data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  isEdit.value = false
  editId.value = null
  Object.assign(form, { name: '', start_date: '', end_date: '' })
  dialogVisible.value = true
}

function openEdit(row: Season) {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, start_date: row.start_date, end_date: row.end_date })
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isEdit.value && editId.value) {
      await updateSeason(editId.value, form)
    } else {
      await createSeason(form)
    }
    ElMessage.success('操作成功')
    dialogVisible.value = false
    await fetchData()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

async function handleActivate(row: Season) {
  await ElMessageBox.confirm('激活此赛季将关闭当前活跃赛季，确认？', '确认激活')
  try {
    await activateSeason(row.id)
    ElMessage.success('赛季已激活')
    await fetchData()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '激活失败')
  }
}

async function handleClose(row: Season) {
  await ElMessageBox.confirm('确认关闭此赛季？', '确认关闭')
  try {
    await closeSeason(row.id)
    ElMessage.success('赛季已关闭')
    await fetchData()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '关闭失败')
  }
}

async function handleDelete(row: Season) {
  await ElMessageBox.confirm('删除赛季将同时删除该赛季下所有赛事、积分和规则数据，确认删除？', '确认删除', { type: 'warning' })
  try {
    await deleteSeason(row.id)
    ElMessage.success('赛季已删除')
    await fetchData()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '删除失败')
  }
}

onMounted(fetchData)
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; font-size: 18px; }
</style>
