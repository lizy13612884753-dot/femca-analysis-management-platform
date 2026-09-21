<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  // 检查用户登录状态
  await userStore.checkAuthStatus()
  
  // 如果未登录，重定向到登录页
  if (!userStore.isAuthenticated && router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
})
</script>

<style scoped>
#app {
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 0;
}
</style>