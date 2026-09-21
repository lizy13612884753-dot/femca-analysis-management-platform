import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { login as loginApi, logout as logoutApi, getUserInfo, refreshToken } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const refreshTokenValue = ref(localStorage.getItem('refreshToken') || '')
  const userInfo = ref(null)
  const isLoading = ref(false)
  const authInitialized = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!userInfo.value)
  const hasValidToken = computed(() => !!token.value)
  const userRole = computed(() => userInfo.value?.role?.name || '')
  const authReady = computed(() => authInitialized.value && !!token.value)

  // 登录
  const login = async (credentials) => {
    try {
      isLoading.value = true
      const response = await loginApi(credentials)
      console.log('登录响应:', response)
      
      const { tokens, user } = response
      console.log('tokens:', tokens)
      console.log('user:', user)
      
      const access = tokens?.access
      const refresh = tokens?.refresh
      
      console.log('access:', access)
      console.log('refresh:', refresh)
      
      token.value = access
      refreshTokenValue.value = refresh
      userInfo.value = user
      authInitialized.value = true
      
      console.log('token设置后:', token.value)
      console.log('userInfo设置后:', userInfo.value)
      console.log('isAuthenticated:', isAuthenticated.value)
      
      // 存储到本地
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)
      
      ElMessage.success('登录成功')
      return { success: true }
    } catch (error) {
      console.error('登录错误:', error)
      ElMessage.error(error.response?.data?.detail || '登录失败')
      return { success: false, error: error.response?.data?.detail || '登录失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      if (token.value) {
        await logoutApi()
      }
    } catch (error) {
      console.error('登出API调用失败:', error)
    } finally {
      // 清除本地状态
      token.value = ''
      refreshTokenValue.value = ''
      userInfo.value = null
      authInitialized.value = false
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
    }
  }

  // 检查认证状态
  const checkAuthStatus = async () => {
    if (!token.value) {
      authInitialized.value = true
      return false
    }
    
    try {
      const response = await getUserInfo()
      userInfo.value = response
      authInitialized.value = true
      return true
    } catch (error) {
      // Token可能过期，尝试刷新
      if (error.response?.status === 401 && refreshTokenValue.value) {
        try {
          const response = await refreshToken({ refresh: refreshTokenValue.value })
          token.value = response.access
          localStorage.setItem('token', token.value)
          
          const userResponse = await getUserInfo()
          userInfo.value = userResponse
          authInitialized.value = true
          return true
        } catch (refreshError) {
          // 刷新失败，清除状态
          logout()
          authInitialized.value = true
          return false
        }
      }
      logout()
      authInitialized.value = true
      return false
    }
  }

  // 更新用户信息
  const updateUserInfo = (info) => {
    userInfo.value = { ...userInfo.value, ...info }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) {
      return null
    }
    
    try {
      const response = await getUserInfo()
      userInfo.value = response
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return null
    }
  }

  return {
    // 状态
    token,
    refreshTokenValue,
    userInfo,
    isLoading,
    authInitialized,
    // 计算属性
    isAuthenticated,
    hasValidToken,
    userRole,
    // 方法
    login,
    logout,
    checkAuthStatus,
    updateUserInfo,
    fetchUserInfo
  }
})