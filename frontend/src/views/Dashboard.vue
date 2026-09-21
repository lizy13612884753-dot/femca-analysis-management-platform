<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表板</h1>
      <p>欢迎使用FMECA设施设备分析管理平台</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stats-card" shadow="hover">
        <div class="stats-content">
          <div class="stats-icon equipment">
            <el-icon size="32"><Tools /></el-icon>
          </div>
          <div class="stats-info">
            <h3>{{ stats.equipmentTypes }}</h3>
            <p>设备类型</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <div class="stats-content">
          <div class="stats-icon instances">
            <el-icon size="32"><Monitor /></el-icon>
          </div>
          <div class="stats-info">
            <h3>{{ stats.equipmentInstances }}</h3>
            <p>设备实例</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <div class="stats-content">
          <div class="stats-icon failure">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stats-info">
            <h3>{{ stats.failureModes }}</h3>
            <p>故障模式</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <div class="stats-content">
          <div class="stats-icon analysis">
            <el-icon size="32"><DataAnalysis /></el-icon>
          </div>
          <div class="stats-info">
            <h3>{{ stats.analyses }}</h3>
            <p>危害度分析</p>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-grid">
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>设备状态分布</span>
          </div>
        </template>
        <div ref="equipmentStatusChart" class="chart-container"></div>
      </el-card>
      
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>故障模式分布</span>
          </div>
        </template>
        <div ref="failureModeChart" class="chart-container"></div>
      </el-card>
    </div>
    
    <!-- 最近活动 -->
    <el-card class="activity-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
          <el-button type="text" size="small" @click="refreshActivities">刷新</el-button>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="activity in recentActivities"
          :key="activity.id"
          :timestamp="activity.timestamp"
          :type="activity.type"
        >
          {{ activity.description }}
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Tools, Monitor, Warning, DataAnalysis } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getDashboardOverview } from '@/api/dashboard'

// 响应式数据
const stats = ref({
  equipmentTypes: 0,
  equipmentInstances: 0,
  failureModes: 0,
  analyses: 0
})

const recentActivities = ref([])
const equipmentStatusData = ref([])
const failureModeData = ref([])

const equipmentStatusChart = ref(null)
const failureModeChart = ref(null)

// 初始化图表
const initCharts = () => {
  nextTick(() => {
    // 设备状态分布图
    if (equipmentStatusChart.value) {
      const chart1 = echarts.init(equipmentStatusChart.value)
      chart1.setOption({
        title: {
          text: '',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#3498db',
          borderWidth: 1,
          textStyle: {
            color: '#2c3e50'
          }
        },
        legend: {
          bottom: '0%',
          left: 'center',
          textStyle: {
            color: '#7f8c8d'
          }
        },
        series: [
          {
            name: '设备状态',
            type: 'pie',
            radius: '70%',
            data: equipmentStatusData.value.length > 0 ? equipmentStatusData.value : [
              { value: 0, name: '运行中' },
              { value: 0, name: '维护中' },
              { value: 0, name: '故障' },
              { value: 0, name: '离线' },
              { value: 0, name: '已退役' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 15,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            color: [
              '#43e97b',  // 运行中 - 绿色
              '#f093fb',  // 维护中 - 粉色
              '#f5576c',  // 故障 - 红色
              '#4facfe',  // 离线 - 蓝色
              '#667eea'   // 已退役 - 紫色
            ]
          }
        ]
      })
    }
    
    // 故障模式分布图
    if (failureModeChart.value) {
      const chart2 = echarts.init(failureModeChart.value)
      
      // 从故障模式数据中提取x轴标签和y轴数据
      const xAxisData = failureModeData.value.map(item => item.name)
      const seriesData = failureModeData.value.map(item => item.value)
      
      chart2.setOption({
        title: {
          text: '',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#3498db',
          borderWidth: 1,
          textStyle: {
            color: '#2c3e50'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: xAxisData.length > 0 ? xAxisData : ['机械故障', '电气故障', '液压故障', '控制系统', '其他'],
          axisLabel: {
            interval: 0,
            rotate: 45,
            fontSize: 10,
            color: '#7f8c8d',
            formatter: function(value) {
              // 限制标签长度，超过10个字符则缩写
              if (value.length > 10) {
                return value.substring(0, 10) + '...';
              }
              return value;
            }
          },
          axisLine: {
            lineStyle: {
              color: '#e9ecef'
            }
          },
          axisTick: {
            lineStyle: {
              color: '#e9ecef'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#7f8c8d'
          },
          axisLine: {
            lineStyle: {
              color: '#e9ecef'
            }
          },
          axisTick: {
            lineStyle: {
              color: '#e9ecef'
            }
          },
          splitLine: {
            lineStyle: {
              color: '#f8f9fa',
              type: 'dashed'
            }
          }
        },
        series: [
          {
            name: '故障数量',
            type: 'bar',
            data: seriesData.length > 0 ? seriesData : [0, 0, 0, 0, 0],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#667eea' },
                { offset: 1, color: '#764ba2' }
              ]),
              borderRadius: [8, 8, 0, 0],
              shadowColor: 'rgba(102, 126, 234, 0.3)',
              shadowBlur: 10,
              shadowOffsetY: 5
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#764ba2' },
                  { offset: 1, color: '#667eea' }
                ]),
                shadowBlur: 20,
                shadowOffsetY: 10
              }
            },
            barWidth: '60%'
          }
        ]
      })
    }
  })
}

