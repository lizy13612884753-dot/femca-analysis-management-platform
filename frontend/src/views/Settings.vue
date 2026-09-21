<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="偏好设置" name="preferences">
          <el-form :model="preferencesForm" label-width="120px" class="settings-form">
            <el-form-item label="主题">
              <el-radio-group v-model="preferencesForm.theme">
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
                <el-radio label="auto">跟随系统</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="语言">
              <el-select v-model="preferencesForm.language" placeholder="请选择语言">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en-US" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="每页显示">
              <el-select v-model="preferencesForm.pageSize" placeholder="请选择">
                <el-option label="10条/页" :value="10" />
                <el-option label="20条/页" :value="20" />
                <el-option label="50条/页" :value="50" />
                <el-option label="100条/页" :value="100" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="自动保存">
              <el-switch v-model="preferencesForm.autoSave" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="savePreferences">保存偏好设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="通知设置" name="notifications">
          <el-form :model="notificationsForm" label-width="120px" class="settings-form">
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationsForm.emailEnabled" />
            </el-form-item>
            
            <el-form-item label="系统通知">
              <el-switch v-model="notificationsForm.systemEnabled" />
            </el-form-item>
            
            <el-form-item label="故障提醒">
              <el-switch v-model="notificationsForm.failureAlert" />
            </el-form-item>
            
            <el-form-item label="分析完成提醒">
              <el-switch v-model="notificationsForm.analysisComplete" />
            </el-form-item>
            
            <el-form-item label="报告生成提醒">
              <el-switch v-model="notificationsForm.reportReady" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveNotifications">保存通知设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="安全设置" name="security">
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px" class="settings-form">
            <el-form-item label="当前密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入当前密码" />
            </el-form-item>
            
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码" />
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
              <el-button @click="resetPasswordForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="系统信息" name="system">
          <div class="system-info">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="系统名称">FMECA设施设备分析管理平台</el-descriptions-item>
              <el-descriptions-item label="系统版本">v1.0.0</el-descriptions-item>
              <el-descriptions-item label="当前用户">{{ userInfo?.username }}</el-descriptions-item>
              <el-descriptions-item label="用户角色">{{ userInfo?.role }}</el-descriptions-item>
              <el-descriptions-item label="用户状态">{{ userInfo?.status }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{ userInfo?.email }}</el-descriptions-item>
              <el-descriptions-item label="部门">{{ userInfo?.department || '未设置' }}</el-descriptions-item>
              <el-descriptions-item label="最后登录时间">{{ userInfo?.last_login_time || '首次登录' }}</el-descriptions-item>
              <el-descriptions-item label="最后登录IP">{{ userInfo?.last_login_ip || '未知' }}</el-descriptions-item>
              <el-descriptions-item label="注册时间">{{ userInfo?.date_joined }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import * as authApi from '@/api/auth'
import * as settingsApi from '@/api/settings'

const userStore = useUserStore()
const activeTab = ref('preferences')
const passwordFormRef = ref(null)
const loading = ref(false)

const userInfo = computed(() => userStore.userInfo)

const preferencesForm = reactive({
  theme: 'light',
  language: 'zh-CN',
  pageSize: 20,
  autoSave: true
})

const notificationsForm = reactive({
  emailEnabled: true,
  systemEnabled: true,
  failureAlert: true,
  analysisComplete: true,
  reportReady: true
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const loadSettings = async () => {
  try {
    loading.value = true
    const response = await settingsApi.getUserSettings()
    const settings = response.data || response
    
    preferencesForm.theme = settings.theme || 'light'
    preferencesForm.language = settings.language || 'zh-CN'
    preferencesForm.pageSize = settings.page_size || 20
    preferencesForm.autoSave = settings.auto_save !== false
    
    notificationsForm.emailEnabled = settings.email_enabled !== false
    notificationsForm.systemEnabled = settings.system_enabled !== false
    notificationsForm.failureAlert = settings.failure_alert !== false
    notificationsForm.analysisComplete = settings.analysis_complete !== false
    notificationsForm.reportReady = settings.report_ready !== false
    
    applySettingsToLocalStorage()
    applyTheme()
  } catch (error) {
    console.error('加载设置失败:', error)
    ElMessage.warning('加载设置失败，使用默认值')
    loadSettingsFromLocalStorage()
  } finally {
    loading.value = false
  }
}

const loadSettingsFromLocalStorage = () => {
  preferencesForm.theme = localStorage.getItem('theme') || 'light'
  preferencesForm.language = localStorage.getItem('language') || 'zh-CN'
  preferencesForm.pageSize = parseInt(localStorage.getItem('pageSize')) || 20
  preferencesForm.autoSave = localStorage.getItem('autoSave') !== 'false'
  
  notificationsForm.emailEnabled = localStorage.getItem('emailEnabled') !== 'false'
  notificationsForm.systemEnabled = localStorage.getItem('systemEnabled') !== 'false'
  notificationsForm.failureAlert = localStorage.getItem('failureAlert') !== 'false'
  notificationsForm.analysisComplete = localStorage.getItem('analysisComplete') !== 'false'
  notificationsForm.reportReady = localStorage.getItem('reportReady') !== 'false'
  
  applyTheme()
}

const applySettingsToLocalStorage = () => {
  localStorage.setItem('theme', preferencesForm.theme)
  localStorage.setItem('language', preferencesForm.language)
  localStorage.setItem('pageSize', preferencesForm.pageSize.toString())
  localStorage.setItem('autoSave', preferencesForm.autoSave.toString())
  
  localStorage.setItem('emailEnabled', notificationsForm.emailEnabled.toString())
  localStorage.setItem('systemEnabled', notificationsForm.systemEnabled.toString())
  localStorage.setItem('failureAlert', notificationsForm.failureAlert.toString())
  localStorage.setItem('analysisComplete', notificationsForm.analysisComplete.toString())
  localStorage.setItem('reportReady', notificationsForm.reportReady.toString())
  
  applyTheme()
}

const applyTheme = () => {
  console.log('applyTheme called, current theme:', preferencesForm.theme)
  const html = document.documentElement
  console.log('Before removal:', html.className)
  html.classList.remove('light', 'dark')
  console.log('After removal:', html.className)
  
  if (preferencesForm.theme === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    html.classList.add(prefersDark ? 'dark' : 'light')
    console.log('Auto theme, prefersDark:', prefersDark, 'Added class:', prefersDark ? 'dark' : 'light')
  } else {
    html.classList.add(preferencesForm.theme)
    console.log('Manual theme, Added class:', preferencesForm.theme)
  }
  
  console.log('Theme applied:', preferencesForm.theme, 'Classes:', html.className)
  console.log('HTML element:', html)
}

const savePreferences = async () => {
  console.log('savePreferences called')
  try {
    loading.value = true
    console.log('Before API call, theme:', preferencesForm.theme)
    await settingsApi.updateUserSettings({
      theme: preferencesForm.theme,
      language: preferencesForm.language,
      page_size: preferencesForm.pageSize,
      auto_save: preferencesForm.autoSave
    })
    
    console.log('After API call, calling applySettingsToLocalStorage')
    applySettingsToLocalStorage()
    console.log('After applySettingsToLocalStorage, calling applyTheme')
    applyTheme()
    console.log('After applyTheme')
    ElMessage.success('偏好设置已保存')
  } catch (error) {
    console.error('保存偏好设置失败:', error)
    ElMessage.error('保存偏好设置失败')
  } finally {
    loading.value = false
  }
}

const saveNotifications = async () => {
  try {
    loading.value = true
    await settingsApi.updateUserSettings({
      email_enabled: notificationsForm.emailEnabled,
      system_enabled: notificationsForm.systemEnabled,
      failure_alert: notificationsForm.failureAlert,
      analysis_complete: notificationsForm.analysisComplete,
      report_ready: notificationsForm.reportReady
    })
    
    applySettingsToLocalStorage()
    ElMessage.success('通知设置已保存')
  } catch (error) {
    console.error('保存通知设置失败:', error)
    ElMessage.error('保存通知设置失败')
  } finally {
    loading.value = false
  }
}

const changePassword = async () => {
  try {
    await passwordFormRef.value.validate()
    
    await authApi.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    
    ElMessage.success('密码修改成功，请重新登录')
    resetPasswordForm()
    
    setTimeout(() => {
      userStore.logout()
      window.location.href = '/login'
    }, 1500)
  } catch (error) {
    if (error.response?.data) {
      ElMessage.error(error.response.data.detail || '密码修改失败')
    } else {
      ElMessage.error('密码修改失败')
    }
  }
}

const resetPasswordForm = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordFormRef.value?.clearValidate()
}

onMounted(async () => {
  await userStore.fetchUserInfo()
  await loadSettings()
})
</script>

<style scoped>
.settings-container {
  max-width: 900px;
  margin: 0 auto;
}

.settings-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: var(--background-light);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.settings-form {
  max-width: 600px;
  margin-top: 20px;
}

.system-info {
  padding: 20px;
}

:deep(.el-tabs--border-card) {
  box-shadow: none;
  border: 1px solid var(--border-base);
  background: var(--background-light);
}

:deep(.el-tabs__item) {
  color: var(--text-regular);
}

:deep(.el-tabs__item.is-active) {
  color: var(--primary-color);
}

:deep(.el-descriptions) {
  margin-top: 20px;
}

:deep(.el-descriptions__label) {
  width: 120px;
  background-color: var(--background-base);
  color: var(--text-primary);
}

:deep(.el-descriptions__content) {
  color: var(--text-regular);
}

:deep(.el-form-item__label) {
  color: var(--text-regular);
}

:deep(.el-radio__label) {
  color: var(--text-regular);
}

:deep(.el-checkbox__label) {
  color: var(--text-regular);
}
</style>
