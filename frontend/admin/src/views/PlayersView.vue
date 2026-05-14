<template>
  <div class="page-container">
    <div class="page-header">
      <h2>选手管理</h2>
      <el-button type="primary" @click="openCreate">新建选手</el-button>
    </div>

    <div class="filter-bar">
      <el-input v-model="searchText" placeholder="搜索选手姓名" clearable style="width: 200px" @input="debouncedSearch" />
      <el-select v-model="filterDept" placeholder="院系筛选" clearable style="width: 160px" @change="fetchData">
        <el-option v-for="d in departments" :key="d" :label="d" :value="d" />
      </el-select>
    </div>

    <el-table :data="players" v-loading="loading" border style="margin-top: 16px">
      <el-table-column prop="full_name" label="姓名" width="120" />
      <el-table-column prop="gender" label="性别" width="80">
        <template #default="{ row }">{{ row.gender === 'male' ? '男' : row.gender === 'female' ? '女' : '-' }}</template>
      </el-table-column>
      <el-table-column prop="birth_date" label="出生日期" width="120" />
      <el-table-column prop="department" label="院系" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status === 'active' ? '活跃' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑选手' : '新建选手'" width="480px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="form.full_name" />
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="出生日期">
          <el-date-picker v-model="form.birth_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="院系">
          <el-input v-model="form.department" />
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
import { ElMessage, type FormInstance } from 'element-plus'
import { getPlayers, createPlayer, updatePlayer } from '@/api/players'
import { debounce } from '@tha/shared/utils/debounce'
import type { Player } from '@tha/shared/types/player'

const loading = ref(false)
const players = ref<Player[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const searchText = ref('')
const filterDept = ref('')
const departments = ref<string[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({ full_name: '', gender: '', birth_date: '', department: '' })
const rules = { full_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }] }

async function fetchData() {
  loading.value = true
  try {
    const res = await getPlayers({
      page: page.value,
      page_size: pageSize,
      search: searchText.value || undefined,
      department: filterDept.value || undefined,
    })
    players.value = res.data
    total.value = res.total
  } finally {
    loading.value = false
  }
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

function openCreate() {
  isEdit.value = false; editId.value = null
  Object.assign(form, { full_name: '', gender: '', birth_date: '', department: '' })
  dialogVisible.value = true
}

function openEdit(row: Player) {
  isEdit.value = true; editId.value = row.id
  Object.assign(form, { full_name: row.full_name, gender: row.gender || '', birth_date: row.birth_date || '', department: row.department || '' })
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  const data: any = { full_name: form.full_name }
  if (form.gender) data.gender = form.gender
  if (form.birth_date) data.birth_date = form.birth_date
  if (form.department) data.department = form.department
  try {
    if (isEdit.value && editId.value) {
      await updatePlayer(editId.value, data)
    } else {
      await createPlayer(data)
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

onMounted(() => { fetchData(); fetchDepartments() })
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
.filter-bar { display: flex; gap: 12px; }
</style>
