<template>
  <div class="page-container">
    <div class="page-header">
      <h2>积分规则</h2>
      <el-button type="primary" @click="openCreate">新建规则</el-button>
    </div>

    <el-tabs v-model="activeTab" @tab-change="fetchData">
      <el-tab-pane label="个人赛事" name="individual_event" />
      <el-tab-pane label="团体赛事" name="team_event" />
      <el-tab-pane label="差旅加分" name="travel_bonus" />
      <el-tab-pane label="代表队" name="representative_team" />
      <el-tab-pane label="组织者加分" name="organizer_bonus" />
      <el-tab-pane label="捐赠加分" name="donation_bonus" />
    </el-tabs>

    <el-table :data="rules" v-loading="loading" border>
      <el-table-column prop="event_level" label="赛事级别" width="120" />
      <el-table-column prop="group_name" label="组别" width="80" />
      <el-table-column prop="result_type" label="成绩类型" width="120">
        <template #default="{ row }">{{ resultLabel(row.result_type) }}</template>
      </el-table-column>
      <el-table-column prop="points" label="积分" width="80" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑规则' : '新建规则'" width="520px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="规则类型" prop="rule_type">
          <el-select v-model="form.rule_type" style="width: 100%">
            <el-option label="个人赛事" value="individual_event" />
            <el-option label="团体赛事" value="team_event" />
            <el-option label="差旅加分" value="travel_bonus" />
            <el-option label="代表队" value="representative_team" />
            <el-option label="组织者加分" value="organizer_bonus" />
            <el-option label="捐赠加分" value="donation_bonus" />
          </el-select>
        </el-form-item>
        <el-form-item label="赛事级别" v-if="form.rule_type === 'individual_event' || form.rule_type === 'team_event'">
          <el-select v-model="form.event_level" clearable style="width: 100%">
            <el-option v-for="l in levels" :key="l" :label="l" :value="l" />
          </el-select>
        </el-form-item>
        <el-form-item label="组别">
          <el-input v-model="form.group_name" placeholder="如：甲组" />
        </el-form-item>
        <el-form-item label="成绩类型" v-if="form.rule_type === 'individual_event' || form.rule_type === 'team_event'">
          <el-select v-model="form.result_type" clearable style="width: 100%">
            <el-option label="冠军" value="champion" />
            <el-option label="亚军" value="runner_up" />
            <el-option label="四强" value="semifinal" />
            <el-option label="八强" value="quarterfinal" />
            <el-option label="参赛" value="participant" />
          </el-select>
        </el-form-item>
        <el-form-item label="积分" prop="points">
          <el-input-number v-model="form.points" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
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
import { getPointsRules, createPointsRule, updatePointsRule, deletePointsRule } from '@/api/pointsRules'
import type { PointsRule } from '@tha/shared/types/pointsRule'

const levels = ['THA1000', 'THA800', 'THA500', 'THA200', 'THA_S', 'THA_A', 'THA_B', 'representative', 'bonus']
const loading = ref(false)
const rules = ref<PointsRule[]>([])
const activeTab = ref('individual_event')
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({ rule_type: 'individual_event', event_level: '', group_name: '', result_type: '', points: 0, description: '' })
const formRules = {
  rule_type: [{ required: true, message: '请选择规则类型', trigger: 'change' }],
  points: [{ required: true, message: '请输入积分', trigger: 'blur' }],
}

function resultLabel(r: string) {
  return { champion: '冠军', runner_up: '亚军', semifinal: '四强', quarterfinal: '八强', participant: '参赛' }[r] || r || '-'
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getPointsRules({ rule_type: activeTab.value })
    rules.value = res.data
  } finally { loading.value = false }
}

function openCreate() {
  isEdit.value = false; editId.value = null
  Object.assign(form, { rule_type: activeTab.value, event_level: '', group_name: '', result_type: '', points: 0, description: '' })
  dialogVisible.value = true
}

function openEdit(row: PointsRule) {
  isEdit.value = true; editId.value = row.id
  Object.assign(form, { rule_type: row.rule_type, event_level: row.event_level || '', group_name: row.group_name || '', result_type: row.result_type || '', points: row.points, description: row.description || '' })
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  const data: any = { rule_type: form.rule_type, points: form.points }
  if (form.event_level) data.event_level = form.event_level
  if (form.group_name) data.group_name = form.group_name
  if (form.result_type) data.result_type = form.result_type
  if (form.description) data.description = form.description
  try {
    if (isEdit.value && editId.value) { await updatePointsRule(editId.value, data) }
    else { await createPointsRule(data) }
    ElMessage.success('操作成功')
    dialogVisible.value = false
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '操作失败') }
  finally { submitting.value = false }
}

async function handleDelete(row: PointsRule) {
  await ElMessageBox.confirm('确认删除此规则？', '确认删除')
  try {
    await deletePointsRule(row.id)
    ElMessage.success('已删除')
    await fetchData()
  } catch (e: any) { ElMessage.error(e?.response?.data?.detail || '删除失败') }
}

onMounted(fetchData)
</script>

<style scoped>
.page-container { background: #fff; padding: 24px; border-radius: 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
</style>
