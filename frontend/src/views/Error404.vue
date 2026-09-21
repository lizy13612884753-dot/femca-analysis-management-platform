<template>
  <div class="error-404">
    <div class="error-content">
      <el-icon size="120" color="#909399"><Warning /></el-icon>
      <h1>404</h1>
      <p>抱歉，您访问的页面不存在</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script setup>
import { Warning } from '@element-plus/icons-vue'
</script>

<style scoped>
.error-404 {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.error-content {
  text-align: center;
}

.error-content h1 {
  font-size: 72px;
  color: #909399;
  margin: 20px 0;
}

.error-content p {
  font-size: 18px;
  color: #606266;
  margin-bottom: 30px;
}
</style>
