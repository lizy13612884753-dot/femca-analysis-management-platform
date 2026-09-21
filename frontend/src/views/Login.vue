<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>FMECA设施设备分析管理平台</h1>
      <p>请登录您的账户</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        size="large"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="isLoading"
            @click="handleLogin"
            style="width: 100%"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>© 2026 FMECA平台. 保留所有权利.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref()

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

// 加载状态
const isLoading = ref(false)

// 登录处理
const handleLogin = async () => {
  try {
    // 表单验证
    await loginFormRef.value.validate()
    
    isLoading.value = true
    console.log('🚀 开始登录...', loginForm.username)
    
    // 执行登录
    const result = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    console.log('📋 登录结果:', result)
    
    if (result.success) {
      console.log('✅ 登录成功，跳转到仪表盘')
      console.log('📊 当前状态: token=', !!userStore.token, 'userInfo=', !!userStore.userInfo, 'authInitialized=', userStore.authInitialized)
      
      // 强制更新 authInitialized
      userStore.authInitialized = true
      
      // 使用 replace 而不是 push，避免浏览器历史问题
      router.replace('/dashboard')
    }
  } catch (error) {
    console.error('❌ 登录失败:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.login-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-footer {
  text-align: center;
}

.login-footer p {
  margin: 0;
  color: #999;
  font-size: 12px;
}

:deep(.el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-button--large) {
  border-radius: 6px;
  font-size: 16px;
}
</style>