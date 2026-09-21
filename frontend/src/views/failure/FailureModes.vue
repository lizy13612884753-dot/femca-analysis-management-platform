<template>
  <div class="failure-modes">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>故障模式管理</h1>
      <p>管理设备故障模式，包括原因和影响分析</p>
    </div>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增故障模式
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
    
    <!-- 过滤器 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-select v-model="filters.equipmentType" placeholder="设备类型" clearable @change="handleFilterChange">
            <el-option v-for="type in equipmentTypes" :key="type.id" :label="type.name" :value="type.id" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.severity" placeholder="严重程度" clearable @change="handleFilterChange">
            <el-option label="极高" value="A" />
            <el-option label="高" value="B" />
            <el-option label="中等" value="C" />
            <el-option label="低" value="D" />
            <el-option label="极低" value="E" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button @click="handleResetFilters">重置筛选</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="failureModes"
        style="width: 100%"
        stripe
      >
        <el-table-column label="ID" width="80">
          <template #default="{ row, $index }">
            {{ (pagination.page - 1) * pagination.pageSize + $index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="name" label="故障模式名称" min-width="150" />
        <el-table-column prop="code" label="项目实例名称" width="120" />
        <el-table-column prop="equipment_type_name" label="设备类型" width="120" />
        <el-table-column prop="function_name" label="功能名称" width="120" />
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getSeverityColor(row.severity)" size="small">
              {{ getSeverityName(row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cause_count" label="故障原因" min-width="200">
          <template #default="{ row }">
            {{ row.causes || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="effect_count" label="故障影响" min-width="200">
          <template #default="{ row }">
            {{ parseFailureEffectDetail(row.failure_effect, 'local') || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_by_name" label="创建人" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleViewDetails(row)">
              详情
            </el-button>
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
    
    <!-- 故障模式详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="故障模式详情"
      width="800px"
    >
      <div v-if="selectedFailure" class="failure-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="故障模式名称">
            {{ selectedFailure.name }}
          </el-descriptions-item>
          <el-descriptions-item label="设备类型">
            {{ selectedFailure.equipment_type_name }}
          </el-descriptions-item>
          <el-descriptions-item label="功能名称">
            {{ selectedFailure.function_name }}
          </el-descriptions-item>
          <el-descriptions-item label="功能状态">
            {{ selectedFailure.function_status }}
          </el-descriptions-item>
          <el-descriptions-item label="严重程度">
            {{ selectedFailure.severity }}
          </el-descriptions-item>
          <el-descriptions-item label="发生频率">
            {{ selectedFailure.frequency }}
          </el-descriptions-item>
          <el-descriptions-item label="项目实例名称">
            {{ selectedFailure.code }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人">
            {{ selectedFailure.created_by_name }}
          </el-descriptions-item>
          <el-descriptions-item label="局部影响" :span="2">
            {{ parseFailureEffectDetail(selectedFailure.failure_effect, 'local') || '无局部影响描述' }}
          </el-descriptions-item>
          <el-descriptions-item label="高一层影响" :span="2">
            {{ parseFailureEffectDetail(selectedFailure.failure_effect, 'higher') || '无高一层影响描述' }}
          </el-descriptions-item>
          <el-descriptions-item label="最终影响" :span="2">
            {{ parseFailureEffectDetail(selectedFailure.failure_effect, 'final') || '无最终影响描述' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 新增/编辑故障模式对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑故障模式' : '新增故障模式'"
      width="800px"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="120px" style="max-width: 600px; margin: 0 auto;">
        <el-form-item label="故障模式名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入故障模式名称" />
        </el-form-item>
        <el-form-item label="项目实例名称" prop="code">
          <el-input v-model="formData.code" placeholder="请输入项目实例名称" />
        </el-form-item>
        <el-form-item label="设备类型" prop="equipment_type">
          <el-select v-model="formData.equipment_type" placeholder="请选择设备类型" style="width: 100%;">
            <el-option
              v-for="item in equipmentTypes"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="功能名称" prop="function_name">
          <el-input v-model="formData.function_name" placeholder="请输入功能名称" />
        </el-form-item>
        <el-form-item label="功能状态">
          <el-select v-model="formData.function_status" placeholder="请选择功能状态" style="width: 100%;">
            <el-option label="丧失功能" value="1" />
            <el-option label="功能降级" value="2" />
            <el-option label="功能无影响" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="formData.severity" placeholder="请选择严重程度" style="width: 100%;">
            <el-option label="极高" value="A" />
            <el-option label="高" value="B" />
            <el-option label="中等" value="C" />
            <el-option label="低" value="D" />
            <el-option label="极低" value="E" />
          </el-select>
        </el-form-item>
        <!-- 故障影响细分 -->
        <el-form-item label="局部影响" prop="local_effect">
          <el-input
            v-model="formData.local_effect"
            type="textarea"
            placeholder="请输入局部影响（直接影响的部件或功能）"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="高一层影响" prop="higher_effect">
          <el-input
            v-model="formData.higher_effect"
            type="textarea"
            placeholder="请输入高一层影响（对系统或子系统的影响）"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="最终影响" prop="final_effect">
          <el-input
            v-model="formData.final_effect"
            type="textarea"
            placeholder="请输入最终影响（对整个设备或用户的影响）"
            :rows="2"
          />
        </el-form-item>
        <el-form-item label="故障检测方法" prop="detection_methods">
          <el-input
            v-model="formData.detection_methods"
            type="textarea"
            placeholder="请输入故障检测方法"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="故障描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            placeholder="请输入故障描述"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="故障原因">
          <el-input
            v-model="formData.causes"
            type="textarea"
            placeholder="请输入故障原因"
            :rows="3"
          />
        </el-form-item>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Warning } from '@element-plus/icons-vue'
import * as failureApi from '@/api/failure'
import * as equipmentApi from '@/api/equipment'

// 响应式数据
const loading = ref(false)
const searchQuery = ref('')

// 过滤器
const filters = reactive({
  equipmentType: '',
  severity: ''
})

// 设备类型列表
const equipmentTypes = ref([])
const failureModes = ref([])
const selectedFailure = ref(null)
const editingFailureId = ref(null)

const detailDialogVisible = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 表单数据
const formData = reactive({
  name: '',
  code: '',
  description: '',
  equipment_type: null,
  function_name: '',
  function_status: '1',
  // 故障影响细分
  local_effect: '',
  higher_effect: '',
  final_effect: '',
  severity: 'C',
  detection_methods: '',
  causes: ''
  // 删除了effects字段，后端模型中不存在这个字段
})

// 自定义故障影响验证规则
const validateFailureEffects = (rule, value, callback) => {
  // 只检查三个影响字段中是否至少有一个不为空
  // 无论当前验证的是哪个字段，都检查所有三个字段
  if (!formData.local_effect && !formData.higher_effect && !formData.final_effect) {
    callback(new Error('请至少填写一个故障影响字段'))
  } else {
    callback()
  }
}

// 表单验证规则
const formRules = reactive({
  name: [
    { required: true, message: '请输入故障模式名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入项目实例名称', trigger: 'blur' }
  ],
  equipment_type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  function_name: [
    { required: true, message: '请输入功能名称', trigger: 'blur' }
  ],
  detection_methods: [
    { required: true, message: '请输入故障检测方法', trigger: 'blur' }
  ],
  // 在所有三个故障影响字段上应用自定义验证规则
  local_effect: [
    { validator: validateFailureEffects, trigger: ['blur', 'change'] }
  ],
  higher_effect: [
    { validator: validateFailureEffects, trigger: ['blur', 'change'] }
  ],
  final_effect: [
    { validator: validateFailureEffects, trigger: ['blur', 'change'] }
  ]
})

// 严重程度映射
const severityMap = {
  'A': { name: '极高', color: 'danger' },
  'B': { name: '高', color: 'warning' },
  'C': { name: '中等', color: 'warning' },
  'D': { name: '低', color: 'success' },
  'E': { name: '极低', color: 'success' }
}

// 解析故障影响详情
const parseFailureEffectDetail = (failureEffect, type) => {
  if (!failureEffect) return ''
  
  // 定义不同影响类型的前缀
  const prefixes = {
    local: '局部影响：',
    higher: '高一层影响：',
    final: '最终影响：'
  }
  
  // 获取当前类型的前缀
  const prefix = prefixes[type]
  
  // 按换行符分割成多行
  const lines = failureEffect.split(/\r?\n/)
  
  // 遍历所有行，查找匹配的前缀
  for (const line of lines) {
    // 检查行是否以当前类型的前缀开头
    if (line.startsWith(prefix)) {
      // 如果找到匹配的行，则提取出影响描述并返回
      return line.substring(prefix.length).trim()
    }
  }
  
  // 如果没有找到匹配的行，则返回空字符串
  return ''
}


// 获取严重程度显示名称
const getSeverityName = (severity) => {
  return severityMap[severity]?.name || severity
}

// 获取严重程度颜色
const getSeverityColor = (severity) => {
  return severityMap[severity]?.color || 'info'
}

// 格式化时间
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return ''
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
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

// 加载故障模式数据
const loadFailureModes = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchQuery.value
    }
    
    // 添加过滤器
    if (filters.equipmentType) {
      params.equipment_type = filters.equipmentType
    }
    if (filters.severity) {
      params.severity = filters.severity
    }
    
    const response = await failureApi.getFailureModes(params)
    failureModes.value = response.results || []
    pagination.total = response.count || 0
  } catch (error) {
    ElMessage.error('加载故障模式列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  loadFailureModes()
}

// 过滤器变化处理
const handleFilterChange = () => {
  pagination.page = 1
  loadFailureModes()
}

// 重置过滤器
const handleResetFilters = () => {
  Object.assign(filters, {
    equipmentType: '',
    severity: ''
  })
  pagination.page = 1
  loadFailureModes()
}

// 分页变化处理
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadFailureModes()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadFailureModes()
}

// 重置表单
const resetForm = () => {
  // 显式地将所有字段重置为它们的初始值
  Object.assign(formData, {
    name: '',
    code: '',
    description: '',
    equipment_type: null,
    function_name: '',
    function_status: '1',
    local_effect: '',
    higher_effect: '',
    final_effect: '',
    severity: 'C',
    detection_methods: '',
    causes: ''
  })
  
  // 调用resetFields方法，确保表单验证状态也被重置
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 新增故障模式
const handleAdd = () => {
  // 先重置表单
  resetForm()
  
  isEdit.value = false
  editingFailureId.value = null
  dialogVisible.value = true
}

// 编辑故障模式
const handleEdit = async (row) => {
  try {
    loading.value = true
    isEdit.value = true
    editingFailureId.value = row.id
    const response = await failureApi.getFailureMode(row.id)
    const failureMode = response
    
    // 解析故障影响字段
    const parseFailureEffects = (failureEffect) => {
      const effects = { local_effect: '', higher_effect: '', final_effect: '' }
      if (!failureEffect) return effects
      
      // 使用正则表达式分割，可以处理不同的换行符格式
      const lines = failureEffect.split(/\r?\n/)
      lines.forEach(line => {
        if (line.startsWith('局部影响：')) {
          effects.local_effect = line.replace('局部影响：', '')
        } else if (line.startsWith('高一层影响：')) {
          effects.higher_effect = line.replace('高一层影响：', '')
        } else if (line.startsWith('最终影响：')) {
          effects.final_effect = line.replace('最终影响：', '')
        }
      })
      
      return effects
    }
    
    const effects = parseFailureEffects(failureMode.failure_effect)
    
    // 填充表单数据
    Object.assign(formData, {
      name: failureMode.name,
      code: failureMode.code,
      description: failureMode.description || '',
      equipment_type: failureMode.equipment_type,
      function_name: failureMode.function_name,
      function_status: failureMode.function_status,
      // 设置细分的故障影响字段
      local_effect: effects.local_effect,
      higher_effect: effects.higher_effect,
      final_effect: effects.final_effect,
      severity: failureMode.severity,
      detection_methods: failureMode.detection_methods || '',
      causes: failureMode.causes || ''
      // 删除了effects字段，后端模型中不存在这个字段
    })
    
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('加载故障模式详情失败')
  } finally {
    loading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    

    
    // 确保字段值是字符串类型，避免表单验证将它们转换为数组
    const localEffect = Array.isArray(formData.local_effect) ? formData.local_effect.join('') : formData.local_effect
    const higherEffect = Array.isArray(formData.higher_effect) ? formData.higher_effect.join('') : formData.higher_effect
    const finalEffect = Array.isArray(formData.final_effect) ? formData.final_effect.join('') : formData.final_effect
    

    
    // 构建提交数据，只包含后端模型中存在的字段
    const submitData = {
      name: formData.name,
      code: formData.code,
      description: formData.description,
      equipment_type: formData.equipment_type, // 确保这是一个有效的ID
      function_name: formData.function_name,
      function_status: formData.function_status,
      detection_methods: formData.detection_methods,
      causes: formData.causes,
      severity: formData.severity
    }
    
    // 将三个故障影响字段合并为一个failure_effect字段
    const effects = []
    if (localEffect) effects.push(`局部影响：${localEffect}`)
    if (higherEffect) effects.push(`高一层影响：${higherEffect}`)
    if (finalEffect) effects.push(`最终影响：${finalEffect}`)
    
    // 设置failure_effect字段，后端需要这个字段
    // 使用单个换行符分隔，以便解析方法能够正确处理
    submitData.failure_effect = effects.join('\n')
    
    // 添加调试日志
    console.log('Submit Data:', submitData)


    if (isEdit.value) {
      // 编辑故障模式
      const updateResult = await failureApi.updateFailureMode(editingFailureId.value, submitData)
      console.log('Update Result:', updateResult)
      ElMessage.success('编辑故障模式成功')
    } else {
      // 新增故障模式
      const createResult = await failureApi.createFailureMode(submitData)
      console.log('Create Result:', createResult)
      ElMessage.success('新增故障模式成功')
    }
    
    dialogVisible.value = false
    loadFailureModes()
  } catch (error) {
    console.error('提交失败:', error)
    // 检查是否是表单验证错误
    if (typeof error === 'object' && error !== null && !Array.isArray(error)) {
      if ('response' in error) {
        // 这是一个Axios错误
        console.error('响应状态:', error.response.status)
        console.error('响应数据:', error.response.data)
        
        // 提供更详细的错误信息
        let errorMessage = isEdit.value ? '编辑故障模式失败' : '新增故障模式失败'
        if (error.response.status === 400) {
          const data = error.response.data
          if (data.code && Array.isArray(data.code)) {
            errorMessage = `项目实例名称: ${data.code[0]}`
          } else if (data.name && Array.isArray(data.name)) {
            errorMessage = `故障模式名称: ${data.name[0]}`
          } else {
            // 尝试提取其他字段的错误信息
            const fieldErrors = Object.entries(data)
            if (fieldErrors.length > 0) {
              const [field, messages] = fieldErrors[0]
              errorMessage = `${field}: ${messages[0]}`
            }
          }
        }
        
        ElMessage.error(errorMessage)
      } else if ('message' in error) {
        // 这是其他标准错误
        ElMessage.error(isEdit.value ? '编辑故障模式失败' : '新增故障模式失败')
      }
    } else {
      // 这是表单验证错误，不显示通用错误消息
      // 让Element Plus的表单验证自动显示错误提示
    }
  } finally {
    loading.value = false
  }
}

// 查看详情
const handleViewDetails = async (row) => {
  try {
    loading.value = true
    // 通过API获取完整的故障模式详情
    const detail = await failureApi.getFailureMode(row.id)
    selectedFailure.value = detail
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取故障模式详情失败')
  } finally {
    loading.value = false
  }
}

// 删除故障模式
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除故障模式"${row.name}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await failureApi.deleteFailureMode(row.id)
    ElMessage.success('删除故障模式成功')
    loadFailureModes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除故障模式失败')
    }
  }
}

onMounted(async () => {
  await loadEquipmentTypes()
  await loadFailureModes()
})
</script>

<style scoped>
.failure-modes {
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

.filter-card {
  margin: 20px 0;
  border-radius: 4px;
  border: none;
}

.table-card {
  border: none;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.failure-details {
  padding: 16px 0;
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
}


</style>