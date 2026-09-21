<template>
  <div class="layout-container">
    <!-- 顶部导航栏 -->
    <div class="layout-header">
      <div class="header-left">
        <div class="logo">
          <h2>FMECA平台</h2>
        </div>
      </div>
      
      <div class="header-center">
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          router
          class="top-menu"
        >
          <el-menu-item index="/dashboard">
            <el-icon><Monitor /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          
          <el-sub-menu index="/equipment">
            <template #title>
              <el-icon><Tools /></el-icon>
              <span>设备管理</span>
            </template>
            <el-menu-item index="/equipment/types">设备类型</el-menu-item>
            <el-menu-item index="/equipment/instances">设备实例</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/failure">
            <el-icon><Warning /></el-icon>
            <span>故障模式</span>
          </el-menu-item>
          
          <el-menu-item index="/severity">
            <el-icon><TrendCharts /></el-icon>
            <span>严酷度</span>
          </el-menu-item>
          

          
          <el-sub-menu index="/analysis">
            <template #title>
              <el-icon><DataAnalysis /></el-icon>
              <span>危害度分析</span>
            </template>
            <el-menu-item index="/analysis/failure-mode">故障模式分析</el-menu-item>
            <el-menu-item index="/analysis/product">产品分析</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/statistics">
            <el-icon><DataBoard /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
        </el-menu>
      </div>
      
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <div class="user-info">
            <el-avatar :size="32" :src="userInfo?.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span class="username">{{ userInfo?.username }}</span>
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <!-- 主内容区域 -->
    <div class="layout-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Monitor, Tools, Connection, Warning, TrendCharts,
  DataAnalysis, DataBoard, User, ArrowDown,
  SwitchButton
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 计算属性
const activeMenu = computed(() => {
  if (route.path.includes('/equipment/types')) return '/equipment/types'
  if (route.path.includes('/equipment/instances')) return '/equipment/instances'
  if (route.path.includes('/analysis/failure-mode')) return '/analysis/failure-mode'
  if (route.path.includes('/analysis/product')) return '/analysis/product'
  return route.path
})

const userInfo = computed(() => userStore.userInfo)

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm(
          '确定要退出登录吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        await userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 用户取消
      }
      break
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-header {
  height: 64px;
  background: var(--background-light);
  border-bottom: 1px solid var(--border-base);
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-left {
  width: 200px;
  flex-shrink: 0;
}

.logo h2 {
  margin: 0;
  color: var(--primary-color);
  font-size: 20px;
  font-weight: 600;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.top-menu {
  border-bottom: none;
  background: transparent;
}

.header-right {
  width: 200px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: var(--background-base);
}

.username {
  margin: 0 8px;
  font-size: 14px;
  color: var(--text-primary);
}

.layout-content {
  flex: 1;
  overflow: auto;
  background: var(--background-base);
  padding: 24px;
}

:deep(.el-menu--horizontal > .el-menu-item) {
  height: 64px;
  line-height: 64px;
  padding: 0 16px;
}

:deep(.el-menu--horizontal > .el-sub-menu .el-sub-menu__title) {
  height: 64px;
  line-height: 64px;
  padding: 0 16px;
}
</style>