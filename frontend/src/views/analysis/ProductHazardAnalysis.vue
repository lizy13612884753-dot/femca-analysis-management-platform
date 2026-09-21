<template>
  <div class="product-hazard-analysis">
    <div class="page-header">
      <h1>产品危害度分析</h1>
      <p>对设备产品进行危害度汇总和综合评估</p>
    </div>
    
    <el-tabs v-model="activeTab" type="border-card" class="analysis-tabs" @tab-click="handleTabChange">
      <!-- 产品危害度汇总 -->
      <el-tab-pane label="产品危害度汇总" name="summary">
        <div class="tab-content">
          <el-card class="filter-card">
            <el-form :inline="true" :model="filterForm">
              <el-form-item label="设备类型">
                <el-select v-model="filterForm.equipmentType" placeholder="选择设备类型" clearable>
                  <el-option
                    v-for="type in equipmentTypes"
                    :key="type.id"
                    :label="type.name"
                    :value="type.id"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="产品名称">
                <el-input v-model="filterForm.productName" placeholder="搜索产品名称" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
                <el-button @click="handleReset">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <el-card class="table-card">
            <el-table :data="productSummaryData" stripe style="width: 100%">
              <el-table-column prop="product_name" label="产品名称" min-width="150" />
              <el-table-column prop="equipment_type" label="设备类型" width="150" />
              <el-table-column prop="total_failure_modes" label="故障模式数量" width="120" />
              <el-table-column prop="high_hazard_count" label="高危害数量" width="100">
                <template #default="{ row }">
                  <el-tag type="danger">{{ row.high_hazard_count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="medium_hazard_count" label="中危害数量" width="100">
                <template #default="{ row }">
                  <el-tag type="warning">{{ row.medium_hazard_count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="low_hazard_count" label="低危害数量" width="100">
                <template #default="{ row }">
                  <el-tag type="success">{{ row.low_hazard_count }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="average_rpn" label="平均风险优先级" width="140" />
              <el-table-column prop="overall_hazard_level" label="整体危害等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getHazardType(row.overall_hazard_level)">
                    {{ row.overall_hazard_level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="handleView(row)">
                    详情
                  </el-button>
                  <el-button type="warning" link size="small" @click="handleEvaluate(row)">
                    评估
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-card>
        </div>
      </el-tab-pane>
      
      <!-- 产品综合评估 -->
      <el-tab-pane label="产品综合评估" name="evaluation">
        <div class="tab-content">
          <el-card class="evaluation-card">
            <template #header>
              <div class="card-header">
                <span>产品综合评估</span>
                <el-select v-model="evaluationProductId" @change="loadProductEvaluation">
                  <el-option
                    v-for="product in productSummaryData"
                    :key="product.id"
                    :label="product.product_name"
                    :value="product.id"
                  />
                </el-select>
              </div>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="产品名称">{{ currentEvaluation.product_name }}</el-descriptions-item>
              <el-descriptions-item label="设备类型">{{ currentEvaluation.equipment_type }}</el-descriptions-item>
              <el-descriptions-item label="故障模式数量">{{ currentEvaluation.total_failure_modes }}</el-descriptions-item>
              <el-descriptions-item label="平均风险优先级">{{ currentEvaluation.average_rpn }}</el-descriptions-item>
              <el-descriptions-item label="整体危害等级">
                <el-tag :type="getHazardType(currentEvaluation.overall_hazard_level)">
                  {{ currentEvaluation.overall_hazard_level }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="风险评估结果">{{ currentEvaluation.risk_assessment_result }}</el-descriptions-item>
              <el-descriptions-item label="改进建议" :span="2">{{ currentEvaluation.improvement_suggestions }}</el-descriptions-item>
              <el-descriptions-item label="评估时间" :span="2">{{ currentEvaluation.evaluation_time }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>
      </el-tab-pane>
      
      <!-- 产品危害度可视化 -->
      <el-tab-pane label="产品危害度可视化" name="visualization">
        <div class="tab-content">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <span>产品危害等级分布</span>
                </template>
                <div ref="productHazardLevelChart" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <span>产品风险优先级分布</span>
                </template>
                <div ref="productRiskPriorityChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <span>产品风险趋势分析</span>
                </template>
                <div ref="productRiskTrendChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 产品详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="产品危害度详情" width="600px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="产品名称">{{ currentDetail.product_name }}</el-descriptions-item>
        <el-descriptions-item label="设备类型">{{ currentDetail.equipment_type }}</el-descriptions-item>
        <el-descriptions-item label="故障模式数量">{{ currentDetail.total_failure_modes }}</el-descriptions-item>
        <el-descriptions-item label="平均风险优先级">{{ currentDetail.average_rpn }}</el-descriptions-item>
        <el-descriptions-item label="整体危害等级">
          <el-tag :type="getHazardType(currentDetail.overall_hazard_level)">
            {{ currentDetail.overall_hazard_level }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="高危害数量">{{ currentDetail.high_hazard_count }}</el-descriptions-item>
        <el-descriptions-item label="中危害数量">{{ currentDetail.medium_hazard_count }}</el-descriptions-item>
        <el-descriptions-item label="低危害数量">{{ currentDetail.low_hazard_count }}</el-descriptions-item>
        <el-descriptions-item label="故障模式详情" :span="2">
          <el-table :data="currentDetail.failure_modes" size="small" style="width: 100%">
            <el-table-column prop="failure_mode" label="故障模式" width="180" />
            <el-table-column prop="hazard_level" label="危害等级" width="100">
              <template #default="{ row }">
                <el-tag :type="getHazardType(row.hazard_level)">
                  {{ row.hazard_level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="risk_priority" label="风险优先级数" width="120" />
          </el-table>
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEvaluate(currentDetail)">
          评估
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 产品评估对话框 -->
    <el-dialog v-model="evaluateDialogVisible" title="产品综合评估" width="600px">
      <el-form :model="evaluateForm" label-width="120px">
        <el-form-item label="产品名称">
          <el-input v-model="evaluateForm.product_name" disabled />
        </el-form-item>
        <el-form-item label="设备类型">
          <el-input v-model="evaluateForm.equipment_type" disabled />
        </el-form-item>
        <el-form-item label="整体危害等级">
          <el-select v-model="evaluateForm.overall_hazard_level" placeholder="请选择整体危害等级">
            <el-option label="严重" value="严重" />
            <el-option label="高" value="高" />
            <el-option label="中" value="中" />
            <el-option label="低" value="低" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险评估结果">
          <el-input v-model="evaluateForm.risk_assessment_result" placeholder="请输入风险评估结果" />
        </el-form-item>
        <el-form-item label="改进建议">
          <el-input v-model="evaluateForm.improvement_suggestions" type="textarea" placeholder="请输入改进建议" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="evaluateDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEvaluation">保存评估</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Warning, Plus, Edit, Delete, Setting, Calculator, Sort, DataAnalysis } from '@element-plus/icons-vue'
import * as equipmentApi from '@/api/equipment'
import * as productAnalysisApi from '@/api/product_analysis'
import * as echarts from 'echarts'

// 标签页状态
const activeTab = ref('summary')

const filterForm = reactive({
  equipmentType: '',
  productName: ''
})

// 设备类型列表
const equipmentTypes = ref([])

// 产品危害度汇总数据
const productSummaryData = ref([
  {
    id: 1,
    product_name: '电梯A型号',
    equipment_type: '电梯',
    total_failure_modes: 5,
    high_hazard_count: 2,
    medium_hazard_count: 2,
    low_hazard_count: 1,
    average_rpn: 180,
    overall_hazard_level: '高',
    failure_modes: [
      { failure_mode: '门系统故障', hazard_level: '高', risk_priority: 168 },
      { failure_mode: '制动器失灵', hazard_level: '严重', risk_priority: 252 },
      { failure_mode: '控制系统故障', hazard_level: '中', risk_priority: 120 },
      { failure_mode: '钢丝绳磨损', hazard_level: '中', risk_priority: 130 },
      { failure_mode: '按钮失灵', hazard_level: '低', risk_priority: 80 }
    ]
  },
  {
    id: 2,
    product_name: '空调系统B型号',
    equipment_type: '空调系统',
    total_failure_modes: 3,
    high_hazard_count: 0,
    medium_hazard_count: 2,
    low_hazard_count: 1,
    average_rpn: 110,
    overall_hazard_level: '中',
    failure_modes: [
      { failure_mode: '制冷剂泄漏', hazard_level: '中', risk_priority: 126 },
      { failure_mode: '压缩机故障', hazard_level: '中', risk_priority: 140 },
      { failure_mode: '风扇故障', hazard_level: '低', risk_priority: 90 }
    ]
  }
])

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)
const detailDialogVisible = ref(false)
const currentDetail = ref({})

// 产品评估相关
const evaluateDialogVisible = ref(false)
const evaluateForm = reactive({
  product_name: '',
  equipment_type: '',
  overall_hazard_level: '',
  risk_assessment_result: '',
  improvement_suggestions: ''
})
const currentEvaluation = ref({})
const currentEvaluateRow = ref({})
const evaluationProductId = ref('')

// 图表引用
const productHazardLevelChart = ref(null)
const productRiskPriorityChart = ref(null)
const productRiskTrendChart = ref(null)

const getHazardType = (level) => {
  const levelMap = {
    '严重': 'danger',
    '高': 'warning',
    '中': 'info',
    '低': 'success'
  }
  return levelMap[level] || 'info'
}

const handleSearch = () => {
  ElMessage.success('搜索功能开发中')
}

const handleReset = () => {
  filterForm.equipmentType = ''
  filterForm.productName = ''
  ElMessage.success('重置成功')
}

const handleView = (row) => {
  currentDetail.value = row
  detailDialogVisible.value = true
}

const handleEvaluate = (row) => {
  currentEvaluateRow.value = row
  // 初始化评估表单
  Object.assign(evaluateForm, {
    product_name: row.product_name,
    equipment_type: row.equipment_type,
    overall_hazard_level: row.overall_hazard_level,
    risk_assessment_result: '',
    improvement_suggestions: ''
  })
  evaluateDialogVisible.value = true
}

const saveEvaluation = async () => {
  try {
    // 构建评估数据
    const evaluationData = {
      product_id: currentEvaluateRow.value.id,
      product_name: evaluateForm.product_name,
      equipment_type: evaluateForm.equipment_type,
      overall_hazard_level: evaluateForm.overall_hazard_level,
      risk_assessment_result: evaluateForm.risk_assessment_result,
      improvement_suggestions: evaluateForm.improvement_suggestions,
      evaluation_time: new Date().toLocaleString()
    }
    
    // 调用API保存评估结果
    // await productAnalysisApi.saveEvaluation(evaluationData)
    
    ElMessage.success('评估结果保存成功')
    evaluateDialogVisible.value = false
    
    // 更新评估数据
    currentEvaluation.value = evaluationData
  } catch (error) {
    ElMessage.error('保存评估结果失败')
  }
}

const loadProductEvaluation = async () => {
  try {
    // 调用API加载产品评估数据
    // const response = await productAnalysisApi.getProductEvaluation(evaluationProductId.value)
    // currentEvaluation.value = response.data || {}
    
    // 模拟数据
    const product = productSummaryData.value.find(item => item.id === evaluationProductId.value)
    if (product) {
      currentEvaluation.value = {
        product_name: product.product_name,
        equipment_type: product.equipment_type,
        total_failure_modes: product.total_failure_modes,
        average_rpn: product.average_rpn,
        overall_hazard_level: product.overall_hazard_level,
        risk_assessment_result: '产品整体风险可控，建议定期维护',
        improvement_suggestions: '加强设备定期检查，提高维护频率',
        evaluation_time: new Date().toLocaleString()
      }
    }
  } catch (error) {
    ElMessage.error('加载产品评估数据失败')
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadData()
}

// 危害度可视化相关方法
const initCharts = () => {
  initProductHazardLevelChart()
  initProductRiskPriorityChart()
  initProductRiskTrendChart()
}

const initProductHazardLevelChart = () => {
  if (!productHazardLevelChart.value) return
  
  const chart = echarts.init(productHazardLevelChart.value)
  
  // 模拟数据
  const hazardLevelData = {
    '严重': 1,
    '高': 1,
    '中': 2,
    '低': 1
  }
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '危害等级',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: Object.entries(hazardLevelData).map(([name, value]) => ({
          name,
          value
        }))
      }
    ]
  }
  
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const initProductRiskPriorityChart = () => {
  if (!productRiskPriorityChart.value) return
  
  const chart = echarts.init(productRiskPriorityChart.value)
  
  // 模拟数据
  const products = productSummaryData.value.map(item => item.product_name)
  const rpnValues = productSummaryData.value.map(item => item.average_rpn)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: products
    },
    yAxis: {
      type: 'value',
      name: '平均风险优先级数'
    },
    series: [
      {
        name: '平均风险优先级数',
        type: 'bar',
        data: rpnValues,
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value > 200) return '#f56c6c'
            if (value > 150) return '#e6a23c'
            if (value > 100) return '#409eff'
            return '#67c23a'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const initProductRiskTrendChart = () => {
  if (!productRiskTrendChart.value) return
  
  const chart = echarts.init(productRiskTrendChart.value)
  
  // 模拟数据
  const months = ['1月', '2月', '3月', '4月', '5月', '6月']
  const elevatorData = [180, 175, 170, 165, 160, 155]
  const hvacData = [110, 115, 120, 118, 115, 112]
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['电梯', '空调系统']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: months
    },
    yAxis: {
      type: 'value',
      name: '平均风险优先级数'
    },
    series: [
      {
        name: '电梯',
        type: 'line',
        data: elevatorData,
        smooth: true,
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '空调系统',
        type: 'line',
        data: hvacData,
        smooth: true,
        itemStyle: {
          color: '#67c23a'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 加载设备类型列表
const loadEquipmentTypes = async () => {
  try {
    const response = await equipmentApi.getEquipmentTypes()
    equipmentTypes.value = response.results || []
  } catch (error) {
    ElMessage.error('加载设备类型列表失败')
  }
}

const loadData = () => {
  // 加载数据逻辑
}

// 监听标签页切换，重新初始化图表
const handleTabChange = (tab) => {
  // tab是一个对象，包含pane属性
  const tabName = tab.props.name
  activeTab.value = tabName
  if (tabName === 'visualization') {
    setTimeout(() => {
      initCharts()
    }, 100)
  }
}

onMounted(() => {
  loadEquipmentTypes()
  loadData()
  
  // 延迟初始化图表，确保DOM已渲染
  setTimeout(() => {
    initCharts()
  }, 100)
})
</script>

<style scoped>
.product-hazard-analysis {
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

.analysis-tabs {
  margin-bottom: 20px;
}

.tab-content {
  padding: 20px;
}

.action-bar {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-container {
  width: 100%;
  height: 350px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.evaluation-card {
  margin-bottom: 20px;
}

.el-tabs__header {
  margin-bottom: 0;
}

.el-tabs__content {
  padding: 20px;
  background-color: #f5f7fa;
  border: 1px solid #ebeef5;
  border-top: none;
  border-radius: 0 0 4px 4px;
}
</style>