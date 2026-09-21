import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const service = axios.create({
  baseURL: '',
  timeout: 10000,
  transformResponse: [
    (data) => {
      try {
        return JSON.parse(data)
      } catch (e) {
        return data
      }
    }
  ],
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  transitional: {
    silentJSONParsing: true,
    forcedJSONParsing: true,
    clarifyTimeoutError: false
  }
})

service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // 添加缓存控制头，确保每次请求都获取最新数据
    config.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    config.headers['Pragma'] = 'no-cache'
    config.headers['Expires'] = '0'
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response) => {
    console.log('API响应成功:', {
      url: response.config.url,
      status: response.status,
      dataType: typeof response.data,
      isArray: Array.isArray(response.data),
      data: response.data
    })
    return response.data
  },
  (error) => {
    console.error('请求错误:', error)
    console.error('错误详情:', {
      message: error.message,
      code: error.code,
      config: error.config?.url,
      response: error.response?.data,
      status: error.response?.status
    })
    
    // 处理401未授权错误
    if (error.response?.status === 401) {
      // 清除本地存储的token
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      // 重定向到登录页
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    }
    
    return Promise.reject(error)
  }
)

export default service