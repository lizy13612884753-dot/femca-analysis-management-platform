<template>
  <div class="effectiveness-evaluation">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>有效性评估管理</h1>
      <p>管理补偿措施的有效性评估结果和趋势分析</p>
    </div>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增评估
        </el-button>
        <el-button @click="handleViewTrends">
          <el-icon><TrendCharts /></el-icon>
          趋势分析
        </el-button>
      </div>
      <div class="toolbar-right">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="handleDateRangeChange"
          style="margin-right: 10px"
        />
        <el-input
          v-model="searchQuery"
          placeholder="搜索评估..."
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
    
    <!-- 筛选条件 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="补偿措施">
            <el-select
              v-model="filters.compensationMeasure"
              placeholder="请选择补偿措施"
              clearable
              style="width: 100%"
              @change="handleFilterChange"
              filterable
            >
              <el-option
                v-for="measure in compensationMeasures"
                :key="measure.id"
                :label="measure.name"
                :value="measure.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="评估人">
            <el-select
              v-model="filters.evaluator"
              placeholder="请选择评估人"
              clearable
              style="width: 100%"
              @change="handleFilterChange"
              filterable
            >
              <el-option
                v-for="user in evaluators"
                :key="user.id"
                :label="user.name"
                :value="user.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="效果等级">
            <el-select
              v-model="filters.effectivenessLevel"
              placeholder="请选择效果等级"
              clearable
              style="width: 100%"
              @change="handleFilterChange"
            >
              <el-option label="优秀 (>90%)" :value="90" />
              <el-option label="良好 (70-90%)" :value="70" />
              <el-option label="一般 (50-70%)" :value="50" />
              <el-option label="较差 (<50%)" :value="0" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 评估统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="stat-text">
              <div class="stat-value">{{ statistics.totalEvaluations }}</div>
              <div class="stat-label">总评估次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-text">
              <div class="stat-value">{{ statistics.averageEffectiveness }}%</div>
              <div class="stat-label">平均效果</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><ArrowUp /></el-icon>
            </div>
            <div class="stat-text">
              <div class="stat-value">{{ statistics.bestEffectiveness }}%</div>
              <div class="stat-label">最高效果</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><ArrowDown /></el-icon>
            </div>
            <div class="stat-text">
              <div class="stat-value">{{ statistics.worstEffectiveness }}%</div>
              <div class="stat-label">最低效果</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 评估表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="effectivenessEvaluations"
        style="width: 100%"
        stripe
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column prop="compensation_measure" label="补偿措施" width="200" sortable="custom">
          <template #default="{ row }">
            <el-link type="primary" @click="handleViewCompensation(row.compensation_measure.id)">
              {{ row.compensation_measure.name }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="evaluation_date" label="评估日期" width="120" sortable="custom" />
        <el-table-column prop="evaluator" label="评估人" width="120" />
        <el-table-column prop="actual_effectiveness" label="实际效果" width="120" sortable="custom">
          <template #default="{ row }">
            <el-tag :type="getEffectivenessColor(row.actual_effectiveness)" size="small">
              {{ row.actual_effectiveness }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expected_effectiveness" label="预期效果" width="120">
          <template #default="{ row }">
            <el-tag type="info" size="small">
              {{ row.compensation_measure.effectiveness }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="deviation" label="偏差" width="100" sortable="custom">
          <template #default="{ row }">
            <el-tag :type="getDeviationColor(row.deviation)" size="small">
              {{ row.deviation > 0 ? '+' : '' }}{{ row.deviation }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="notes" label="备注" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
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
    
    <!-- 有效性评估表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '新增有效性评估' : '编辑有效性评估'"
      width="700px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="补偿措施" prop="compensation_measure">
              <el-select
                v-model="form.compensation_measure"
                placeholder="请选择补偿措施"
                style="width: 100%"
                @change="handleCompensationChange"
                filterable
              >
                <el-option
                  v-for="measure in compensationMeasures"
                  :key="measure.id"
                  :label="measure.name"
                  :value="measure.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="评估日期" prop="evaluation_date">
              <el-date-picker
                v-model="form.evaluation_date"
                type="date"
                placeholder="请选择评估日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="实际效果" prop="actual_effectiveness">
              <el-rate
                v-model="form.actual_effectiveness"
                show-score
                text-color="#99A9BF"
                score-template="{value}%"
                @change="handleEffectivenessChange"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="偏差" prop="deviation">
              <el-tag :type="getDeviationColor(form.deviation)" size="large">
                {{ form.deviation > 0 ? '+' : '' }}{{ form.deviation }}%
              </el-tag>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="4"
            placeholder="请输入评估备注"
          />
        </el-form-item>
        <el-alert
          v-if="selectedCompensation"
          :title="`预期效果：${selectedCompensation.effectiveness}%`"
          type="info"
          :closable="false"
          show-icon
        />
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确认</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 趋势分析对话框 -->
    <el-dialog
      v-model="trendsDialogVisible"
      title="补偿措施效果趋势分析"
      width="900px"
      @close="handleTrendsDialogClose"
    >
      <div v-if="trendsData" class="trends-analysis">
        <el-tabs v-model="activeTab" type="card">
          <el-tab-pane label="整体趋势" name="overall">
            <div id="overallTrendChart" style="height: 400px; width: 100%;"></div>
          </el-tab-pane>
          <el-tab-pane label="措施对比" name="comparison">
            <div id="comparisonChart" style="height: 400px; width: 100%;"></div>
          </el-tab-pane>
          <el-tab-pane label="效果分布" name="distribution">
            <div id="distributionChart" style="height: 400px; width: 100%;"></div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="trendsDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Search, TrendCharts, DataAnalysis, ArrowUp, ArrowDown
} from '@element-plus/icons-vue'
import {
  getEffectivenessEvaluations,
  createEffectivenessEvaluation,
  updateEffectivenessEvaluation,
  deleteEffectivenessEvaluation,
  getEffectivenessEvaluationsForCompensation,
  getRecentEvaluations
} from '@/api/compensation'
import * as echarts from 'echarts'

export default {
  name: 'EffectivenessEvaluation',
  components: {
    Plus,
    Search,
    TrendCharts,
    DataAnalysis,
    ArrowUp,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    
    // 响应式数据
    const loading = ref(false)
    const effectivenessEvaluations = ref([])
    const compensationMeasures = ref([])
    const evaluators = ref([])
    const dialogVisible = ref(false)
    const trendsDialogVisible = ref(false)
    const dialogMode = ref('add')
    const searchQuery = ref('')
    const formRef = ref(null)
    const currentRow = ref(null)
    const dateRange = ref([])
    const activeTab = ref('overall')
    const trendsData = ref(null)
    const selectedCompensation = ref(null)
    
    // 分页数据
    const pagination = reactive({
      page: 1,
      pageSize: 10,
      total: 0
    })
    
    // 统计数据
    const statistics = reactive({
      totalEvaluations: 0,
      averageEffectiveness: 0,
      bestEffectiveness: 0,
      worstEffectiveness: 100
    })
    
    // 筛选条件
    const filters = reactive({
      compensationMeasure: '',
      evaluator: '',
      effectivenessLevel: ''
    })
    
    // 表单数据
    const form = reactive({
      compensation_measure: '',
      evaluation_date: '',
      actual_effectiveness: 0,
      deviation: 0,
      notes: ''
    })
    
    // 表单验证规则
    const formRules = {
      compensation_measure: [
        { required: true, message: '请选择补偿措施', trigger: 'change' }
      ],
      evaluation_date: [
        { required: true, message: '请选择评估日期', trigger: 'change' }
      ],
      actual_effectiveness: [
        { required: true, message: '请评估实际效果', trigger: 'change' }
      ]
    }
    
    // 获取补偿措施列表
    const fetchCompensationMeasures = () => {
      // 示例数据
      compensationMeasures.value = [
        { id: 1, name: '定期维护', effectiveness: 85 },
        { id: 2, name: '预防性更换', effectiveness: 90 },
        { id: 3, name: '实时监测', effectiveness: 95 },
        { id: 4, name: '安全联锁', effectiveness: 100 },
        { id: 5, name: '冗余设计', effectiveness: 80 }
      ]
    }
    
    // 获取评估人列表
    const fetchEvaluators = () => {
      // 示例数据
      evaluators.value = [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' },
        { id: 3, name: '王五' },
        { id: 4, name: '赵六' }
      ]
    }
    
    // 获取有效性评估列表
    const fetchEffectivenessEvaluations = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.page,
          page_size: pagination.pageSize,
          search: searchQuery.value || undefined,
          ordering: getSortParams().ordering,
          compensation_measure: filters.compensationMeasure || undefined,
          evaluator: filters.evaluator || undefined,
          min_effectiveness: filters.effectivenessLevel || undefined
        }
        
        // 处理日期范围
        if (dateRange.value && dateRange.value.length === 2) {
          params.start_date = dateRange.value[0]
          params.end_date = dateRange.value[1]
        }
        
        const response = await getEffectivenessEvaluations(params)
        effectivenessEvaluations.value = response.results || response.data || []
        pagination.total = response.count || response.total || 0
        
        // 计算统计数据
        calculateStatistics()
      } catch (error) {
        console.error('获取有效性评估列表失败:', error)
        ElMessage.error('获取有效性评估列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 计算统计数据
    const calculateStatistics = () => {
      if (!effectivenessEvaluations.value || effectivenessEvaluations.value.length === 0) {
        statistics.totalEvaluations = 0
        statistics.averageEffectiveness = 0
        statistics.bestEffectiveness = 0
        statistics.worstEffectiveness = 0
        return
      }
      
      statistics.totalEvaluations = effectivenessEvaluations.value.length
      const total = effectivenessEvaluations.value.reduce((sum, item) => sum + item.actual_effectiveness, 0)
      statistics.averageEffectiveness = Math.round(total / effectivenessEvaluations.value.length)
      
      const effectivenessValues = effectivenessEvaluations.value.map(item => item.actual_effectiveness)
      statistics.bestEffectiveness = Math.max(...effectivenessValues)
      statistics.worstEffectiveness = Math.min(...effectivenessValues)
    }
    
    // 获取排序参数
    const getSortParams = () => {
      return {
        ordering: `${currentSortOrder.value === 'ascending' ? '' : '-'}${currentSortField.value}`
      }
    }
    
    // 排序字段和顺序
    const currentSortField = ref('')
    const currentSortOrder = ref('')
    
    // 处理排序变化
    const handleSortChange = ({ prop, order }) => {
      currentSortField.value = prop
      currentSortOrder.value = order
      pagination.page = 1
      fetchEffectivenessEvaluations()
    }
    
    // 处理日期范围变化
    const handleDateRangeChange = () => {
      pagination.page = 1
      fetchEffectivenessEvaluations()
    }
    
    // 搜索有效性评估
    const handleSearch = async () => {
      pagination.page = 1
      await fetchEffectivenessEvaluations()
    }
    
    // 处理筛选条件变化
    const handleFilterChange = () => {
      pagination.page = 1
      fetchEffectivenessEvaluations()
    }
    
    // 处理分页大小变化
    const handleSizeChange = (size) => {
      pagination.pageSize = size
      pagination.page = 1
      fetchEffectivenessEvaluations()
    }
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      pagination.page = page
      fetchEffectivenessEvaluations()
    }
    
    // 处理新增
    const handleAdd = () => {
      dialogMode.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 处理编辑
    const handleEdit = (row) => {
      dialogMode.value = 'edit'
      currentRow.value = row
      resetForm()
      
      // 填充表单数据
      form.compensation_measure = row.compensation_measure.id
      form.evaluation_date = row.evaluation_date
      form.actual_effectiveness = row.actual_effectiveness
      form.deviation = row.deviation
      form.notes = row.notes
      
      // 获取选中的补偿措施
      selectedCompensation.value = compensationMeasures.value.find(m => m.id === row.compensation_measure.id)
      
      dialogVisible.value = true
    }
    
    // 处理删除
    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除 "${row.compensation_measure.name}" 的评估记录吗？`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await deleteEffectivenessEvaluation(row.id)
        ElMessage.success('删除成功')
        fetchEffectivenessEvaluations()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    // 处理补偿措施变化
    const handleCompensationChange = (value) => {
      if (value) {
        selectedCompensation.value = compensationMeasures.value.find(m => m.id === value)
        // 计算偏差
        if (form.actual_effectiveness) {
          form.deviation = form.actual_effectiveness - selectedCompensation.value.effectiveness
        }
      } else {
        selectedCompensation.value = null
      }
    }
    
    // 处理实际效果变化
    const handleEffectivenessChange = () => {
      if (selectedCompensation.value && form.actual_effectiveness) {
        form.deviation = form.actual_effectiveness - selectedCompensation.value.effectiveness
      }
    }
    
    // 查看补偿措施
    const handleViewCompensation = (id) => {
      router.push(`/compensation/measures/${id}`)
    }
    
    // 重置表单
    const resetForm = () => {
      form.compensation_measure = ''
      form.evaluation_date = ''
      form.actual_effectiveness = 0
      form.deviation = 0
      form.notes = ''
      selectedCompensation.value = null
      formRef.value && formRef.value.clearValidate()
    }
    
    // 处理对话框关闭
    const handleDialogClose = () => {
      resetForm()
      currentRow.value = null
    }
    
    // 提交表单
    const handleSubmit = async () => {
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogMode.value === 'add') {
              await createEffectivenessEvaluation(form)
              ElMessage.success('创建成功')
            } else {
              await updateEffectivenessEvaluation(currentRow.value.id, form)
              ElMessage.success('更新成功')
            }
            dialogVisible.value = false
            fetchEffectivenessEvaluations()
          } catch (error) {
            console.error('保存失败:', error)
            ElMessage.error('保存失败')
          }
        }
      })
    }
    
    // 查看趋势分析
    const handleViewTrends = async () => {
      loading.value = true
      try {
        // 获取最近30天的评估数据
        const response = await getRecentEvaluations(30)
        trendsData.value = response
        trendsDialogVisible.value = true
        
        // 初始化图表
        setTimeout(() => {
          initCharts()
        }, 100)
      } catch (error) {
        console.error('获取趋势分析失败:', error)
        ElMessage.error('获取趋势分析失败')
      } finally {
        loading.value = false
      }
    }
    
    // 处理趋势分析对话框关闭
    const handleTrendsDialogClose = () => {
      trendsData.value = null
      activeTab.value = 'overall'
    }
    
    // 初始化图表
    const initCharts = () => {
      if (!trendsData.value) return
      
      // 整体趋势图表
      const overallChart = echarts.init(document.getElementById('overallTrendChart'))
      const overallOption = {
        title: {
          text: '补偿措施效果整体趋势'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均效果', '预期效果']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: trendsData.value.dates
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            name: '平均效果',
            type: 'line',
            data: trendsData.value.average_effectiveness,
            smooth: true
          },
          {
            name: '预期效果',
            type: 'line',
            data: trendsData.value.expected_effectiveness,
            smooth: true,
            lineStyle: {
              type: 'dashed'
            }
          }
        ]
      }
      overallChart.setOption(overallOption)
      
      // 措施对比图表
      const comparisonChart = echarts.init(document.getElementById('comparisonChart'))
      const comparisonOption = {
        title: {
          text: '补偿措施效果对比'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['实际效果', '预期效果']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: trendsData.value.measure_names
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            name: '实际效果',
            type: 'bar',
            data: trendsData.value.actual_effectiveness
          },
          {
            name: '预期效果',
            type: 'bar',
            data: trendsData.value.expected_effectiveness
          }
        ]
      }
      comparisonChart.setOption(comparisonOption)
      
      // 效果分布图表
      const distributionChart = echarts.init(document.getElementById('distributionChart'))
      const distributionOption = {
        title: {
          text: '补偿措施效果分布'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '效果分布',
            type: 'pie',
            radius: '50%',
            data: trendsData.value.effectiveness_distribution,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      distributionChart.setOption(distributionOption)
    }
    
    // 获取效果颜色
    const getEffectivenessColor = (effectiveness) => {
      if (effectiveness >= 90) return 'success'
      if (effectiveness >= 70) return 'info'
      if (effectiveness >= 50) return 'warning'
      return 'danger'
    }
    
    // 获取偏差颜色
    const getDeviationColor = (deviation) => {
      if (deviation > 10) return 'success'
      if (deviation > 0) return 'info'
      if (deviation === 0) return 'warning'
      return 'danger'
    }
    
    // 初始化
    onMounted(() => {
      fetchCompensationMeasures()
      fetchEvaluators()
      fetchEffectivenessEvaluations()
    })
    
    return {
      // 响应式数据
      loading,
      effectivenessEvaluations,
      compensationMeasures,
      evaluators,
      dialogVisible,
      trendsDialogVisible,
      dialogMode,
      searchQuery,
      formRef,
      currentRow,
      dateRange,
      activeTab,
      trendsData,
      selectedCompensation,
      
      // 分页数据
      pagination,
      
      // 统计数据
      statistics,
      
      // 筛选条件
      filters,
      
      // 表单数据
      form,
      formRules,
      
      // 方法
      handleSearch,
      handleFilterChange,
      handleSortChange,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleEdit,
      handleDelete,
      handleCompensationChange,
      handleEffectivenessChange,
      handleViewCompensation,
      handleDialogClose,
      handleSubmit,
      handleViewTrends,
      handleTrendsDialogClose,
      handleDateRangeChange,
      
      // 辅助方法
      getEffectivenessColor,
      getDeviationColor
    }
  }
}
</script>

<style scoped>
.effectiveness-evaluation {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 500;
  margin: 0 0 8px 0;
}

.page-header p {
  color: #606266;
  font-size: 14px;
  margin: 0;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.toolbar-left {
  display: flex;
  gap: 10px;
}

.toolbar-right {
  display: flex;
  align-items: center;
}

.filter-card {
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 32px;
  color: #409EFF;
  margin-right: 15px;
}

.stat-text {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.trends-analysis {
  padding: 10px;
}
</style>