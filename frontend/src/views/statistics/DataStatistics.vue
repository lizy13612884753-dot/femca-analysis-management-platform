<template>
  <div class="data-statistics">
    <div class="page-header">
      <h1>数据统计</h1>
      <p>设备FMECA分析数据统计与可视化展示</p>
    </div>
    
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon equipment">
              <el-icon size="28"><Tools /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ overviewData.equipment_stats?.total_equipment_types || 0 }}</h3>
              <p>设备类型</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon failure">
              <el-icon size="28"><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ overviewData.failure_stats?.total_failure_modes || 0 }}</h3>
              <p>故障模式</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon analysis">
              <el-icon size="28"><DataAnalysis /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ overviewData.hazard_analysis_stats?.analyzed_failure_modes || 0 }}</h3>
              <p>已分析故障</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>故障模式分布</span>
          </template>
          <div ref="failureDistributionChart" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>风险趋势分析</span>
          </template>
          <div ref="riskTrendChart" style="width: 100%; height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>设备故障统计</span>
          <div>
            <el-select v-model="selectedPeriod" placeholder="选择时间段" style="width: 120px; margin-right: 10px" @change="handlePeriodChange">
              <el-option label="本周" value="week" />
              <el-option label="本月" value="month" />
              <el-option label="本年" value="year" />
            </el-select>
            <el-button type="primary" link size="small" @click="handleExportData">导出数据</el-button>
          </div>
        </div>
      </template>
      <el-table :data="equipmentFailureData" stripe :loading="loading">
        <el-table-column prop="equipment_type_name" label="设备类型" width="150" />
        <el-table-column prop="failure_count" label="故障次数" width="100" align="center" />
        <el-table-column prop="analyzed_count" label="已分析" width="100" align="center" />
        <el-table-column prop="analysis_rate" label="分析率" width="100" align="center">
          <template #default="{ row }">
            {{ ((row.analyzed_count / row.failure_count) * 100).toFixed(1) }}%
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>严酷度分布</span>
          </template>
          <div ref="severityDistributionChart" style="width: 100%; height: 250px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>风险等级分布</span>
          </template>
          <div ref="riskLevelDistributionChart" style="width: 100%; height: 250px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  Tools,
  Warning,
  DataAnalysis
} from '@element-plus/icons-vue'
import * as dashboardApi from '@/api/dashboard'

const loading = ref(false)
const selectedPeriod = ref('month')
const overviewData = ref({})
const equipmentFailureData = ref([])

const failureDistributionChart = ref(null)
const riskTrendChart = ref(null)
const severityDistributionChart = ref(null)
const riskLevelDistributionChart = ref(null)

let failureDistributionChartInstance = null
let riskTrendChartInstance = null
let severityDistributionChartInstance = null
let riskLevelDistributionChartInstance = null

const loadOverviewData = async () => {
  try {
    const response = await dashboardApi.getDashboardOverview()
    overviewData.value = response
  } catch (error) {
    console.error('加载概览数据失败:', error)
  }
}

const loadEquipmentFailureData = async () => {
  loading.value = true
  try {
    const response = await dashboardApi.getEquipmentFailureDistribution()
    
    if (!response || !response.labels || !response.datasets || !response.datasets[0] || !response.datasets[0].data) {
      console.warn('设备故障数据格式不正确或为空')
      equipmentFailureData.value = []
      return
    }
    
    equipmentFailureData.value = response.labels.map((label, index) => ({
      equipment_type_name: label,
      failure_count: response.datasets[0].data[index],
      analyzed_count: response.datasets[1]?.data[index] || 0,
      status: getEquipmentStatus(response.datasets[1]?.data[index] || 0, response.datasets[0].data[index])
    }))
  } catch (error) {
    console.error('加载设备故障数据失败:', error)
    ElMessage.error('加载设备故障数据失败')
  } finally {
    loading.value = false
  }
}

