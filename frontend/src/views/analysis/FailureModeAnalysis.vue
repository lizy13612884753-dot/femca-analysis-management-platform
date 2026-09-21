<template>
  <div class="failure-mode-analysis">
    <div class="page-header">
      <h1>故障模式危害度分析</h1>
      <p>对设备故障模式进行危害度评估和分析</p>
    </div>
    
    <el-tabs v-model="activeTab" type="border-card" class="analysis-tabs" @tab-click="handleTabChange">
      <!-- 危害度参数配置 -->
      <el-tab-pane label="危害度参数配置" name="parameters">
        <div class="tab-content">
          <div class="action-bar">
            <el-button type="primary" @click="openParameterForm">
              <el-icon><Plus /></el-icon>
              新增参数
            </el-button>
          </div>
          
          <el-card class="table-card">
            <el-table :data="parameters" stripe style="width: 100%">
              <el-table-column prop="name" label="参数名称" min-width="150" />
              <el-table-column prop="parameter_type" label="参数类型" width="120">
                <template #default="{ row }">
                  {{ getParameterTypeName(row.parameter_type) }}
                </template>
              </el-table-column>
              <el-table-column prop="min_value" label="最小值" width="100" />
              <el-table-column prop="max_value" label="最大值" width="100" />
              <el-table-column prop="default_value" label="默认值" width="100" />
              <el-table-column prop="unit" label="单位" width="80" />
              <el-table-column prop="is_active" label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'danger'">
                    {{ row.is_active ? '启用' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="openParameterForm(row)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteParameter(row)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </el-tab-pane>
      
      <!-- 危害度计算 -->
      <el-tab-pane label="危害度计算" name="calculation">
        <div class="tab-content">
          <el-card class="filter-card">
            <el-form :inline="true" :model="filterForm">
              <el-form-item label="设备类型">
                <el-select v-model="filterForm.equipmentType" placeholder="选择设备类型" clearable style="width: 300px">
                  <el-option
                    v-for="type in equipmentTypes"
                    :key="type.id"
                    :label="type.name"
                    :value="type.id"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="故障模式">
                <el-input v-model="filterForm.failureMode" placeholder="搜索故障模式" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
                <el-button @click="handleReset">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <el-card class="table-card">
            <el-table :data="tableData" :loading="loading" stripe style="width: 100%">
              <el-table-column prop="equipment_type" label="设备类型" width="150">
                <template #default="{ row }">
                  {{ getEquipmentTypeName(row.equipment_type) }}
                </template>
              </el-table-column>
              <el-table-column prop="project_instance_name" label="项目实例名称" width="150" />
              <el-table-column prop="failure_mode" label="故障模式" width="180" />
              <el-table-column prop="severity" label="严酷度等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getSeverityType(row.severity)">
                    {{ row.severity }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="risk_priority" label="风险优先级数" width="140" />
              <el-table-column prop="hazard_level" label="危害等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getHazardType(row.hazard_level)">
                    {{ row.hazard_level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="recommended_action" label="使用补偿措施" min-width="200" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="handleView(row)">
                    详情
                  </el-button>
                  <el-button type="warning" link size="small" @click="handleAnalyze(row)">
                    分析
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="pagination.page"
                v-model:page-size="pagination.pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-card>
        </div>
      </el-tab-pane>
      
      <!-- 危害度排序 -->
      <el-tab-pane label="危害度排序" name="ranking">
        <div class="tab-content">
          <el-card class="table-card">
            <template #header>
              <div class="card-header">
                <span>危害度等级排序</span>
                <div class="header-actions">
                  <el-select v-model="sortBy" @change="handleSortChange" style="width: 200px; margin-right: 10px">
                    <el-option label="按风险优先级数" value="risk_priority" />
                    <el-option label="按严酷度" value="severity" />
                    <el-option label="按危害等级" value="hazard_level" />
                    <el-option label="按故障模式危害度" value="failure_hazard" />
                  </el-select>
                  <el-button type="primary" @click="exportRankingData">
                    <el-icon><Download /></el-icon>
                    导出
                  </el-button>
                </div>
              </div>
            </template>
            <el-table :data="sortedData" stripe style="width: 100%">
              <el-table-column label="排名" width="80">
                <template #default="{ $index }">
                  <el-tag :type="getRankingType($index + 1)">{{ $index + 1 }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="equipment_type" label="设备类型" width="150">
                <template #default="{ row }">
                  {{ getEquipmentTypeName(row.equipment_type) }}
                </template>
              </el-table-column>
              <el-table-column prop="project_instance_name" label="项目实例名称" width="150" />
              <el-table-column prop="failure_mode" label="故障模式" width="180" />
              <el-table-column prop="risk_priority" label="风险优先级数" width="140" sortable>
                <template #default="{ row }">
                  <el-tag :type="getRPNType(row.risk_priority)">{{ row.risk_priority }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="severity" label="严酷度等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getSeverityType(row.severity)">
                    {{ row.severity }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="hazard_level" label="危害等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getHazardType(row.hazard_level)">
                    {{ row.hazard_level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="failureHazard" label="故障模式危害度" width="140">
                <template #default="{ row }">
                  <span>{{ (row.failureHazard || 0).toFixed(4) }}</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="handleView(row)">
                    详情
                  </el-button>
                  <el-button type="warning" link size="small" @click="handleAnalyze(row)">
                    分析
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </el-tab-pane>
      
      <!-- 危害度可视化 -->
      <el-tab-pane label="危害度可视化" name="visualization">
        <div class="tab-content">
          <el-card class="filter-card" style="margin-bottom: 20px">
            <el-form :inline="true">
              <el-form-item label="设备类型">
                <el-select v-model="visualizationFilter.equipmentType" placeholder="全部设备类型" clearable style="width: 300px" @change="updateVisualization">
                  <el-option
                    v-for="type in equipmentTypes"
                    :key="type.id"
                    :label="type.name"
                    :value="type.id"
                  />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="refreshCharts">
                  <el-icon><Refresh /></el-icon>
                  刷新图表
                </el-button>
                <el-button type="success" @click="exportCharts">
                  <el-icon><Download /></el-icon>
                  导出图表
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card class="chart-card">
                <template #header>
                  <span>危害等级分布</span>
                </template>
                <div ref="hazardLevelChart" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="chart-card">
                <template #header>
                  <span>严酷度等级分布</span>
                </template>
                <div ref="severityChart" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="chart-card">
                <template #header>
                  <span>风险优先级分布</span>
                </template>
                <div ref="riskPriorityChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <span>风险矩阵分析</span>
                </template>
                <div ref="riskMatrixChart" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <span>故障模式危害度对比</span>
                </template>
                <div ref="failureHazardChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <span>产品危害度分析</span>
                </template>
                <div ref="productHazardChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 参数配置对话框 -->
    <el-dialog v-model="parameterDialogVisible" :title="isEditParameter ? '编辑参数' : '新增参数'" width="600px">
      <el-form ref="parameterFormRef" :model="parameterForm" :rules="parameterFormRules">
        <el-form-item label="参数名称" prop="name">
          <el-input v-model="parameterForm.name" placeholder="请输入参数名称" />
        </el-form-item>
        <el-form-item label="参数类型" prop="parameter_type">
          <el-select v-model="parameterForm.parameter_type" placeholder="请选择参数类型">
            <el-option label="严酷度" value="severity" />
            <el-option label="发生概率" value="occurrence" />
            <el-option label="检测概率" value="detection" />
            <el-option label="风险" value="risk" />
          </el-select>
        </el-form-item>
        <el-form-item label="参数描述" prop="description">
          <el-input v-model="parameterForm.description" type="textarea" placeholder="请输入参数描述" />
        </el-form-item>
        <el-form-item label="最小值" prop="min_value">
          <el-input v-model.number="parameterForm.min_value" type="number" placeholder="请输入最小值" />
        </el-form-item>
        <el-form-item label="最大值" prop="max_value">
          <el-input v-model.number="parameterForm.max_value" type="number" placeholder="请输入最大值" />
        </el-form-item>
        <el-form-item label="默认值" prop="default_value">
          <el-input v-model.number="parameterForm.default_value" type="number" placeholder="请输入默认值" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="parameterForm.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="parameterForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="parameterDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitParameterForm">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 故障模式详细信息对话框 -->
    <el-dialog v-model="detailDialogVisible" title="故障模式详细信息" width="600px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="设备类型">{{ currentDetail.equipment_type }}</el-descriptions-item>
        <el-descriptions-item label="故障模式">{{ currentDetail.failure_mode }}</el-descriptions-item>
        <el-descriptions-item label="严酷度等级">{{ currentDetail.severity }}</el-descriptions-item>
        <el-descriptions-item label="风险优先级数">{{ currentDetail.risk_priority }}</el-descriptions-item>
        <el-descriptions-item label="危害等级">
          <el-tag :type="getHazardType(currentDetail.hazard_level)">
            {{ currentDetail.hazard_level }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="使用补偿措施" :span="2">
          {{ currentDetail.recommended_action }}
        </el-descriptions-item>
        <el-descriptions-item label="故障原因" :span="2">
          {{ currentDetail.failure_cause }}
        </el-descriptions-item>
        <el-descriptions-item label="影响分析" :span="2">
          {{ currentDetail.impact_analysis }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleAnalyze(currentDetail)">
          开始分析
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 危害度分析对话框 -->
    <el-dialog v-model="analyzeDialogVisible" title="危害度分析" width="600px">
      <el-form :model="analyzeForm" label-width="140px">
        <el-form-item label="故障模式">
          <el-input v-model="currentAnalyzeRow.failure_mode" disabled />
        </el-form-item>
        <el-form-item label="设备类型">
          <el-input v-model="currentAnalyzeRow.equipment_type" disabled />
        </el-form-item>
        <el-form-item label="严酷度等级">
          <el-input v-model="analyzeForm.severity" disabled />
        </el-form-item>
        <el-form-item label="严酷度值">
          <el-input v-model.number="analyzeForm.severity_value" type="number" placeholder="请输入严酷度值" />
        </el-form-item>
        <el-form-item label="发生概率(%)">
          <el-input v-model.number="analyzeForm.occurrence_probability" type="number" placeholder="请输入发生概率" />
        </el-form-item>
        <el-form-item label="检测概率(%)">
          <el-input v-model.number="analyzeForm.detection_probability" type="number" placeholder="请输入检测概率" />
        </el-form-item>
        <el-form-item label="使用补偿措施">
          <el-input v-model="analyzeForm.recommended_action" type="textarea" :rows="3" placeholder="请输入使用补偿措施" />
        </el-form-item>
        <el-form-item label="分析说明">
          <el-input v-model="analyzeForm.notes" type="textarea" :rows="2" placeholder="请输入分析说明" />
        </el-form-item>
        <el-form-item label="风险优先级数">
          <el-input v-model="analyzeForm.risk_priority" disabled />
        </el-form-item>
        <el-form-item label="危害等级">
          <el-input v-model="analyzeForm.hazard_level" disabled />
        </el-form-item>
        <el-form-item label="严重度系数αj">
          <el-input v-model="analyzeForm.alpha" type="number" placeholder="请输入严重度系数" />
        </el-form-item>
        <el-form-item label="发生概率系数βj">
          <el-input v-model="analyzeForm.beta" type="number" placeholder="请输入发生概率系数" />
        </el-form-item>
        <el-form-item label="故障率λp (×10⁻⁶/h)">
          <el-input v-model="analyzeForm.lambdaP" type="number" placeholder="请输入故障率" />
        </el-form-item>
        <el-form-item label="运行时间t (h)">
          <el-input v-model="analyzeForm.time" type="number" placeholder="请输入运行时间" />
        </el-form-item>
        <el-form-item label="故障模式危害度Cmj (×10⁻³)">
          <el-input v-model="analyzeForm.failureHazard" disabled />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="analyzeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="calculateRPN">计算RPN</el-button>
        <el-button type="warning" @click="calculateCmj">计算危害度</el-button>
        <el-button type="success" @click="saveAnalysisResult">保存结果</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Warning, Plus, Edit, Delete, Setting, Sort, DataAnalysis, Download, Refresh } from '@element-plus/icons-vue'
import * as equipmentApi from '@/api/equipment'
import * as failureApi from '@/api/failure'
import failureAnalysisApi from '@/api/failure_analysis'
import * as productAnalysisApi from '@/api/product_analysis'
import * as severityApi from '@/api/severity'
import * as echarts from 'echarts'

// 标签页状态
const activeTab = ref('parameters')

const filterForm = reactive({
  equipmentType: null,
  failureMode: ''
})

// 设备类型列表
const equipmentTypes = ref([])

// 危害度参数列表
const parameters = ref([])

// 严酷度评定数据
const severityAssessments = ref([])

const tableData = ref([])

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 加载状态
const loading = ref(false)
const detailDialogVisible = ref(false)
const currentDetail = ref({})

// 参数配置相关
const parameterDialogVisible = ref(false)
const parameterForm = reactive({
  name: '',
  parameter_type: '',
  description: '',
  min_value: 0,
  max_value: 10,
  default_value: 1,
  unit: '',
  is_active: true
})
const parameterFormRules = {
  name: [{ required: true, message: '请输入参数名称', trigger: 'blur' }],
  parameter_type: [{ required: true, message: '请选择参数类型', trigger: 'change' }],
  min_value: [{ required: true, message: '请输入最小值', trigger: 'blur' }],
  max_value: [{ required: true, message: '请输入最大值', trigger: 'blur' }],
  default_value: [{ required: true, message: '请输入默认值', trigger: 'blur' }]
}
const parameterFormRef = ref(null)
const isEditParameter = ref(false)
const currentParameterId = ref(null)

// 排序相关
const sortBy = ref('risk_priority')

// 可视化过滤器
const visualizationFilter = reactive({
  equipmentType: null
})

// 图表引用
const hazardLevelChart = ref(null)
const severityChart = ref(null)
const riskPriorityChart = ref(null)
const riskMatrixChart = ref(null)
const failureHazardChart = ref(null)
const productHazardChart = ref(null)

const getSeverityType = (severity) => {
  const severityMap = {
    'Ⅰ': 'danger',
    'Ⅱ': 'warning',
    'Ⅲ': 'info',
    'Ⅳ': 'success',
    'A': 'danger',
    'B': 'warning',
    'C': 'info',
    'D': 'success',
    'E': 'info',
    'I类': 'danger',
    'II类': 'warning',
    'III类': 'info',
    'I': 'danger',
    'II': 'warning',
    'III': 'info'
  }
  return severityMap[severity] || 'info'
}

const convertSeverityToRoman = (severity) => {
  const severityMap = {
    'A': 'Ⅰ',
    'B': 'Ⅱ',
    'C': 'Ⅲ',
    'D': 'Ⅳ',
    'E': 'Ⅳ',
    'I类': 'Ⅰ',
    'II类': 'Ⅱ',
    'III类': 'Ⅲ',
    'I': 'Ⅰ',
    'II': 'Ⅱ',
    'III': 'Ⅲ'
  }
  return severityMap[severity] || severity
}

const getHazardType = (level) => {
  const levelMap = {
    '严重': 'danger',
    '高': 'warning',
    '中': 'info',
    '低': 'success'
  }
  return levelMap[level] || 'info'
}

const getRankingType = (rank) => {
  if (rank === 1) return 'danger'
  if (rank <= 3) return 'warning'
  if (rank <= 5) return 'primary'
  return 'info'
}

const getRPNType = (rpn) => {
  if (rpn >= 200) return 'danger'
  if (rpn >= 150) return 'warning'
  if (rpn >= 100) return 'primary'
  return 'success'
}

const getParameterTypeName = (type) => {
  const typeMap = {
    'severity': '严酷度',
    'occurrence': '发生概率',
    'detection': '检测概率',
    'risk': '风险'
  }
  return typeMap[type] || type
}

// 原始表格数据，用于恢复
const originalTableData = ref([...tableData.value])

const handleSearch = () => {
  pagination.page = 1
  loadData()
  
  ElMessage.success('搜索完成')
}

const handleReset = () => {
  filterForm.equipmentType = null
  filterForm.failureMode = ''
  
  pagination.page = 1
  loadData()
  
  ElMessage.success('重置成功')
}

const handleView = (row) => {
  currentDetail.value = row
  detailDialogVisible.value = true
}

// 危害度计算相关
const analyzeDialogVisible = ref(false)
const analyzeForm = reactive({
  severity: '',
  severity_value: 1,
  occurrence_probability: 1,
  detection_probability: 1,
  recommended_action: '',
  notes: '',
  risk_priority: 0,
  hazard_level: '',
  alpha: 0,
  beta: 0,
  lambdaP: 0,
  time: 0,
  failureHazard: 0
})
const productHazard = ref(0)
const currentAnalyzeRow = ref({})

const handleAnalyze = async (row) => {
  currentAnalyzeRow.value = row
  
  // 从严酷度评定数据中查找对应的严酷度等级
  let severityLevel = ''
  const failureModeName = row.failure_mode || row.name
  if (failureModeName) {
    const assessment = severityAssessments.value.find(item => {
      return item.failure_mode_name === failureModeName || 
             item.failure_mode === failureModeName ||
             (typeof item.failure_mode === 'object' && item.failure_mode.name === failureModeName)
    })
    if (assessment) {
      severityLevel = assessment.severity_level_code || assessment.severity_level
    }
  }
  
  // 尝试获取已存在的分析结果
  try {
    const analyses = await failureAnalysisApi.getAnalyses({ failure_mode: row.id })
    if (analyses.results && analyses.results.length > 0) {
      const existingAnalysis = analyses.results[0]
      Object.assign(analyzeForm, {
        severity: existingAnalysis.severity_level_name || severityLevel || row.severity || '',
        severity_value: existingAnalysis.severity_value || 1,
        occurrence_probability: existingAnalysis.occurrence_probability || 1,
        detection_probability: existingAnalysis.detection_probability || 1,
        recommended_action: existingAnalysis.recommended_action || '',
        notes: existingAnalysis.notes || '',
        risk_priority: existingAnalysis.risk_priority_number || 0,
        hazard_level: existingAnalysis.risk_level || '',
        alpha: 0,
        beta: 0,
        lambdaP: 0,
        time: 0,
        failureHazard: 0
      })
    } else {
      // 初始化分析表单
      Object.assign(analyzeForm, {
        severity: severityLevel || row.severity || '',
        severity_value: 1,
        occurrence_probability: 1,
        detection_probability: 1,
        recommended_action: row.recommended_action || '',
        notes: '',
        risk_priority: row.risk_priority || 0,
        hazard_level: row.hazard_level || '',
        alpha: 0,
        beta: 0,
        lambdaP: 0,
        time: 0,
        failureHazard: 0
      })
    }
  } catch (error) {
    console.error('获取分析结果失败', error)
    // 初始化分析表单
    Object.assign(analyzeForm, {
      severity: severityLevel || row.severity || '',
      severity_value: 1,
      occurrence_probability: 1,
      detection_probability: 1,
      recommended_action: row.recommended_action || '',
      notes: '',
      risk_priority: row.risk_priority || 0,
      hazard_level: row.hazard_level || '',
      alpha: 0,
      beta: 0,
      lambdaP: 0,
      time: 0,
      failureHazard: 0
    })
  }
  
  analyzeDialogVisible.value = true
}

// 计算风险优先级数（RPN）
const calculateRPN = () => {
  // 转换为数值
  const severityValue = getSeverityValue(analyzeForm.severity)
  const occurrenceValue = getOccurrenceValue(analyzeForm.occurrence)
  const detectionValue = getDetectionValue(analyzeForm.detection)
  
  // 计算RPN
  const rpn = severityValue * occurrenceValue * detectionValue
  analyzeForm.risk_priority = rpn
  
  // 确定危害等级
  analyzeForm.hazard_level = getHazardLevel(rpn)
  
  ElMessage.success('危害度计算完成')
}

// 计算故障模式危害度（Cmj）
const calculateCmj = () => {
  const { alpha, beta, lambdaP, time } = analyzeForm
  
  // 验证输入
  if (!alpha || !beta || !lambdaP || !time) {
    ElMessage.error('请填写完整的危害度计算参数')
    return
  }
  
  // 计算Cmj = αj × βj × λp × t
  // λp的单位是10⁻⁶/h，所以结果需要乘以10⁻³来转换为10⁻³的单位
  const cmj = alpha * beta * lambdaP * time * 1e-3
  analyzeForm.failureHazard = cmj
  
  ElMessage.success('故障模式危害度计算完成')
}

// 计算产品危害度（Cr）
const calculateCr = () => {
  // 计算所有故障模式危害度的总和
  const cr = tableData.value.reduce((sum, item) => {
    return sum + (item.failureHazard || 0)
  }, 0)
  
  productHazard.value = cr
  
  ElMessage.success('产品危害度计算完成')
}

// 获取严酷度数值
const getSeverityValue = (severity) => {
  const severityMap = {
    'Ⅰ': 10,
    'Ⅱ': 7,
    'Ⅲ': 4,
    'Ⅳ': 1,
    'I类': 10,
    'II类': 7,
    'III类': 4,
    'I': 10,
    'II': 7,
    'III': 4
  }
  return severityMap[severity] || 1
}

// 获取发生概率数值
const getOccurrenceValue = (occurrence) => {
  const occurrenceMap = {
    'A': 10,
    'B': 7,
    'C': 4,
    'D': 2,
    'E': 1
  }
  return occurrenceMap[occurrence] || 1
}

// 获取检测难度数值
const getDetectionValue = (detection) => {
  const detectionMap = {
    '1': 10,
    '2': 7,
    '3': 4,
    '4': 2,
    '5': 1
  }
  return detectionMap[detection] || 1
}

// 根据RPN值获取危害等级
const getHazardLevel = (rpn) => {
  if (rpn >= 200) return '严重'
  if (rpn >= 150) return '高'
  if (rpn >= 100) return '中'
  return '低'
}

// 从本地存储获取分析结果
const getAnalysisResultsFromStorage = () => {
  try {
    const storedResults = localStorage.getItem('failureAnalysisResults')
    return storedResults ? JSON.parse(storedResults) : {}
  } catch (error) {
    console.log('从本地存储获取分析结果失败', error)
    return {}
  }
}

// 保存分析结果到本地存储
const saveAnalysisResultsToStorage = (results) => {
  try {
    localStorage.setItem('failureAnalysisResults', JSON.stringify(results))
  } catch (error) {
    console.log('保存分析结果到本地存储失败', error)
  }
}

// 保存分析结果
const saveAnalysisResult = async () => {
  try {
    // 构建分析结果数据
    const analysisData = {
      failure_mode: currentAnalyzeRow.value.id,
      severity_value: parseFloat(analyzeForm.severity_value) || 1,
      occurrence_probability: parseFloat(analyzeForm.occurrence_probability) || 1,
      detection_probability: parseFloat(analyzeForm.detection_probability) || 1,
      recommended_action: analyzeForm.recommended_action || '',
      notes: analyzeForm.notes || ''
    }
    
    console.log('准备保存的分析数据:', analysisData)
    console.log('数据类型检查:', {
      failure_mode: typeof analysisData.failure_mode,
      severity_value: typeof analysisData.severity_value,
      occurrence_probability: typeof analysisData.occurrence_probability,
      detection_probability: typeof analysisData.detection_probability,
      recommended_action: typeof analysisData.recommended_action,
      notes: typeof analysisData.notes
    })
    
    // 先检查是否已存在该故障模式的分析记录
    const existingAnalyses = await failureAnalysisApi.getAnalyses({ failure_mode: currentAnalyzeRow.value.id })
    
    let response
    if (existingAnalyses.results && existingAnalyses.results.length > 0) {
      // 如果已存在，则更新
      const existingId = existingAnalyses.results[0].id
      console.log('更新现有分析记录，ID:', existingId)
      response = await failureAnalysisApi.updateAnalysis(existingId, analysisData)
    } else {
      // 如果不存在，则创建
      console.log('创建新的分析记录')
      response = await failureAnalysisApi.createAnalysis(analysisData)
    }
    
    console.log('保存成功，返回数据:', response)
    
    ElMessage.success('分析结果保存成功')
    analyzeDialogVisible.value = false
    
    // 更新表格数据
    const index = tableData.value.findIndex(item => item.failure_mode === currentAnalyzeRow.value.failure_mode)
    if (index !== -1) {
      tableData.value[index] = {
        ...tableData.value[index],
        severity: analyzeForm.severity,
        recommended_action: analyzeForm.recommended_action,
        risk_priority: response.risk_priority_number,
        hazard_level: response.risk_level
      }
    }
    
    // 重新加载数据
    await loadData()
  } catch (error) {
    console.error('保存分析结果失败', error)
    console.error('错误详情:', error.response?.data || error.message)
    console.error('完整错误对象:', error)
    const errorMessage = error.response?.data?.detail || error.response?.data?.error || '保存分析结果失败'
    ElMessage.error(errorMessage)
  }
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
  pagination.page = 1
  loadData()
}

const handleCurrentChange = (val) => {
  pagination.page = val
  loadData()
}

// 危害度参数配置相关方法
const loadParameters = async () => {
  try {
    const response = await failureAnalysisApi.getParameters()
    console.log('API响应:', response)
    console.log('results:', response.results)
    parameters.value = response.results || []
    console.log('parameters.value:', parameters.value)
  } catch (error) {
    console.log('加载危害度参数失败，使用默认数据', error)
    // 使用默认参数数据
    parameters.value = [
      {
        id: 1,
        name: '严重度系数αj',
        parameter_type: 'severity',
        description: '故障模式的严重度系数',
        min_value: 0,
        max_value: 10,
        default_value: 1,
        unit: '',
        is_active: true
      },
      {
        id: 2,
        name: '发生概率系数βj',
        parameter_type: 'occurrence',
        description: '故障模式的发生概率系数',
        min_value: 0,
        max_value: 10,
        default_value: 1,
        unit: '',
        is_active: true
      },
      {
        id: 3,
        name: '故障率λp',
        parameter_type: 'risk',
        description: '设备的故障率，单位为10⁻⁶/h',
        min_value: 0,
        max_value: 1000,
        default_value: 100,
        unit: '×10⁻⁶/h',
        is_active: true
      },
      {
        id: 4,
        name: '运行时间t',
        parameter_type: 'risk',
        description: '设备的运行时间，单位为小时',
        min_value: 0,
        max_value: 10000,
        default_value: 1000,
        unit: 'h',
        is_active: true
      }
    ]
    console.log('使用默认参数:', parameters.value)
  }
}

const openParameterForm = (row = null) => {
  if (row) {
    // 编辑模式
    isEditParameter.value = true
    currentParameterId.value = row.id
    Object.assign(parameterForm, row)
  } else {
    // 新增模式
    isEditParameter.value = false
    currentParameterId.value = null
    Object.assign(parameterForm, {
      name: '',
      parameter_type: '',
      description: '',
      min_value: 0,
      max_value: 10,
      default_value: 1,
      unit: '',
      is_active: true
    })
  }
  parameterDialogVisible.value = true
};

const submitParameterForm = async () => {
  if (!parameterFormRef.value) return
  
  try {
    await parameterFormRef.value.validate()
    
    if (isEditParameter.value) {
      // 更新参数
      await failureAnalysisApi.updateParameter(currentParameterId.value, parameterForm)
      ElMessage.success('参数更新成功')
    } else {
      // 创建参数
      await failureAnalysisApi.createParameter(parameterForm)
      ElMessage.success('参数创建成功')
    }
    
    parameterDialogVisible.value = false
    loadParameters()
  } catch (error) {
    if (error.name === 'Error') {
      ElMessage.error('操作失败：' + error.message)
    }
  }
}

const deleteParameter = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除参数 ${row.name} 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await failureAnalysisApi.deleteParameter(row.id)
    ElMessage.success('参数删除成功')
    loadParameters()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 危害度排序相关方法
const handleSortChange = () => {
  ElMessage.success(`已按${getSortByName(sortBy.value)}排序`)
}

// 获取排序名称
const getSortByName = (sortBy) => {
  const sortMap = {
    'risk_priority': '风险优先级数',
    'severity': '严酷度',
    'hazard_level': '危害等级',
    'failure_hazard': '故障模式危害度'
  }
  return sortMap[sortBy] || sortBy
}

const exportRankingData = () => {
  const headers = ['排名', '设备类型', '项目实例名称', '故障模式', '风险优先级数', '严酷度等级', '危害等级', '故障模式危害度']
  const rows = sortedData.value.map((item, index) => [
    index + 1,
    getEquipmentTypeName(item.equipment_type),
    item.project_instance_name,
    item.failure_mode,
    item.risk_priority,
    item.severity,
    item.hazard_level,
    (item.failureHazard || 0).toFixed(4)
  ])
  
  let csvContent = headers.join(',') + '\n'
  rows.forEach(row => {
    csvContent += row.join(',') + '\n'
  })
  
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', '危害度排序数据.csv')
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  ElMessage.success('导出成功')
}

// 计算属性：排序后的数据
const sortedData = computed(() => {
  return [...tableData.value].sort((a, b) => {
    if (sortBy.value === 'risk_priority') {
      const aRpn = Number(a.risk_priority) || 0
      const bRpn = Number(b.risk_priority) || 0
      return bRpn - aRpn
    } else if (sortBy.value === 'severity') {
      const severityOrder = { 'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'I类': 1, 'II类': 2, 'III类': 3, 'I': 1, 'II': 2, 'III': 3 }
      const aSeverity = severityOrder[a.severity] || 999
      const bSeverity = severityOrder[b.severity] || 999
      return aSeverity - bSeverity
    } else if (sortBy.value === 'hazard_level') {
      const hazardOrder = { '严重': 1, '高': 2, '中': 3, '低': 4 }
      const aHazard = hazardOrder[a.hazard_level] || 999
      const bHazard = hazardOrder[b.hazard_level] || 999
      return aHazard - bHazard
    } else if (sortBy.value === 'failure_hazard') {
      const aHazard = Number(a.failureHazard) || 0
      const bHazard = Number(b.failureHazard) || 0
      return bHazard - aHazard
    }
    return 0
  })
})

// 危害度可视化相关方法
const initCharts = () => {
  initHazardLevelChart()
  initSeverityChart()
  initRiskPriorityChart()
  initRiskMatrixChart()
  initFailureHazardChart()
  initProductHazardChart()
}

const updateVisualization = () => {
  refreshCharts()
}

const refreshCharts = () => {
  initCharts()
  ElMessage.success('图表已刷新')
}

const exportCharts = () => {
  const charts = [
    { ref: hazardLevelChart, name: '危害等级分布' },
    { ref: severityChart, name: '严酷度等级分布' },
    { ref: riskPriorityChart, name: '风险优先级分布' },
    { ref: riskMatrixChart, name: '风险矩阵分析' },
    { ref: failureHazardChart, name: '故障模式危害度对比' },
    { ref: productHazardChart, name: '产品危害度分析' }
  ]
  
  charts.forEach((chart, index) => {
    setTimeout(() => {
      if (chart.ref.value) {
        const instance = echarts.getInstanceByDom(chart.ref.value)
        if (instance) {
          const url = instance.getDataURL({
            type: 'png',
            pixelRatio: 2,
            backgroundColor: '#fff'
          })
          const link = document.createElement('a')
          link.download = `${chart.name}.png`
          link.href = url
          link.click()
        }
      }
    }, index * 500)
  })
  
  ElMessage.success('图表导出中...')
}

const initHazardLevelChart = () => {
  if (!hazardLevelChart.value) return
  
  const chart = echarts.init(hazardLevelChart.value)
  
  const filteredData = visualizationFilter.equipmentType 
    ? tableData.value.filter(item => item.equipment_type === visualizationFilter.equipmentType)
    : tableData.value
  
  const hazardLevelData = filteredData.reduce((acc, item) => {
    const level = item.hazard_level || '未分类'
    acc[level] = (acc[level] || 0) + 1
    return acc
  }, {})
  
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

const initSeverityChart = () => {
  if (!severityChart.value) return
  
  const chart = echarts.init(severityChart.value)
  
  const filteredData = visualizationFilter.equipmentType 
    ? tableData.value.filter(item => item.equipment_type === visualizationFilter.equipmentType)
    : tableData.value
  
  const severityData = filteredData.reduce((acc, item) => {
    const severity = item.severity || '未分类'
    acc[severity] = (acc[severity] || 0) + 1
    return acc
  }, {})
  
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
        name: '严酷度等级',
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
        data: Object.entries(severityData).map(([name, value]) => ({
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

const initRiskPriorityChart = () => {
  if (!riskPriorityChart.value) return
  
  const chart = echarts.init(riskPriorityChart.value)
  
  const filteredData = visualizationFilter.equipmentType 
    ? tableData.value.filter(item => item.equipment_type === visualizationFilter.equipmentType)
    : tableData.value
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['风险优先级数', '故障模式危害度'],
      top: '5%',
      left: 'center'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: filteredData.map(item => item.failure_mode)
    },
    yAxis: {
      type: 'value',
      name: '数值'
    },
    series: [
      {
        name: '风险优先级数',
        type: 'bar',
        data: filteredData.map(item => item.risk_priority),
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value > 200) return '#f56c6c'
            if (value > 150) return '#e6a23c'
            if (value > 100) return '#409eff'
            return '#67c23a'
          }
        }
      },
      {
        name: '故障模式危害度',
        type: 'bar',
        data: filteredData.map(item => item.failureHazard),
        itemStyle: {
          color: '#909399'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const initRiskMatrixChart = () => {
  if (!riskMatrixChart.value) return
  
  const chart = echarts.init(riskMatrixChart.value)
  
  const option = {
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: ['几乎不可能', '很少发生', '偶尔发生', '经常发生', '频繁发生'],
      splitArea: {
        show: true
      }
    },
    yAxis: {
      type: 'category',
      data: ['轻微伤害', '轻度伤害', '中度伤害', '严重伤害', '致命伤害'],
      splitArea: {
        show: true
      }
    },
    visualMap: {
      min: 0,
      max: 100,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#67c23a', '#409eff', '#e6a23c', '#f56c6c']
      }
    },
    series: [
      {
        name: '风险等级',
        type: 'heatmap',
        data: [
          [0, 0, 10],
          [0, 1, 20],
          [0, 2, 30],
          [0, 3, 40],
          [0, 4, 50],
          [1, 0, 20],
          [1, 1, 30],
          [1, 2, 40],
          [1, 3, 50],
          [1, 4, 60],
          [2, 0, 30],
          [2, 1, 40],
          [2, 2, 50],
          [2, 3, 60],
          [2, 4, 70],
          [3, 0, 40],
          [3, 1, 50],
          [3, 2, 60],
          [3, 3, 70],
          [3, 4, 80],
          [4, 0, 50],
          [4, 1, 60],
          [4, 2, 70],
          [4, 3, 80],
          [4, 4, 90]
        ],
        label: {
          show: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
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

const initFailureHazardChart = () => {
  if (!failureHazardChart.value) return
  
  const chart = echarts.init(failureHazardChart.value)
  
  const filteredData = visualizationFilter.equipmentType 
    ? tableData.value.filter(item => item.equipment_type === visualizationFilter.equipmentType)
    : tableData.value
  
  const sortedByHazard = [...filteredData].sort((a, b) => {
    return (b.failureHazard || 0) - (a.failureHazard || 0)
  })
  
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
      data: sortedByHazard.map(item => item.failure_mode),
      axisLabel: {
        rotate: 45,
        interval: 0
      }
    },
    yAxis: {
      type: 'value',
      name: '危害度值 (×10⁻³)'
    },
    series: [
      {
        name: '故障模式危害度',
        type: 'bar',
        data: sortedByHazard.map(item => item.failureHazard || 0),
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value > 0.5) return '#f56c6c'
            if (value > 0.3) return '#e6a23c'
            if (value > 0.1) return '#409eff'
            return '#67c23a'
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const initProductHazardChart = () => {
  if (!productHazardChart.value) return
  
  const chart = echarts.init(productHazardChart.value)
  
  const filteredData = visualizationFilter.equipmentType 
    ? tableData.value.filter(item => item.equipment_type === visualizationFilter.equipmentType)
    : tableData.value
  
  const cr = filteredData.reduce((sum, item) => {
    return sum + (item.failureHazard || 0)
  }, 0)
  
  productHazard.value = cr
  
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
      data: ['产品危害度Cr']
    },
    yAxis: {
      type: 'value',
      name: '危害度值 (×10⁻³)'
    },
    series: [
      {
        name: '产品危害度Cr',
        type: 'bar',
        data: [cr],
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value > 50) return '#f56c6c'
            if (value > 20) return '#e6a23c'
            if (value > 10) return '#409eff'
            return '#67c23a'
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
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
    console.log('加载设备类型列表失败，使用默认设备类型', error)
    // 使用默认设备类型
    equipmentTypes.value = [
      {
        id: 1,
        name: '电梯'
      },
      {
        id: 2,
        name: '空调系统'
      },
      {
        id: 3,
        name: '防冰管嘴、支架焊缝裂纹、空气泄露'
      }
    ]
  }
}

// 加载严酷度评定数据
const loadSeverityAssessments = async () => {
  try {
    const response = await severityApi.getSeverityAssessments({ page_size: 1000 })
    severityAssessments.value = response.results || []
  } catch (error) {
    console.log('加载严酷度评定数据失败', error)
    severityAssessments.value = []
  }
}

// 根据设备类型ID获取设备类型名称
const getEquipmentTypeName = (equipmentTypeId) => {
  if (!equipmentTypeId) return ''
  
  const equipmentType = equipmentTypes.value.find(type => type.id === equipmentTypeId)
  return equipmentType ? equipmentType.name : equipmentTypeId
}

const loadData = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: filterForm.failureMode
    }
    
    // 添加设备类型过滤器
    if (filterForm.equipmentType) {
      params.equipment_type = filterForm.equipmentType
    }
    
    const response = await failureApi.getFailureModes(params)
    const failureModes = response.results || []
    
    // 从后端API获取所有已保存的分析结果
    const analysesResponse = await failureAnalysisApi.getAnalyses({ page_size: 1000 })
    const hazardAnalyses = analysesResponse.results || []
    
    // 创建故障模式ID到分析结果的映射
    const analysisMap = {}
    hazardAnalyses.forEach(analysis => {
      if (analysis.failure_mode) {
        analysisMap[analysis.failure_mode] = analysis
      }
    })
    
    // 转换故障模式数据为表格数据格式
    tableData.value = failureModes.map(mode => {
      const failureModeName = mode.name || ''
      const hazardAnalysis = analysisMap[mode.id]
      
      // 从严酷度评定数据中查找对应的严酷度等级
      let severityLevel = ''
      if (failureModeName) {
        const assessment = severityAssessments.value.find(item => {
          return item.failure_mode_name === failureModeName || 
                 item.failure_mode === failureModeName ||
                 (typeof item.failure_mode === 'object' && item.failure_mode.name === failureModeName)
        })
        if (assessment) {
          severityLevel = assessment.severity_level?.level || assessment.severity_level_code || assessment.severity_level || ''
        }
      }
      
      return {
        id: mode.id,
        equipment_type: mode.equipment_type || '',
        project_instance_name: mode.code || '',
        failure_mode: failureModeName,
        severity: hazardAnalysis?.severity_level_name || severityLevel || convertSeverityToRoman(mode.severity) || '',
        occurrence: hazardAnalysis?.occurrence_probability || mode.occurrence || '',
        detection: hazardAnalysis?.detection_probability || mode.detection || '',
        risk_priority: hazardAnalysis?.risk_priority_number || mode.risk_priority || 0,
        hazard_level: hazardAnalysis?.risk_level || mode.hazard_level || '',
        recommended_action: hazardAnalysis?.recommended_action || mode.recommended_action || '',
        failure_cause: mode.causes || '',
        impact_analysis: mode.description || '',
        alpha: hazardAnalysis?.alpha || mode.alpha || 0,
        beta: hazardAnalysis?.beta || mode.beta || 0,
        lambdaP: hazardAnalysis?.lambdaP || mode.lambdaP || 0,
        time: hazardAnalysis?.time || mode.time || 0,
        failureHazard: hazardAnalysis?.failureHazard || mode.failureHazard || 0
      }
    })
    
    pagination.total = response.count || 0
  } catch (error) {
    console.log('加载故障模式数据失败', error)
    // 显示更友好的错误信息
    ElMessage.warning('加载故障模式数据失败，使用本地数据')
    
    // 从本地存储获取已保存的分析结果
    const analysisResults = getAnalysisResultsFromStorage()
    
    // 使用本地默认数据
    tableData.value = [
      {
        id:1,
        equipment_type: 2,
        project_instance_name: '热边进口封头组件',
        failure_mode: '防冰管嘴、支架焊缝裂纹、空气泄露',
        severity: 'Ⅲ',
        occurrence: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.occurrence || '',
        detection: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.detection || '',
        risk_priority: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.risk_priority || 1,
        hazard_level: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.hazard_level || '',
        recommended_action: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.recommended_action || '',
        failure_cause: '',
        impact_analysis: '',
        alpha: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.alpha || 0,
        beta: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.beta || 0,
        lambdaP: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.lambdaP || 0,
        time: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.time || 0,
        failureHazard: analysisResults['防冰管嘴、支架焊缝裂纹、空气泄露']?.failureHazard || 0
      },
      {
        id: 2,
        equipment_type: 2,
        project_instance_name: '热边出口封头组件',
        failure_mode: '焊缝裂纹、空气泄露',
        severity: 'Ⅲ',
        occurrence: analysisResults['焊缝裂纹、空气泄露']?.occurrence || '',
        detection: analysisResults['焊缝裂纹、空气泄露']?.detection || '',
        risk_priority: analysisResults['焊缝裂纹、空气泄露']?.risk_priority || 0,
        hazard_level: analysisResults['焊缝裂纹、空气泄露']?.hazard_level || '',
        recommended_action: analysisResults['焊缝裂纹、空气泄露']?.recommended_action || '',
        failure_cause: '',
        impact_analysis: '',
        alpha: analysisResults['焊缝裂纹、空气泄露']?.alpha || 0,
        beta: analysisResults['焊缝裂纹、空气泄露']?.beta || 0,
        lambdaP: analysisResults['焊缝裂纹、空气泄露']?.lambdaP || 0,
        time: analysisResults['焊缝裂纹、空气泄露']?.time || 0,
        failureHazard: analysisResults['焊缝裂纹、空气泄露']?.failureHazard || 0
      },
      {
        id: 3,
        equipment_type: 1,
        project_instance_name: '曳引机',
        failure_mode: '曳引轮过度磨损',
        severity: 'Ⅲ',
        occurrence: analysisResults['曳引轮过度磨损']?.occurrence || '',
        detection: analysisResults['曳引轮过度磨损']?.detection || '',
        risk_priority: analysisResults['曳引轮过度磨损']?.risk_priority || 0,
        hazard_level: analysisResults['曳引轮过度磨损']?.hazard_level || '',
        recommended_action: analysisResults['曳引轮过度磨损']?.recommended_action || '',
        failure_cause: '',
        impact_analysis: '',
        alpha: analysisResults['曳引轮过度磨损']?.alpha || 0,
        beta: analysisResults['曳引轮过度磨损']?.beta || 0,
        lambdaP: analysisResults['曳引轮过度磨损']?.lambdaP || 0,
        time: analysisResults['曳引轮过度磨损']?.time || 0,
        failureHazard: analysisResults['曳引轮过度磨损']?.failureHazard || 0
      },
      {
        id: 4,
        equipment_type: 1,
        project_instance_name: '曳引机',
        failure_mode: '制动力矩过小',
        severity: 'Ⅱ',
        occurrence: analysisResults['制动力矩过小']?.occurrence || '',
        detection: analysisResults['制动力矩过小']?.detection || '',
        risk_priority: analysisResults['制动力矩过小']?.risk_priority || 0,
        hazard_level: analysisResults['制动力矩过小']?.hazard_level || '',
        recommended_action: analysisResults['制动力矩过小']?.recommended_action || '',
        failure_cause: '',
        impact_analysis: '',
        alpha: analysisResults['制动力矩过小']?.alpha || 0,
        beta: analysisResults['制动力矩过小']?.beta || 0,
        lambdaP: analysisResults['制动力矩过小']?.lambdaP || 0,
        time: analysisResults['制动力矩过小']?.time || 0,
        failureHazard: analysisResults['制动力矩过小']?.failureHazard || 0
      },
      {
        id: 5,
        equipment_type: 1,
        project_instance_name: '曳引机',
        failure_mode: '制动延时',
        severity: 'Ⅲ',
        occurrence: analysisResults['制动延时']?.occurrence || '',
        detection: analysisResults['制动延时']?.detection || '',
        risk_priority: analysisResults['制动延时']?.risk_priority || 0,
        hazard_level: analysisResults['制动延时']?.hazard_level || '',
        recommended_action: analysisResults['制动延时']?.recommended_action || '',
        failure_cause: '',
        impact_analysis: '',
        alpha: analysisResults['制动延时']?.alpha || 0,
        beta: analysisResults['制动延时']?.beta || 0,
        lambdaP: analysisResults['制动延时']?.lambdaP || 0,
        time: analysisResults['制动延时']?.time || 0,
        failureHazard: analysisResults['制动延时']?.failureHazard || 0
      }
    ]
    
    pagination.total = tableData.value.length
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadEquipmentTypes()
  loadParameters()
  loadSeverityAssessments()
  loadData()
  
  // 延迟初始化图表，确保DOM已渲染
  setTimeout(() => {
    initCharts()
  }, 100)
})

// 监听标签页切换，重新初始化图表
const handleTabChange = (tab) => {
  const tabName = tab.props.name
  activeTab.value = tabName
  if (tabName === 'visualization') {
    setTimeout(() => {
      initCharts()
    }, 300)
  }
};
</script>

<style scoped>
.failure-mode-analysis {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
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
