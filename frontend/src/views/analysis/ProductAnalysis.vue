<template>
  <div class="product-analysis">
    <div class="page-header">
      <h1>产品危害度分析</h1>
      <p>对设备系统进行整体危害度评估和风险排序</p>
    </div>
    
    <el-card class="filter-card" style="margin-bottom: 20px">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="设备类型">
          <el-select v-model="filterForm.equipmentType" placeholder="选择设备类型" clearable style="width: 250px" @change="handleEquipmentTypeChange">
            <el-option
              v-for="type in equipmentTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadAnalysisData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
          <el-button type="success" @click="openCreateDialog">
            <el-icon><Plus /></el-icon>
            创建新分析
          </el-button>
          <el-button @click="handleExportReport">
            <el-icon><Download /></el-icon>
            导出报告
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-row :gutter="20" v-if="currentAnalysis">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ currentAnalysis.total_failure_modes }}</div>
            <div class="stat-label">总故障模式数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ currentAnalysis.analyzed_failure_modes }}</div>
            <div class="stat-label">已分析故障模式</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value">{{ currentAnalysis.avg_rpn?.toFixed(2) || 0 }}</div>
            <div class="stat-label">平均RPN</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-value" :class="getRiskLevelClass(currentAnalysis.overall_risk_level)">
              {{ getRiskLevelText(currentAnalysis.overall_risk_level) }}
            </div>
            <div class="stat-label">整体风险等级</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>风险矩阵分析</span>
              <el-button type="primary" link size="small" @click="handleExportReport">导出报告</el-button>
            </div>
          </template>
          <div class="chart-container">
            <div ref="riskMatrixChart" style="width: 100%; height: 400px"></div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span>危害度排名</span>
              <el-button type="primary" link size="small" @click="loadAnalysisData">刷新</el-button>
            </div>
          </template>
          <el-table :data="riskRanking" stripe size="small" :loading="loading">
            <el-table-column prop="rank" label="排名" width="60" />
            <el-table-column prop="failure_mode" label="故障模式" min-width="120" />
            <el-table-column prop="rpn" label="RPN" width="70" />
            <el-table-column prop="risk_level" label="风险等级" width="90">
              <template #default="{ row }">
                <el-tag :type="getRiskTagType(row.risk_level)" size="small">
                  {{ getRiskLevelText(row.risk_level) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="analysis-details" style="margin-top: 20px" v-if="currentAnalysis">
      <template #header>
        <div class="card-header">
          <span>详细分析报告</span>
          <div>
            <el-button type="warning" size="small" @click="handleRecalculate" :loading="recalculating">
              <el-icon><Refresh /></el-icon>
              重新计算
            </el-button>
            <el-button type="primary" size="small" @click="handleExportReport">
              <el-icon><Download /></el-icon>
              生成报告
            </el-button>
          </div>
        </div>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="设备类型">{{ currentAnalysis.equipment_type_name || '全部设备类型' }}</el-descriptions-item>
        <el-descriptions-item label="分析日期">{{ currentAnalysis.analysis_date ? formatDate(currentAnalysis.analysis_date) : '汇总分析' }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ currentAnalysis.created_by_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="总故障模式">{{ currentAnalysis.total_failure_modes || '-' }}</el-descriptions-item>
        <el-descriptions-item label="已分析故障模式">{{ currentAnalysis.analyzed_failure_modes || '-' }}</el-descriptions-item>
        <el-descriptions-item label="平均严酷度">{{ currentAnalysis.avg_severity?.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="平均发生概率">{{ currentAnalysis.avg_occurrence?.toFixed(2) }}%</el-descriptions-item>
        <el-descriptions-item label="平均检测概率">{{ currentAnalysis.avg_detection?.toFixed(2) }}%</el-descriptions-item>
        <el-descriptions-item label="平均RPN">{{ currentAnalysis.avg_rpn?.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="最高RPN">{{ currentAnalysis.max_rpn }}</el-descriptions-item>
        <el-descriptions-item label="最低RPN">{{ currentAnalysis.min_rpn }}</el-descriptions-item>
        <el-descriptions-item label="整体风险等级">
          <el-tag :type="getRiskTagType(currentAnalysis.overall_risk_level)">
            {{ getRiskLevelText(currentAnalysis.overall_risk_level) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      
      <div style="margin-top: 20px">
        <h4>风险等级分布</h4>
        <el-row :gutter="20" style="margin-top: 10px">
          <el-col :span="6">
            <div class="risk-distribution-item critical">
              <div class="risk-label">严重风险</div>
              <div class="risk-value">{{ currentAnalysis.critical_count }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="risk-distribution-item high">
              <div class="risk-label">高风险</div>
              <div class="risk-value">{{ currentAnalysis.high_count }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="risk-distribution-item medium">
              <div class="risk-label">中等风险</div>
              <div class="risk-value">{{ currentAnalysis.medium_count }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="risk-distribution-item low">
              <div class="risk-label">低风险</div>
              <div class="risk-value">{{ currentAnalysis.low_count }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div style="margin-top: 20px">
        <h4>评估结论</h4>
        <p>{{ currentAnalysis.assessment_conclusion || '暂无评估结论' }}</p>
      </div>
      
      <div style="margin-top: 20px">
        <h4>改进建议</h4>
        <p>{{ currentAnalysis.recommendations || '暂无改进建议' }}</p>
      </div>
    </el-card>
    
    <el-dialog v-model="createDialogVisible" title="创建新的产品危害度分析" width="500px">
      <el-form :model="createForm" label-width="120px">
        <el-form-item label="设备类型" required>
          <el-select v-model="createForm.equipment_type" placeholder="选择设备类型" style="width: 100%">
            <el-option
              v-for="type in equipmentTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评估结论">
          <el-input v-model="createForm.assessment_conclusion" type="textarea" :rows="3" placeholder="请输入评估结论" />
        </el-form-item>
        <el-form-item label="改进建议">
          <el-input v-model="createForm.recommendations" type="textarea" :rows="3" placeholder="请输入改进建议" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateAnalysis" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { productAnalysisApi } from '@/api/product_analysis'
import { failureAnalysisApi } from '@/api/failure_analysis'
import { getEquipmentTypes } from '@/api/equipment'

const loading = ref(false)
const recalculating = ref(false)
const creating = ref(false)
const createDialogVisible = ref(false)
const currentAnalysis = ref(null)
const equipmentTypes = ref([])
const riskMatrixChart = ref(null)
let chartInstance = null

const filterForm = ref({
  equipmentType: null
})

const createForm = ref({
  equipment_type: null,
  assessment_conclusion: '',
  recommendations: ''
})

const riskRanking = ref([])

const loadEquipmentTypes = async () => {
  try {
    // 只获取活跃状态的设备类型
    const response = await getEquipmentTypes({ status: 'active' })
    console.log('设备类型API响应:', response)
    
    if (response && response.results && Array.isArray(response.results)) {
      equipmentTypes.value = response.results
    } else if (Array.isArray(response)) {
      equipmentTypes.value = response
    } else {
      equipmentTypes.value = []
    }
    
    console.log('设备类型数据:', equipmentTypes.value)
    
    // 检查当前选择的设备类型是否在活跃设备类型列表中
    if (filterForm.value.equipmentType) {
      const isActive = equipmentTypes.value.some(type => type.id === filterForm.value.equipmentType)
      if (!isActive) {
        // 如果当前选择的设备类型不在活跃列表中，直接重置为null
        filterForm.value.equipmentType = null
        // 重新加载数据，显示整体汇总
        await loadAnalysisData()
      }
    }
  } catch (error) {
    console.error('加载设备类型失败:', error)
    ElMessage.error('加载设备类型失败')
    equipmentTypes.value = []
  }
}

const loadRiskRanking = async () => {
  try {
    const params = {}
    if (filterForm.value.equipmentType) {
      params.failure_mode__equipment_type = filterForm.value.equipmentType
    }
    
    const response = await failureAnalysisApi.getAnalyses(params)
    console.log('风险排名API响应:', response)
    
    let analyses = []
    if (response && response.results && Array.isArray(response.results)) {
      analyses = response.results
    } else if (Array.isArray(response)) {
      analyses = response
    }
    
    console.log('故障分析数据:', analyses)
    
    riskRanking.value = analyses.slice(0, 10).map((analysis, index) => ({
      rank: index + 1,
      failure_mode: analysis.failure_mode_name || analysis.failure_mode?.name || '未知',
      rpn: analysis.risk_priority_number || 0,
      risk_level: analysis.risk_level || 'low'
    }))
    
    console.log('风险排名数据:', riskRanking.value)
  } catch (error) {
    console.error('加载风险排名失败:', error)
    riskRanking.value = []
  }
}

const loadAnalysisData = async () => {
  loading.value = true
  try {
    let response
    // 检查设备类型是否存在于活跃设备类型列表中
    const isEquipmentTypeActive = filterForm.value.equipmentType ? 
      equipmentTypes.value.some(type => type.id === filterForm.value.equipmentType) : 
      true
    
    if (filterForm.value.equipmentType && isEquipmentTypeActive) {
      try {
        response = await productAnalysisApi.getLatestAnalysis(filterForm.value.equipmentType)
      } catch (error) {
        if (error.response && error.response.status === 404) {
          // 设备类型不存在或已被删除，直接重置为null
          filterForm.value.equipmentType = null
          // 重新加载数据，显示整体汇总
          await loadAnalysisData()
          return
        }
        throw error
      }
    } else {
      // 设备类型不存在或不活跃，直接获取整体汇总
      response = await productAnalysisApi.getOverallSummary()
    }
    
    console.log('产品分析API响应:', response)
    
    if (response && typeof response === 'object') {
      currentAnalysis.value = response
      console.log('当前分析数据:', currentAnalysis.value)
    } else {
      currentAnalysis.value = null
      console.log('未找到分析结果')
    }
    
    await loadRiskRanking()
    await nextTick()
    initRiskMatrixChart()
    
    if (!currentAnalysis.value) {
      ElMessage.info('未找到分析结果，请创建新的分析')
    }
  } catch (error) {
    console.error('加载分析数据失败:', error)
    ElMessage.error('加载分析数据失败')
    currentAnalysis.value = null
    await loadRiskRanking()
    await nextTick()
    initRiskMatrixChart()
  } finally {
    loading.value = false
  }
}

const handleEquipmentTypeChange = () => {
  // 检查用户选择的设备类型是否在活跃设备类型列表中
  if (filterForm.value.equipmentType) {
    const isActive = equipmentTypes.value.some(type => type.id === filterForm.value.equipmentType)
    if (!isActive) {
      // 如果用户选择的设备类型不在活跃列表中，直接重置为null
      filterForm.value.equipmentType = null
    }
  }
  loadAnalysisData()
}

const openCreateDialog = () => {
  createForm.value = {
    equipment_type: filterForm.value.equipmentType || null,
    assessment_conclusion: '',
    recommendations: ''
  }
  createDialogVisible.value = true
}

const handleCreateAnalysis = async () => {
  if (!createForm.value.equipment_type) {
    ElMessage.warning('请选择设备类型')
    return
  }
  
  creating.value = true
  try {
    await productAnalysisApi.createAnalysis(createForm.value)
    ElMessage.success('创建成功')
    createDialogVisible.value = false
    await loadAnalysisData()
  } catch (error) {
    console.error('创建分析失败:', error)
    ElMessage.error('创建分析失败')
  } finally {
    creating.value = false
  }
}

const handleRecalculate = async () => {
  if (!currentAnalysis.value) return
  
  // 检查是否有分析ID，如果没有则提示用户创建分析
  if (!currentAnalysis.value.id) {
    ElMessage.warning('请先创建分析结果，然后再进行重新计算')
    return
  }
  
  recalculating.value = true
  try {
    await productAnalysisApi.recalculateAnalysis(currentAnalysis.value.id)
    ElMessage.success('重新计算成功')
    await loadAnalysisData()
  } catch (error) {
    console.error('重新计算失败:', error)
    ElMessage.error('重新计算失败')
  } finally {
    recalculating.value = false
  }
}

const handleExportReport = () => {
  ElMessage.info('导出报告功能开发中')
}

const initRiskMatrixChart = () => {
  if (!riskMatrixChart.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(riskMatrixChart.value)
  
  const scatterData = riskRanking.value.map((item, index) => {
    let xIndex = 0
    let yIndex = 0
    
    if (item.rpn >= 200) {
      xIndex = 2
      yIndex = 2
    } else if (item.rpn >= 100) {
      xIndex = 1
      yIndex = 2
    } else if (item.rpn >= 50) {
      xIndex = 1
      yIndex = 1
    } else if (item.rpn >= 20) {
      xIndex = 0
      yIndex = 1
    } else {
      xIndex = 0
      yIndex = 0
    }
    
    return {
      value: [xIndex, yIndex],
      name: item.failure_mode,
      rpn: item.rpn,
      risk_level: item.risk_level,
      symbolSize: 15 + (item.rpn / 10),
      itemStyle: {
        color: getRiskColor(item.risk_level)
      },
      originalX: xIndex,
      originalY: yIndex
    }
  })
  
  const positionGroups = {}
  scatterData.forEach((item, index) => {
    const key = `${item.originalX}-${item.originalY}`
    if (!positionGroups[key]) {
      positionGroups[key] = []
    }
    positionGroups[key].push(index)
  })
  
  Object.keys(positionGroups).forEach(key => {
    const indices = positionGroups[key]
    if (indices.length > 1) {
      const angleStep = (2 * Math.PI) / indices.length
      const radius = 0.15
      
      indices.forEach((itemIndex, i) => {
        const angle = angleStep * i
        const offsetX = Math.cos(angle) * radius
        const offsetY = Math.sin(angle) * radius
        scatterData[itemIndex].value = [
          scatterData[itemIndex].originalX + offsetX,
          scatterData[itemIndex].originalY + offsetY
        ]
      })
    }
  })
  
  const heatmapData = []
  for (let x = 0; x < 3; x++) {
    for (let y = 0; y < 3; y++) {
      const pointsInCell = scatterData.filter(p => p.value[0] === x && p.value[1] === y)
      if (pointsInCell.length > 0) {
        const maxRpn = Math.max(...pointsInCell.map(p => p.rpn))
        heatmapData.push([x, y, maxRpn])
      } else {
        heatmapData.push([x, y, 0])
      }
    }
  }
  
  const maxRpnValue = scatterData.length > 0 ? Math.max(...scatterData.map(p => p.rpn)) : 300
  
  const option = {
    title: {
      text: '风险矩阵图',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (!params || !params.data) return ''
        
        if (params.componentType === 'series') {
          if (params.seriesName === '故障点') {
            const x = params.data.value[0]
            const y = params.data.value[1]
            const pointsInCell = scatterData.filter(p => p.value[0] === x && p.value[1] === y)
            
            if (pointsInCell.length > 1) {
              let result = `<strong>该位置有 ${pointsInCell.length} 个故障模式：</strong><br/>`
              pointsInCell.forEach((p, i) => {
                result += `${i + 1}. ${p.name} (RPN: ${p.rpn}, 风险等级: ${getRiskLevelText(p.risk_level)})<br/>`
              })
              return result
            } else {
              return `${params.data.name}<br/>RPN: ${params.data.rpn}<br/>风险等级: ${getRiskLevelText(params.data.risk_level)}`
            }
          } else if (params.seriesName === '风险矩阵') {
            const value = params.data.value || params.data
            if (!value || !Array.isArray(value)) return ''
            
            const pointsInCell = scatterData.filter(p => p.value[0] === value[0] && p.value[1] === value[1])
            if (pointsInCell.length > 0) {
              return `发生概率: ${['低', '中', '高'][value[0]]}<br/>严重性: ${['低', '中', '高'][value[1]]}<br/>最高RPN: ${value[2]}<br/>故障数: ${pointsInCell.length}`
            }
            return `发生概率: ${['低', '中', '高'][value[0]]}<br/>严重性: ${['低', '中', '高'][value[1]]}<br/>最高RPN: 0`
          }
        }
        return ''
      }
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '15%'
    },
    xAxis: {
      type: 'category',
      name: '发生概率',
      data: ['低', '中', '高'],
      axisLine: {
        lineStyle: {
          width: 2
        }
      }
    },
    yAxis: {
      type: 'category',
      name: '严重性',
      data: ['低', '中', '高'],
      axisLine: {
        lineStyle: {
          width: 2
        }
      }
    },
    visualMap: {
      min: 0,
      max: maxRpnValue || 300,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#67c23a', '#e6a23c', '#f56c6c']
      }
    },
    series: [
      {
        name: '风险矩阵',
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: true,
          formatter: (params) => {
            return params.value[2] > 0 ? params.value[2] : ''
          }
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      },
      {
        name: '故障点',
        type: 'scatter',
        data: scatterData,
        symbolSize: 20,
        itemStyle: {
          color: '#303133',
          borderColor: '#fff',
          borderWidth: 2
        }
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const getRiskLevelText = (level) => {
  const levelMap = {
    'critical': '严重风险',
    'high': '高风险',
    'medium': '中等风险',
    'low': '低风险'
  }
  return levelMap[level] || level
}

const getRiskTagType = (level) => {
  const typeMap = {
    'critical': 'danger',
    'high': 'warning',
    'medium': 'info',
    'low': 'success'
  }
  return typeMap[level] || 'info'
}

const getRiskLevelClass = (level) => {
  const classMap = {
    'critical': 'risk-critical',
    'high': 'risk-high',
    'medium': 'risk-medium',
    'low': 'risk-low'
  }
  return classMap[level] || ''
}

const getRiskColor = (level) => {
  const colorMap = {
    'critical': '#f56c6c',
    'high': '#e6a23c',
    'medium': '#409eff',
    'low': '#67c23a'
  }
  return colorMap[level] || '#909399'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadEquipmentTypes()
  loadAnalysisData()
  
  window.addEventListener('resize', () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  })
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  })
})
</script>

<style scoped>
.product-analysis {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-card {
  background: #f5f7fa;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-value.risk-critical {
  color: #f56c6c;
}

.stat-value.risk-high {
  color: #e6a23c;
}

.stat-value.risk-medium {
  color: #409eff;
}

.stat-value.risk-low {
  color: #67c23a;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.chart-container {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.risk-distribution-item {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  color: white;
}

.risk-distribution-item.critical {
  background: linear-gradient(135deg, #f56c6c, #ff8787);
}

.risk-distribution-item.high {
  background: linear-gradient(135deg, #e6a23c, #f0c78a);
}

.risk-distribution-item.medium {
  background: linear-gradient(135deg, #409eff, #66b1ff);
}

.risk-distribution-item.low {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.risk-label {
  font-size: 14px;
  margin-bottom: 8px;
}

.risk-value {
  font-size: 32px;
  font-weight: bold;
}

.analysis-details h4 {
  margin-bottom: 10px;
  color: #303133;
}

.analysis-details p {
  color: #606266;
  line-height: 1.6;
}
</style>
