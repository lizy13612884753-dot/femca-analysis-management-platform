import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由懒加载
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表板', icon: 'Monitor' }
      },
      {
        path: '/equipment',
        name: 'Equipment',
        meta: { title: '设备管理', icon: 'Tools' },
        children: [
          {
            path: 'types',
            name: 'EquipmentTypes',
            component: () => import('@/views/equipment/EquipmentTypes.vue'),
            meta: { title: '设备类型管理' }
          },
          {
            path: 'instances',
            name: 'EquipmentInstances',
            component: () => import('@/views/equipment/EquipmentInstances.vue'),
            meta: { title: '设备实例管理' }
          }
        ]
      },
      {
        path: '/failure',
        name: 'Failure',
        component: () => import('@/views/failure/FailureModes.vue'),
        meta: { title: '故障模式管理', icon: 'Warning' }
      },
      {
        path: '/severity',
        name: 'Severity',
        component: () => import('@/views/severity/SeverityLevels.vue'),
        meta: { title: '严酷度管理', icon: 'TrendCharts' }
      },
      {
        path: '/compensation',
        name: 'Compensation',
        redirect: '/compensation/effectiveness',
        meta: { title: '补偿措施', icon: 'Shield' },
        children: [
          {
            path: 'effectiveness',
            name: 'EffectivenessEvaluation',
            component: () => import('@/views/compensation/EffectivenessEvaluation.vue'),
            meta: { title: '有效性评估' }
          }
        ]
      },
      {
        path: '/analysis',
        name: 'Analysis',
        meta: { title: '危害度分析', icon: 'DataAnalysis' },
        children: [
          {
            path: 'failure-mode',
            name: 'FailureModeAnalysis',
            component: () => import('@/views/analysis/FailureModeAnalysis.vue'),
            meta: { title: '故障模式危害度分析' }
          },
          {
            path: 'product',
            name: 'ProductAnalysis',
            component: () => import('@/views/analysis/ProductAnalysis.vue'),
            meta: { title: '产品危害度分析' }
          }
        ]
      },
      {
        path: '/statistics',
        name: 'Statistics',
        component: () => import('@/views/statistics/DataStatistics.vue'),
        meta: { title: '数据统计', icon: 'DataBoard' }
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '个人资料', icon: 'User' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Error404.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const publicPaths = ['/login', '/register', '/reset-password']

router.beforeEach(async (to, from) => {
  const userStore = useUserStore()
  
  const hasToken = !!userStore.token
  const hasUserInfo = !!userStore.userInfo
  const isAuthReady = hasToken && hasUserInfo && userStore.authInitialized
  
  console.log('🔐 路由守卫执行:', to.path, 'authInitialized:', userStore.authInitialized, 'hasToken:', hasToken, 'hasUserInfo:', hasUserInfo, 'isAuthReady:', isAuthReady)
  
  // 等待认证初始化完成
  if (!userStore.authInitialized) {
    console.log('⏳ 等待认证初始化...')
    await userStore.checkAuthStatus()
    console.log('✅ 认证初始化完成')
  }
  
  const isPublicPath = publicPaths.includes(to.path)
  const requiresAuth = to.meta.requiresAuth !== false
  
  // 如果已登录且访问登录页，重定向到首页
  if (to.path === '/login' && isAuthReady) {
    console.log('✅ 已登录，重定向到仪表盘')
    return '/dashboard'
  }
  
  // 检查是否需要登录 - 使用更可靠的状态检查
  if (requiresAuth && !isPublicPath) {
    const isAuthenticated = !!userStore.token && !!userStore.userInfo
    if (!isAuthenticated) {
      console.log('❌ 未登录，重定向到登录页')
      return '/login'
    }
  }
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - FMECA平台`
  }
  
  console.log('✅ 路由放行:', to.path)
  return true
})

export default router