// 刷新活动
const refreshActivities = () => {
  loadStats()
  ElMessage.success('活动列表已刷新')
}

// 加载统计数据
const loadStats = async () => {
  try {
    // 调用API获取统计数据
    const response = await getDashboardOverview()
    stats.value = {
      equipmentTypes: response.equipment_stats?.total_equipment_types || 0,
      equipmentInstances: response.equipment_stats?.total_equipment_instances || 0,
      failureModes: response.failure_stats?.total_failure_modes || 0,
      analyses: response.hazard_analysis_stats?.analyzed_failure_modes || 0
    }
    
    // 更新设备状态分布数据
    if (response.equipment_stats?.status_distribution) {
      equipmentStatusData.value = response.equipment_stats.status_distribution
    }
    
    // 更新故障模式分布数据
    if (response.failure_stats?.mode_distribution) {
      failureModeData.value = response.failure_stats.mode_distribution
    }
    
    // 更新最近活动
    if (response.recent_activities) {
      recentActivities.value = response.recent_activities
    }
    
    // 重新初始化图表
    initCharts()
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

onMounted(() => {
  loadStats()
  
  // 窗口大小改变时重新渲染图表
  window.addEventListener('resize', () => {
    initCharts()
  })
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.page-header {
  margin-bottom: 32px;
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.page-header h1 {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.page-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 16px;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stats-card {
  border: none;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
}

.stats-icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.stats-card:hover .stats-icon {
  transform: scale(1.1);
}

.stats-icon.equipment {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-icon.instances {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stats-icon.failure {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stats-icon.analysis {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stats-info h3 {
  margin: 0 0 8px 0;
  font-size: 36px;
  font-weight: 700;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.stats-card:hover .stats-info h3 {
  color: #3498db;
}

.stats-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 16px;
  font-weight: 500;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  border: none;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  background: white;
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #e9ecef;
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.chart-container {
  height: 320px;
  width: 100%;
  padding: 20px;
}

.activity-card {
  border: none;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  background: white;
  transition: all 0.3s ease;
}

.activity-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

:deep(.el-timeline-item__content) {
  font-size: 14px;
  color: #495057;
  line-height: 1.6;
}

:deep(.el-timeline-item__timestamp) {
  color: #95a5a6;
  font-size: 12px;
}

:deep(.el-timeline-item__node) {
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.1);
}

@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
    border-radius: 8px;
  }
  
  .page-header {
    padding: 15px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .stats-content {
    padding: 20px;
  }
  
  .stats-icon {
    width: 64px;
    height: 64px;
  }
  
  .stats-info h3 {
    font-size: 28px;
  }
  
  .chart-container {
    height: 280px;
    padding: 15px;
  }
}
</style>