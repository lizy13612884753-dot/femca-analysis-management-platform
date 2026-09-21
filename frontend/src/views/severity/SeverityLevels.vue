<template>
  <div class="severity-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>严酷度管理</h1>
      <p>全面管理故障模式的严重程度评估体系</p>
    </div>

    <!-- 标签页导航 -->
    <el-tabs v-model="activeTab" type="border-card" class="severity-tabs">
      <!-- 严酷度评定 -->
      <el-tab-pane label="严酷度评定" name="severity-assessment">
        <div class="tab-content">
          <!-- 评定操作栏 -->
          <div class="toolbar">
            <div class="toolbar-left">
              <el-button type="primary" @click="openAssessmentForm('create')">
                <el-icon><Plus /></el-icon>
                新增评定
              </el-button>
            </div>
            <div class="toolbar-right">
              <el-input
                v-model="searchQuery"
                placeholder="搜索故障模式..."
                style="width: 300px"
                clearable
                @clear="handleSearch"
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </div>

          <!-- 评定表格 -->
          <el-card class="table-card" shadow="never">
            <el-table
              :data="assessmentModule.data"
              style="width: 100%"
              v-loading="assessmentModule.loading"
              row-key="id"
              stripe
            >
              <el-table-column label="ID" width="80">
                <template #default="{ $index }">
                  {{ $index + 1 }}
                </template>
              </el-table-column>
              <el-table-column label="故障模式" width="200">
                <template #default="{ row }">
                  {{ row.failure_mode_name || row.failure_mode?.name || row.failure_mode }}
                </template>
              </el-table-column>
              <el-table-column prop="severity_level_code" label="严酷度等级" width="120">
                <template #default="{ row }">
                  <el-tag :type="getLevelTypeColor(row.severity_level_code)">
                    {{ row.severity_level_code }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="severity_value" label="严酷度S" width="100" />
              <el-table-column prop="occurrence_value" label="发生度O" width="100" />
              <el-table-column prop="detection_value" label="检测度D" width="100" />
              <el-table-column prop="rpn_value" label="RPN值" width="100">
                <template #default="{ row }">
                  <el-tag :type="getRpnTypeColor(row.rpn_value)">
                    {{ row.rpn_value }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="project_instance_name" label="项目实例名称" min-width="200" />
              <el-table-column prop="assessor" label="评定人" width="120" />
              <el-table-column prop="assessment_time" label="评定时间" width="180" />
              <el-table-column label="操作" width="160" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" type="primary" @click="openAssessmentForm('edit', row)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteAssessment(row)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="assessmentModule.pagination.page"
                v-model:page-size="assessmentModule.pagination.pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="assessmentModule.pagination.total"
                @size-change="handleAssessmentSizeChange"
                @current-change="handleAssessmentCurrentChange"
              />
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <!-- 严酷度统计 -->
      <el-tab-pane label="统计分析" name="statistics">
        <div class="tab-content">
          <h3 class="section-title">严酷度等级分布统计</h3>

          <!-- 统计概览卡片 -->
          <div class="stats-overview">
            <el-card class="stat-card" shadow="never">
              <div class="stat-content">
                <div class="stat-icon">
                  <el-icon class="icon-large"><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-label">总评定记录</div>
                  <div class="stat-value">{{ statsModule.totalAssessments }}</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card" shadow="never">
              <div class="stat-content">
                <div class="stat-icon">
                  <el-icon class="icon-large"><DataAnalysis /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-label">平均RPN值</div>
                  <div class="stat-value">{{ statsModule.averageRpn.toFixed(2) }}</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card" shadow="never">
              <div class="stat-content">
                <div class="stat-icon danger">
                  <el-icon class="icon-large"><WarningFilled /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-label">高风险数量</div>
                  <div class="stat-value">{{ statsModule.highRiskCount }}</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card" shadow="never">
              <div class="stat-content">
                <div class="stat-icon warning">
                  <el-icon class="icon-large"><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-label">中风险数量</div>
                  <div class="stat-value">{{ statsModule.mediumRiskCount }}</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card" shadow="never">
              <div class="stat-content">
                <div class="stat-icon success">
                  <el-icon class="icon-large"><CircleCheck /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-label">低风险数量</div>
                  <div class="stat-value">{{ statsModule.lowRiskCount }}</div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- 等级分布表格 -->
          <el-card class="table-card" shadow="never">
            <h4 class="table-title">严酷度等级分布</h4>
            <el-table
              :data="statsModule.levelDistribution"
              style="width: 100%"
              stripe
            >
              <el-table-column prop="level" label="等级" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.color">
                    {{ row.level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="levelName" label="等级名称" width="150" />
              <el-table-column prop="count" label="数量" width="100" />
              <el-table-column prop="percentage" label="占比" width="120">
                <template #default="{ row }">
                  {{ row.percentage.toFixed(2) }}%
                </template>
              </el-table-column>
              <el-table-column prop="description" label="等级描述" min-width="200" />
            </el-table>
          </el-card>

          <!-- RPN分布表格 -->
          <el-card class="table-card" shadow="never">
            <h4 class="table-title">RPN值分布</h4>
            <el-table
              :data="statsModule.rpnDistribution"
              style="width: 100%"
              stripe
            >
              <el-table-column prop="range" label="RPN范围" width="150">
                <template #default="{ row }">
                  <el-tag :type="row.color">
                    {{ row.range }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="count" label="数量" width="100" />
              <el-table-column prop="percentage" label="占比" width="120">
                <template #default="{ row }">
                  {{ row.percentage.toFixed(2) }}%
                </template>
              </el-table-column>
              <el-table-column prop="riskLevel" label="风险等级" width="120" />
            </el-table>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 评定对话框 -->
    <el-dialog
      v-model="assessmentModule.dialogVisible"
      :title="assessmentModule.dialogTitle"
      width="700px"
      destroy-on-close
    >
      <el-form :model="assessmentModule.form" :rules="assessmentModule.rules" ref="assessmentFormRef" label-width="120px">
        <el-form-item label="故障模式" prop="failure_mode">
          <el-select 
            v-model="assessmentModule.form.failure_mode" 
            placeholder="请选择或搜索故障模式" 
            style="width: 100%"
            :loading="loadingFailureModes"
            filterable
            default-first-option
          >
            <el-option 
              v-for="mode in failureModeList" 
              :key="mode.id" 
              :label="mode.name" 
              :value="mode.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="严酷度S" prop="severity_value">
          <el-select v-model="assessmentModule.form.severity_value" placeholder="请选择严酷度值">
            <el-option v-for="i in 10" :key="i" :label="`${i} - ${getSeverityDescription(i)}`" :value="i" />
          </el-select>
        </el-form-item>
        <el-form-item label="发生度O" prop="occurrence_value">
          <el-select v-model="assessmentModule.form.occurrence_value" placeholder="请选择发生度值">
            <el-option v-for="i in 10" :key="i" :label="`${i} - ${getOccurrenceDescription(i)}`" :value="i" />
          </el-select>
        </el-form-item>
        <el-form-item label="检测度D" prop="detection_value">
          <el-select v-model="assessmentModule.form.detection_value" placeholder="请选择检测度值">
            <el-option v-for="i in 10" :key="i" :label="`${i} - ${getDetectionDescription(i)}`" :value="i" />
          </el-select>
        </el-form-item>
        <el-form-item label="RPN值" prop="rpn_value">
          <el-input v-model="assessmentModule.form.rpn_value" readonly />
        </el-form-item>
        <el-form-item label="项目实例名称" prop="project_instance_name" required>
          <el-input v-model="assessmentModule.form.project_instance_name" placeholder="请输入项目实例名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeAssessmentForm">取消</el-button>
          <el-button type="primary" @click="submitAssessmentForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Edit, Delete, Document, DataAnalysis, WarningFilled,
  Warning, CircleCheck
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import * as severityApi from '../../api/severity/index'
import * as failureApi from '../../api/failure/index'

// 当前激活的标签页
const activeTab = ref('severity-assessment')

// 搜索查询
const searchQuery = ref('')

// 故障模式列表
const failureModeList = ref([])
const loadingFailureModes = ref(false)

// 严酷度等级列表
const severityLevelList = ref([])
const loadingSeverityLevels = ref(false)

// 加载故障模式数据
const loadFailureModes = async () => {
  console.log('开始加载故障模式数据...')
  loadingFailureModes.value = true
  try {
    // 获取所有故障模式（不分页）
    const response = await failureApi.getFailureModes({ page_size: 1000 })
    console.log('故障模式API响应:', response)
    if (response && response.results) {
      console.log('获取到的故障模式:', response.results)
      failureModeList.value = response.results
    } else {
      console.log('未获取到故障模式数据，使用空数组')
      // 使用空数组，不显示模拟数据
      failureModeList.value = []
    }
  } catch (error) {
    console.error('加载故障模式失败:', error)
    console.log('API调用失败，使用空数组')
    ElMessage.error('加载故障模式失败')
    // 使用空数组，不显示模拟数据
    failureModeList.value = []
  } finally {
    console.log('故障模式加载完成，当前列表:', failureModeList.value)
    loadingFailureModes.value = false
  }
}

// 加载严酷度等级数据
const loadSeverityLevels = async () => {
  console.log('开始加载严酷度等级数据...')
  loadingSeverityLevels.value = true
  try {
    // 获取所有严酷度等级（不分页）
    const response = await severityApi.getSeverityLevels({ page_size: 1000 })
    console.log('严酷度等级API响应:', response)
    if (response && response.results) {
      console.log('获取到的严酷度等级:', response.results)
      severityLevelList.value = response.results
    } else {
      console.log('未获取到严酷度等级数据，使用空数组')
      // 使用空数组，不显示模拟数据
      severityLevelList.value = []
    }
  } catch (error) {
    console.error('加载严酷度等级失败:', error)
    console.log('API调用失败，使用空数组')
    ElMessage.error('加载严酷度等级失败')
    // 使用空数组，不显示模拟数据
    severityLevelList.value = []
  } finally {
    console.log('严酷度等级加载完成，当前列表:', severityLevelList.value)
    loadingSeverityLevels.value = false
  }
}

// RPN配置模块（简化版，保留必要的配置项）
const rpnConfigModule = reactive({
  form: {
    high_risk_threshold: 100,
    medium_risk_threshold: 50
  }
})

// 严酷度评定模块
const assessmentFormRef = ref(null)
const assessmentModule = reactive({
  data: [],
  loading: false,
  dialogVisible: false,
  dialogTitle: '新增评定',
  isEditing: false,
  currentId: null,
  pagination: {
    page: 1,
    pageSize: 10,
    total: 0
  },
  form: {
    id: null,
    failure_mode: '',
    severity_level: 'Ⅲ',
    severity_value: null,
    occurrence_value: null,
    detection_value: null,
    rpn_value: null,
    score: 50.0,
    project_instance_name: '',
    is_active: true
  },
  rules: {
    failure_mode: [{ required: true, message: '请选择故障模式', trigger: 'change' }],
    severity_value: [{ required: true, message: '请选择严酷度值', trigger: 'change' }],
    occurrence_value: [{ required: true, message: '请选择发生度值', trigger: 'change' }],
    detection_value: [{ required: true, message: '请选择检测度值', trigger: 'change' }],
    project_instance_name: [{ required: true, message: '请输入项目实例名称', trigger: 'blur' }]
  }
})

// 统计分析模块
const statsModule = reactive({
  totalAssessments: computed(() => assessmentModule.data.length),
  averageRpn: computed(() => {
    if (assessmentModule.data.length === 0) return 0
    const sum = assessmentModule.data.reduce((acc, item) => acc + (item.rpn_value || 0), 0)
    return sum / assessmentModule.data.length
  }),
  highRiskCount: computed(() => {
    return assessmentModule.data.filter(item => item.rpn_value > rpnConfigModule.form.high_risk_threshold).length
  }),
  mediumRiskCount: computed(() => {
    return assessmentModule.data.filter(item => 
      item.rpn_value > rpnConfigModule.form.medium_risk_threshold && 
      item.rpn_value <= rpnConfigModule.form.high_risk_threshold
    ).length
  }),
  lowRiskCount: computed(() => {
    return assessmentModule.data.filter(item => item.rpn_value <= rpnConfigModule.form.medium_risk_threshold).length
  }),
  levelDistribution: computed(() => {
    const levelMap = {
      'Ⅰ': { count: 0, levelName: '灾难性', description: '导致人员伤亡或系统完全失效' },
      'Ⅱ': { count: 0, levelName: '严重', description: '导致系统性能严重下降，影响安全' },
      'Ⅲ': { count: 0, levelName: '中等', description: '导致系统性能下降，但不影响安全' },
      'Ⅳ': { count: 0, levelName: '轻微', description: '对系统性能影响很小' }
    }

    // 统计各等级数量
    assessmentModule.data.forEach(item => {
      const levelCode = item.severity_level_code || item.severity_level?.level || item.severity_level
      if (levelMap[levelCode]) {
        levelMap[levelCode].count++
      }
    })

    // 转换为数组格式
    return Object.keys(levelMap).map(level => ({
      level,
      levelName: levelMap[level].levelName,
      count: levelMap[level].count,
      percentage: statsModule.totalAssessments > 0 ? (levelMap[level].count / statsModule.totalAssessments) * 100 : 0,
      description: levelMap[level].description,
      color: getLevelTypeColor(level)
    }))
  }),
  rpnDistribution: computed(() => {
    const lowCount = statsModule.lowRiskCount
    const mediumCount = statsModule.mediumRiskCount
    const highCount = statsModule.highRiskCount

    return [
      {
        range: `1-${rpnConfigModule.form.medium_risk_threshold}`,
        count: lowCount,
        percentage: statsModule.totalAssessments > 0 ? (lowCount / statsModule.totalAssessments) * 100 : 0,
        riskLevel: '低风险',
        color: 'success'
      },
      {
        range: `${rpnConfigModule.form.medium_risk_threshold + 1}-${rpnConfigModule.form.high_risk_threshold}`,
        count: mediumCount,
        percentage: statsModule.totalAssessments > 0 ? (mediumCount / statsModule.totalAssessments) * 100 : 0,
        riskLevel: '中风险',
        color: 'warning'
      },
      {
        range: `${rpnConfigModule.form.high_risk_threshold + 1}+`,
        count: highCount,
        percentage: statsModule.totalAssessments > 0 ? (highCount / statsModule.totalAssessments) * 100 : 0,
        riskLevel: '高风险',
        color: 'danger'
      }
    ]
  })
})

// 监听S/O/D变化，自动计算RPN
watch(
  [() => assessmentModule.form.severity_value, () => assessmentModule.form.occurrence_value, () => assessmentModule.form.detection_value],
  ([s, o, d]) => {
    if (s && o && d) {
      assessmentModule.form.rpn_value = s * o * d
    } else {
      assessmentModule.form.rpn_value = null
    }
  },
  { immediate: true }
)

// 监听故障模式变化，自动填充项目实例名称
watch(
  () => assessmentModule.form.failure_mode,
  (failureModeId) => {
    if (failureModeId) {
      const failureMode = failureModeList.value.find(mode => mode.id === failureModeId)
      if (failureMode && failureMode.code) {
        assessmentModule.form.project_instance_name = failureMode.code
      }
    } else {
      assessmentModule.form.project_instance_name = ''
    }
  },
  { immediate: true }
)

// 加载评定数据
const loadAssessmentData = async () => {
  assessmentModule.loading = true
  try {
    const params = {
      page: assessmentModule.pagination.page,
      page_size: assessmentModule.pagination.pageSize,
      search: searchQuery.value
    }
    const response = await severityApi.getSeverityAssessments(params)
    console.log('API返回的数据:', response)
    if (response && response.results) {
      console.log('API返回的结果项:', response.results[0])
      assessmentModule.data = response.results.map(item => ({
        ...item,
        assessor: item.created_by?.username || 'admin',
        assessment_time: dayjs(item.created_at).format('YYYY-MM-DD HH:mm:ss'),
        project_instance_name: item.project_instance_name || item.failure_mode_code || ''
      }))
      assessmentModule.pagination.total = response.count
    } else {
      // 使用空数组，不显示模拟数据
      assessmentModule.data = []
      assessmentModule.pagination.total = 0
    }
  } catch (error) {
    console.error('加载评定数据失败:', error)
    ElMessage.error('加载评定数据失败')
    // 使用空数组，不显示模拟数据
    assessmentModule.data = []
    assessmentModule.pagination.total = 0
  } finally {
    assessmentModule.loading = false
  }
}

// 搜索处理
const handleSearch = () => {
  assessmentModule.pagination.page = 1
  loadAssessmentData()
}

// 打开评定表单
const openAssessmentForm = async (action, row = null) => {
  assessmentModule.isEditing = action === 'edit'
  assessmentModule.dialogTitle = action === 'edit' ? '编辑评定' : '新增评定'
  
  // 重新加载故障模式和严酷度等级数据，确保显示最新数据
  await Promise.all([loadFailureModes(), loadSeverityLevels()])
  
  assessmentModule.dialogVisible = true
  
  if (action === 'edit' && row) {
    // 在编辑时，直接使用后端返回的数据，包括severity_level和score
    Object.assign(assessmentModule.form, {
      ...row,
      failure_mode: row.failure_mode?.id || row.failure_mode,
      project_instance_name: row.project_instance_name || ''
    })
    assessmentModule.currentId = row.id
  } else {
    resetAssessmentForm()
  }
}

// 关闭评定表单
const closeAssessmentForm = () => {
  assessmentModule.dialogVisible = false
  resetAssessmentForm()
}

// 重置评定表单
const resetAssessmentForm = () => {
  if (assessmentFormRef.value) {
    assessmentFormRef.value.resetFields()
  }
  Object.assign(assessmentModule.form, {
    id: null,
    failure_mode: '',
    severity_value: null,
    occurrence_value: null,
    detection_value: null,
    rpn_value: null,
    project_instance_name: '',
    is_active: true
  })
  assessmentModule.currentId = null
}

// 根据severity_value获取对应的severity_level对象
const getSeverityLevelByValue = (value) => {
  console.log('开始查找对应的严酷度等级，value:', value)
  // 根据value确定应该选择哪个等级
  let level = 'Ⅳ' // 默认轻微
  
  if (value >= 8) {
    level = 'Ⅰ' // 灾难性
  } else if (value >= 6) {
    level = 'Ⅱ' // 严重
  } else if (value >= 3) {
    level = 'Ⅲ' // 中等
  }
  
  console.log('确定的等级代码:', level)
  console.log('当前severityLevelList:', severityLevelList.value)
  // 从severityLevelList中查找对应的等级对象
  const severityLevel = severityLevelList.value.find(item => item.level === level)
  console.log('找到的severityLevel:', severityLevel)
  return severityLevel
}

// 提交评定表单
const submitAssessmentForm = async () => {
  if (!assessmentFormRef.value) return
  try {
    await assessmentFormRef.value.validate()
    
    // 获取对应的severity_level对象
    const severityLevel = getSeverityLevelByValue(assessmentModule.form.severity_value)
    
    if (!severityLevel) {
      console.error('未找到对应的严酷度等级')
      ElMessage.error('未找到对应的严酷度等级，请重试')
      return
    }
    
    const formData = {
      failure_mode: assessmentModule.form.failure_mode,
      severity_level: severityLevel.id, // 传递等级ID而不是字符串
      severity_value: assessmentModule.form.severity_value,
      occurrence_value: assessmentModule.form.occurrence_value,
      detection_value: assessmentModule.form.detection_value,
      rpn_value: assessmentModule.form.rpn_value,
      score: severityLevel.score, // 使用等级对应的分数
      project_instance_name: assessmentModule.form.project_instance_name, // 添加项目实例名称字段
      evidence: '', // 添加evidence字段，允许为空
      is_active: assessmentModule.form.is_active
    }

    console.log('提交的表单数据:', formData)
    console.log('severity_level类型:', typeof severityLevel.id)

    if (assessmentModule.isEditing) {
      // 编辑操作
      await severityApi.updateSeverityAssessment(assessmentModule.currentId, formData)
      ElMessage.success('评定编辑成功')
    } else {
      // 新增操作
      await severityApi.createSeverityAssessment(formData)
      ElMessage.success('评定新增成功')
    }

    assessmentModule.dialogVisible = false
    loadAssessmentData()
  } catch (error) {
    console.error('提交评定表单失败:', error)
    console.error('错误详情:', error.response?.data)
    console.error('请求配置:', error.config)
    console.error('请求数据:', error.config?.data)
    if (error.response?.data) {
      // 显示更详细的错误信息
      const errorMessages = Object.entries(error.response.data).map(([key, value]) => `${key}: ${value}`).join('; ')
      ElMessage.error(`操作失败: ${errorMessages}`)
    } else {
      ElMessage.error('操作失败，请重试')
    }
  }
}

// 删除评定
const deleteAssessment = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除评定记录吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await severityApi.deleteSeverityAssessment(row.id)
    ElMessage.success('评定删除成功')
    loadAssessmentData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除评定失败:', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

// 分页处理函数
const handleAssessmentSizeChange = (size) => {
  assessmentModule.pagination.pageSize = size
  loadAssessmentData()
}

const handleAssessmentCurrentChange = (page) => {
  assessmentModule.pagination.page = page
  loadAssessmentData()
}

// 辅助函数
// 获取等级颜色
const getLevelTypeColor = (level) => {
  const colorMap = {
    'Ⅰ': 'danger',
    'Ⅱ': 'warning',
    'Ⅲ': 'info',
    'Ⅳ': 'success'
  }
  return colorMap[level] || 'info'
}

// 获取RPN颜色
const getRpnTypeColor = (rpn) => {
  if (rpn > rpnConfigModule.form.high_risk_threshold) {
    return 'danger'
  } else if (rpn > rpnConfigModule.form.medium_risk_threshold) {
    return 'warning'
  } else {
    return 'success'
  }
}

// 获取严酷度描述
const getSeverityDescription = (value) => {
  const descriptions = [
    '', '无影响', '轻微', '轻微', '中等', '中等', '严重', '严重', '灾难性', '灾难性', '灾难性'
  ]
  return descriptions[value] || ''
}

// 获取发生度描述
const getOccurrenceDescription = (value) => {
  const descriptions = [
    '', '极低', '低', '中低', '中等', '中高', '高', '很高', '极高', '非常高', '必然'
  ]
  return descriptions[value] || ''
}

// 获取检测度描述
const getDetectionDescription = (value) => {
  const descriptions = [
    '', '肯定检测', '很可能检测', '可能检测', '中等可能', '不太可能', '低', '很低', '极低', '几乎不可能', '完全不可能'
  ]
  return descriptions[value] || ''
}



// 页面初始化
onMounted(async () => {
  await Promise.all([loadFailureModes(), loadSeverityLevels()])
  loadAssessmentData()
})
</script>

<style scoped>
.severity-management {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.toolbar-left {
  display: flex;
  gap: 12px;
}

.toolbar-right {
  display: flex;
  gap: 12px;
}

.table-card {
  border: none;
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.tab-content {
  padding: 16px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #f0f9eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.danger {
  background-color: #fef2f2;
}

.stat-icon.warning {
  background-color: #fff7e6;
}

.stat-icon.success {
  background-color: #f0f9eb;
}

.icon-large {
  font-size: 24px;
  color: #67c23a;
}

.stat-icon.danger .icon-large {
  color: #f56c6c;
}

.stat-icon.warning .icon-large {
  color: #e6a23c;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .toolbar-left,
  .toolbar-right {
    justify-content: center;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }
}
</style>