const getEquipmentStatus = (analyzed, total) => {
  const rate = (analyzed / total) * 100
  if (rate >= 80) return '良好'
  if (rate >= 50) return '正常'
  if (rate >= 20) return '需关注'
  return '危险'
}

const getStatusType = (status) => {
  const statusMap = {
    '良好': 'success',
    '正常': 'info',
    '需关注': 'warning',
    '危险': 'danger'
  }
  return statusMap[status] || 'info'
}

const handlePeriodChange = () => {
  initRiskTrendChart()
}

const handleExportData = () => {
  ElMessage.info('导出数据功能开发中')
}

const initFailureDistributionChart = async () => {
  if (!failureDistributionChart.value) return
  
  if (failureDistributionChartInstance) {
    failureDistributionChartInstance.dispose()
  }
  
  failureDistributionChartInstance = echarts.init(failureDistributionChart.value)
  
  try {
    const response = await dashboardApi.getEquipmentFailureDistribution()
    
    if (!response || !response.labels || !response.datasets || !response.datasets[0] || !response.datasets[0].data) {
      console.warn('故障模式分布数据格式不正确或为空')
      return
    }
    
    const option = {
      title: {
        text: '故障模式分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '故障模式总数',
          type: 'pie',
          radius: '50%',
          data: response.labels.map((label, index) => ({
            value: response.datasets[0].data[index],
            name: label
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            formatter: '{b}: {d}%'
          }
        }
      ]
    }
    
    failureDistributionChartInstance.setOption(option)
  } catch (error) {
    console.error('加载故障模式分布数据失败:', error)
  }
}

const initRiskTrendChart = async () => {
  if (!riskTrendChart.value) return
  
  if (riskTrendChartInstance) {
    riskTrendChartInstance.dispose()
  }
  
  riskTrendChartInstance = echarts.init(riskTrendChart.value)
  
  try {
    const days = selectedPeriod.value === 'week' ? 7 : selectedPeriod.value === 'month' ? 30 : 365
    console.log('开始加载风险趋势数据，天数:', days)
    
    const response = await dashboardApi.getHazardTrend({ days: days })
    
    console.log('风险趋势API响应:', response)
    console.log('响应类型:', typeof response)
    console.log('是否为数组:', Array.isArray(response))
    
    if (!response || typeof response !== 'object') {
      console.warn('风险趋势数据不是有效的对象')
      return
    }
    
    if (!response.labels || !response.datasets || !response.datasets[0] || !response.datasets[0].data) {
      console.warn('风险趋势数据格式不正确或为空', {
        hasLabels: !!response.labels,
        hasDatasets: !!response.datasets,
        hasFirstDataset: !!response.datasets?.[0],
        hasData: !!response.datasets?.[0]?.data
      })
      return
    }
    
    const option = {
      title: {
        text: '风险趋势分析',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: '{b}<br/>平均RPN: {c}'
      },
      xAxis: {
        type: 'category',
        data: response.labels
      },
      yAxis: {
        type: 'value',
        name: 'RPN值'
      },
      series: [
        {
          name: '平均RPN值趋势',
          type: 'line',
          data: response.datasets[0].data,
          smooth: true,
          areaStyle: {
            color: 'rgba(75, 192, 192, 0.3)'
          }
        }
      ]
    }
    
    riskTrendChartInstance.setOption(option)
    console.log('风险趋势图表初始化成功')
  } catch (error) {
    console.error('加载风险趋势数据失败:', error)
    console.error('错误详情:', {
      message: error.message,
      stack: error.stack,
      name: error.name
    })
  }
}

const initSeverityDistributionChart = async () => {
  if (!severityDistributionChart.value) return
  
  if (severityDistributionChartInstance) {
    severityDistributionChartInstance.dispose()
  }
  
  severityDistributionChartInstance = echarts.init(severityDistributionChart.value)
  
  try {
    const response = await dashboardApi.getSeverityDistribution()
    
    if (!response || !response.labels || !response.datasets || !response.datasets[0] || !response.datasets[0].data) {
      console.warn('严酷度分布数据格式不正确或为空')
      return
    }
    
    const option = {
      title: {
        text: '严酷度分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
      },
      xAxis: {
        type: 'category',
        data: response.labels
      },
      yAxis: {
        type: 'value',
        name: '数量'
      },
      series: [
        {
          name: '故障模式数量',
          type: 'bar',
          data: response.datasets[0].data,
          itemStyle: {
            color: 'rgba(54, 162, 235, 0.6)'
          }
        }
      ]
    }
    
    severityDistributionChartInstance.setOption(option)
  } catch (error) {
    console.error('加载严酷度分布数据失败:', error)
  }
}

const initRiskLevelDistributionChart = async () => {
  if (!riskLevelDistributionChart.value) return
  
  if (riskLevelDistributionChartInstance) {
    riskLevelDistributionChartInstance.dispose()
  }
  
  riskLevelDistributionChartInstance = echarts.init(riskLevelDistributionChart.value)
  
  try {
    const response = await dashboardApi.getRiskLevelDistribution()
    
    if (!response || !response.labels || !response.datasets || !response.datasets[0] || !response.datasets[0].data) {
      console.warn('风险等级分布数据格式不正确或为空')
      return
    }
    
    const option = {
      title: {
        text: '风险等级分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '风险等级分布',
          type: 'pie',
          radius: ['40%', '70%'],
          data: response.labels.map((label, index) => ({
            value: response.datasets[0].data[index],
            name: label
          })),
          label: {
            show: true,
            formatter: '{b}: {d}%'
          }
        }
      ]
    }
    
    riskLevelDistributionChartInstance.setOption(option)
  } catch (error) {
    console.error('加载风险等级分布数据失败:', error)
  }
}

