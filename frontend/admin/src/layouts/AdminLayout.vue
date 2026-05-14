<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>THA 积分系统</h2>
      </div>
      <el-menu :default-active="route.path" router>
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <div class="main-area">
      <header class="topbar">
        <div class="topbar-left">
          <span v-if="appStore.currentSeason" class="season-badge">
            当前赛季：{{ appStore.currentSeason.name }}
          </span>
        </div>
        <div class="topbar-right">
          <span class="user-name">{{ authStore.user?.display_name }}</span>
          <el-button text @click="authStore.logout()">退出</el-button>
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Odometer, Calendar, User, Trophy, Setting, Upload, Rank } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const authStore = useAuthStore()
const appStore = useAppStore()

const menuItems = [
  { path: '/dashboard', label: '仪表盘', icon: Odometer },
  { path: '/seasons', label: '赛季管理', icon: Calendar },
  { path: '/players', label: '选手管理', icon: User },
  { path: '/tournaments', label: '赛事管理', icon: Trophy },
  { path: '/points-rules', label: '积分规则', icon: Setting },
  { path: '/uploads', label: 'Excel 导入', icon: Upload },
  { path: '/rankings', label: '排行榜管理', icon: Rank },
]

onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchMe()
  }
  await appStore.fetchCurrentSeason()
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 220px;
  background: #304156;
  color: #fff;
  flex-shrink: 0;
}
.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.sidebar-header h2 {
  font-size: 16px;
  color: #fff;
  margin: 0;
}
.sidebar :deep(.el-menu) {
  border-right: none;
  background: #304156;
}
.sidebar :deep(.el-menu-item) {
  color: #bfcbd9;
}
.sidebar :deep(.el-menu-item:hover),
.sidebar :deep(.el-menu-item.is-active) {
  background: #263445;
  color: #409eff;
}
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.topbar {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-name {
  color: #606266;
}
.season-badge {
  font-size: 14px;
  color: #409eff;
}
.content {
  flex: 1;
  padding: 24px;
  background: #f5f7fa;
  overflow-y: auto;
}
</style>
