<template>
  <div class="profile">
    <div class="page-header">
      <h1>个人资料</h1>
      <p>管理您的个人信息和账户设置</p>
    </div>
    
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="profile-card">
          <div class="avatar-section">
            <el-avatar :size="100" :src="userInfo.avatar || ''">
              {{ userInfo.username ? userInfo.username.charAt(0).toUpperCase() : 'U' }}
            </el-avatar>
            <h3>{{ userInfo.username || '用户名' }}</h3>
            <p>{{ userInfo.email || '邮箱' }}</p>
            <el-tag :type="userInfo.is_active ? 'success' : 'danger'" size="small">
              {{ userInfo.is_active ? '活跃' : '禁用' }}
            </el-tag>
          </div>
          
          <el-divider />
          
          <div class="info-section">
            <div class="info-item">
              <span class="label">用户ID:</span>
              <span class="value">{{ userInfo.id || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">角色:</span>
              <span class="value">{{ userInfo.role || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">注册时间:</span>
              <span class="value">{{ formatDate(userInfo.date_joined) || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="label">最后登录:</span>
              <span class="value">{{ formatDate(userInfo.last_login) || '-' }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card>
          <el-tabs v-model="activeTab" type="border-card">
            <el-tab-pane label="基本信息" name="basic">
              <el-form :model="profileForm" :rules="profileRules" ref="profileFormRef" label-width="120px">
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="profileForm.username" disabled />
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="profileForm.email" />
                </el-form-item>
                <el-form-item label="姓" prop="first_name">
                  <el-input v-model="profileForm.first_name" />
                </el-form-item>
                <el-form-item label="名" prop="last_name">
                  <el-input v-model="profileForm.last_name" />
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                  <el-input v-model="profileForm.phone" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleUpdateProfile" :loading="loading">
                    保存修改
                  </el-button>
                  <el-button @click="handleResetProfile">重置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <el-tab-pane label="修改密码" name="password">
              <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
                <el-form-item label="当前密码" prop="old_password">
                  <el-input v-model="passwordForm.old_password" type="password" show-password />
                </el-form-item>
                <el-form-item label="新密码" prop="new_password">
                  <el-input v-model="passwordForm.new_password" type="password" show-password />
                </el-form-item>
                <el-form-item label="确认密码" prop="new_password_confirm">
                  <el-input v-model="passwordForm.new_password_confirm" type="password" show-password />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">
                    修改密码
                  </el-button>
                  <el-button @click="handleResetPassword">重置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const activeTab = ref('basic')
const loading = ref(false)
const passwordLoading = ref(false)
const userInfo = ref({})

const profileForm = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const profileRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  first_name: [
    { required: true, message: '请输入姓', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: '请输入名', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const profileFormRef = ref(null)
const passwordFormRef = ref(null)

const loadUserInfo = async () => {
  try {
    const response = await request({
      url: '/auth/user/info/',
      method: 'get'
    })
    userInfo.value = response
    
    profileForm.value = {
      username: response.username || '',
      email: response.email || '',
      first_name: response.first_name || '',
      last_name: response.last_name || '',
      phone: response.phone || ''
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  }
}

const handleUpdateProfile = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await request({
          url: `/users/${userInfo.value.id}/`,
          method: 'patch',
          data: profileForm.value
        })
        ElMessage.success('个人信息修改成功')
        await loadUserInfo()
      } catch (error) {
        console.error('修改个人信息失败:', error)
        ElMessage.error('修改个人信息失败')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleResetProfile = () => {
  if (profileFormRef.value) {
    profileFormRef.value.resetFields()
  }
  profileForm.value = {
    username: userInfo.value.username || '',
    email: userInfo.value.email || '',
    first_name: userInfo.value.first_name || '',
    last_name: userInfo.value.last_name || '',
    phone: userInfo.value.phone || ''
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        await request({
          url: '/users/change_password/',
          method: 'post',
          data: {
            old_password: passwordForm.value.old_password,
            new_password: passwordForm.value.new_password,
            new_password_confirm: passwordForm.value.new_password_confirm
          }
        })
        ElMessage.success('密码修改成功，请重新登录')
        handleResetPassword()
      } catch (error) {
        console.error('修改密码失败:', error)
        ElMessage.error(error.response?.data?.message || error.response?.data?.detail || '修改密码失败')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

const handleResetPassword = () => {
  if (passwordFormRef.value) {
    passwordFormRef.value.resetFields()
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.profile {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  margin-bottom: 8px;
}

.page-header p {
  color: #606266;
  margin: 0;
}

.profile-card {
  text-align: center;
}

.avatar-section {
  padding: 20px 0;
}

.avatar-section .el-avatar {
  margin-bottom: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 40px;
  font-weight: bold;
}

.avatar-section h3 {
  margin: 10px 0;
  font-size: 20px;
  color: #303133;
}

.avatar-section p {
  margin: 5px 0 15px;
  color: #909399;
}

.info-section {
  text-align: left;
  padding: 0 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #909399;
  font-weight: 500;
}

.info-item .value {
  color: #303133;
  font-weight: 600;
}
</style>