onMounted(async () => {
  await loadOverviewData()
  await loadEquipmentFailureData()
  
  await nextTick()
  await Promise.all([
    initFailureDistributionChart(),
    initRiskTrendChart(),
    initSeverityDistributionChart(),
    initRiskLevelDistributionChart()
  ])
  
  window.addEventListener('resize', () => {
    if (failureDistributionChartInstance) failureDistributionChartInstance.resize()
    if (riskTrendChartInstance) riskTrendChartInstance.resize()
    if (severityDistributionChartInstance) severityDistributionChartInstance.resize()
    if (riskLevelDistributionChartInstance) riskLevelDistributionChartInstance.resize()
  })
})

onUnmounted(() => {
  if (failureDistributionChartInstance) failureDistributionChartInstance.dispose()
  if (riskTrendChartInstance) riskTrendChartInstance.dispose()
  if (severityDistributionChartInstance) severityDistributionChartInstance.dispose()
  if (riskLevelDistributionChartInstance) riskLevelDistributionChartInstance.dispose()
  
  window.removeEventListener('resize', () => {
    if (failureDistributionChartInstance) failureDistributionChartInstance.resize()
    if (riskTrendChartInstance) riskTrendChartInstance.resize()
    if (severityDistributionChartInstance) severityDistributionChartInstance.resize()
    if (riskLevelDistributionChartInstance) riskLevelDistributionChartInstance.resize()
  })
})
</script>

<style scoped>
.data-statistics {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 8px;
}

.page-header p {
  color: #909399;
  font-size: 14px;
}

.stat-cards {
  margin-top: 20px;
}

.stat-card {
  cursor: pointer;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stat-icon.equipment {
  background-color: #ecf5ff;
  color: #409eff;
}

.stat-icon.failure {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.analysis {
  background-color: #f0f9eb;
  color: #67c23a;
}

.stat-icon.measure {
  background-color: #fef0f0;
  color: #f56c6c;
}

.stat-info h3 {
  font-size: 28px;
  color: #303133;
  margin: 0 0 5px 0;
}

.stat-info p {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>