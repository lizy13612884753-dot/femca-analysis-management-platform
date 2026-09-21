<template>
  <div class="equipment-instances">
    <!-- 页面标题 -->
    <!-- 动态提取安装位置 -->
    <div class="page-header">
      <h1>设备实例管理</h1>
      <p>管理系统中的设备实例信息</p>
    </div>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增设备实例
        </el-button>
      </div>
      <div class="toolbar-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索设备实例..."
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
        <el-col :span="8">
          <el-select v-model="filters.equipmentType" placeholder="设备类型" clearable @change="handleFilterChange" style="width: 100%">
            <el-option
              v-for="type in equipmentTypes"
              :key="type.id"
              :label="type.name"
              :value="type.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.status" placeholder="设备状态" clearable @change="handleFilterChange">
            <el-option label="运行中" value="operational" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="故障" value="fault" />
            <el-option label="离线" value="offline" />
            <el-option label="已退役" value="decommissioned" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filters.location" placeholder="安装位置" clearable @change="handleFilterChange">
            <el-option
              v-for="location in uniqueLocations"
              :key="location"
              :label="location"
              :value="location"
            />
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
        :data="equipmentInstances"
        style="width: 100%"
        stripe
        @sort-change="handleSortChange"
      >
        <el-table-column prop="display_id" label="ID" width="80" sortable="custom" />
        <el-table-column prop="name" label="设备名称" min-width="150" sortable="custom" />
        <el-table-column prop="serial_number" label="序列号" width="120" />
        <el-table-column prop="equipment_type_name" label="设备类型" width="120" />
        <el-table-column prop="location" label="安装位置" width="120" />
        <el-table-column prop="install_date" label="安装日期" width="120" />
        <el-table-column prop="warranty_expire_date" label="保修到期日期" width="150" />
        <el-table-column prop="status" label="设备状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="function_description" label="功能描述" width="200" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.function_description || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_by_name" label="创建人" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="160" sortable="custom" />
        <el-table-column label="操作" width="180" fixed="right">
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
    
    <!-- 设备实例表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '新增设备实例' : '编辑设备实例'"
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
            <el-form-item label="设备名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入设备名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="序列号" prop="serial_number">
              <el-input v-model="form.serial_number" placeholder="请输入序列号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="设备类型" prop="equipment_type">
              <el-select v-model="form.equipment_type" placeholder="请选择设备类型" style="width: 100%" @change="onEquipmentTypeChange">
                <el-option
                  v-for="type in equipmentTypes"
                  :key="type.id"
                  :label="type.name"
                  :value="type.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="安装位置" prop="location">
              <el-input v-model="form.location" placeholder="请输入安装位置" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="安装日期" prop="install_date">
              <el-date-picker
                v-model="form.install_date"
                type="date"
                placeholder="请选择安装日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="保修到期日期" prop="warranty_expire_date">
              <el-date-picker
                v-model="form.warranty_expire_date"
                type="date"
                placeholder="请选择保修到期日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="功能描述" prop="function_description">
          <el-input
            v-model="form.function_description"
            type="textarea"
            :rows="3"
            placeholder="请输入功能描述"
          />
        </el-form-item>
        
        <el-form-item label="设备备注" prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入设备备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import {
  getEquipmentInstances,
  createEquipmentInstance,
  updateEquipmentInstance,
  deleteEquipmentInstance,
  getEquipmentTypes
} from '@/api/equipment'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const searchQuery = ref('')
const equipmentInstances = ref([])
const equipmentTypes = ref([])
const formRef = ref(null)
const uniqueLocations = ref([])

const dialogVisible = ref(false)
const dialogMode = ref('add') // 'add' | 'edit'
const currentId = ref(null)

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 排序数据
const sort = reactive({
  prop: 'equipment_type,created_at',
  order: 'ascending'
})

// 过滤器
const filters = reactive({
  equipmentType: null,
  status: '',
  location: ''
})

// 表单数据
const form = reactive({
  name: '',
  serial_number: '',
  equipment_type: null,
  location: '',
  install_date: null,
  warranty_expire_date: null,
  status: 'operational',
  function_description: '',
  notes: '',
  custom_specifications: {} // 添加自定义规格字段，默认值为空字典
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度应在2-100个字符', trigger: 'blur' }
  ],
  serial_number: [
    { required: true, message: '请输入序列号', trigger: 'blur' }
  ],
  equipment_type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  location: [
    { required: false, message: '请输入安装位置', trigger: 'blur' }
  ],
  status: [
    { required: false, message: '请选择设备状态', trigger: 'change' }
  ],
  function_description: [
    { required: false, message: '请输入功能描述', trigger: 'blur' }
  ],
  notes: [
    { required: false, message: '请输入设备备注', trigger: 'blur' }
  ]
}

// 获取状态标签类型
const getStatusType = (status) => {
  const statusMap = {
    operational: 'success',
    maintenance: 'warning',
    fault: 'danger',
    offline: 'info',
    decommissioned: 'info'
  }
  return statusMap[status] || ''
}

// 提取唯一的安装位置
const extractUniqueLocations = (instances) => {
  const locations = new Set()
  instances.forEach(instance => {
    if (instance.location && instance.location.trim()) {
      locations.add(instance.location.trim())
    }
  })
  uniqueLocations.value = Array.from(locations).sort()
  console.log('提取到的安装位置:', uniqueLocations.value)
}

// 加载设备实例列表
const loadEquipmentInstances = async () => {
  try {
    loading.value = true
    
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchQuery.value
    }
    
    // 添加过滤器
    if (filters.equipmentType !== null && filters.equipmentType !== '') {
      params.equipment_type = filters.equipmentType
    }
    if (filters.status) {
      params.status = filters.status
    }
    if (filters.location) {
      params.location = filters.location
    }
    
    if (sort.prop) {
      if (sort.order === 'descending') {
        params.ordering = sort.prop.split(',').map(field => `-${field.trim()}`).join(',')
      } else {
        params.ordering = sort.prop
      }
    }
    
    const response = await getEquipmentInstances(params)
    const instances = response.results || response.data || []
    console.log('DEBUG: API返回的原始数据:', instances[0])
    console.log('DEBUG: created_at原始值:', instances[0]?.created_at)
    // 转换时间格式
    const formattedInstances = instances.map(item => ({
      ...item,
      created_at: dayjs(item.created_at).format('YYYY-MM-DD HH:mm:ss')
    }))
    
    // 提取唯一的安装位置
    extractUniqueLocations(formattedInstances)
    
    // 按设备类型分组，每个设备类型内的实例按创建时间升序排序
    equipmentInstances.value = sortInstancesByTypeAndTime(formattedInstances)
    
    console.log('DEBUG: 格式化后的created_at:', equipmentInstances.value[0]?.created_at)
    pagination.total = response.count || response.total || 0
  } catch (error) {
    ElMessage.error('加载设备实例列表失败')
  } finally {
    loading.value = false
  }
}

// 加载设备类型列表
const loadEquipmentTypes = async () => {
  try {
    const response = await getEquipmentTypes({ page_size: 1000 })
    let types = response.results || response.data || []
    // 按照ID排序
    types.sort((a, b) => a.id - b.id)
    equipmentTypes.value = types
    console.log('加载的设备类型:', equipmentTypes.value)
  } catch (error) {
    console.error('加载设备类型列表失败:', error)
  }
}

// 设备类型选择变化处理
const onEquipmentTypeChange = (value) => {
  console.log('选择的设备类型ID:', value)
  console.log('form.equipment_type:', form.equipment_type)
}

// 按设备类型分组，每个设备类型内的实例按创建时间升序排序
const sortInstancesByTypeAndTime = (instances) => {
  // 按设备类型分组
  const grouped = {}
  instances.forEach(instance => {
    const typeId = instance.equipment_type
    if (!grouped[typeId]) {
      grouped[typeId] = []
    }
    grouped[typeId].push(instance)
  })
  
  // 对每个设备类型内的实例按创建时间升序排序
  Object.keys(grouped).forEach(typeId => {
    grouped[typeId].sort((a, b) => {
      return dayjs(a.created_at).isBefore(dayjs(b.created_at)) ? -1 : 1
    })
  })
  
  // 按设备类型ID排序，然后合并所有实例
  const sortedTypeIds = Object.keys(grouped).sort((a, b) => {
    return parseInt(a) - parseInt(b)
  })
  
  const sortedInstances = []
  sortedTypeIds.forEach(typeId => {
    sortedInstances.push(...grouped[typeId])
  })
  
  return sortedInstances
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  loadEquipmentInstances()
}

// 过滤器变化处理
const handleFilterChange = () => {
  pagination.page = 1
  loadEquipmentInstances()
}

// 重置过滤器
const handleResetFilters = () => {
  Object.assign(filters, {
    equipmentType: null,
    status: '',
    location: ''
  })
  pagination.page = 1
  loadEquipmentInstances()
}

// 排序变化处理
const handleSortChange = ({ prop, order }) => {
  sort.prop = prop
  sort.order = order
  pagination.page = 1
  loadEquipmentInstances()
}

// 分页变化处理
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadEquipmentInstances()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadEquipmentInstances()
}

// 新增设备实例
const handleAdd = () => {
  dialogMode.value = 'add'
  currentId.value = null
  resetForm()
  dialogVisible.value = true
}

// 编辑设备实例
const handleEdit = (row) => {
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(form, {
    name: row.name,
    serial_number: row.serial_number,
    equipment_type: row.equipment_type,
    location: row.location,
    install_date: row.install_date,
    warranty_expire_date: row.warranty_expire_date,
    status: row.status,
    function_description: row.function_description,
    notes: row.notes,
    custom_specifications: row.custom_specifications || {} // 确保自定义规格字段被赋值
  })
  dialogVisible.value = true
}

// 删除设备实例
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设备实例"${row.name}"吗？此操作不可恢复。`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteEquipmentInstance(row.id)
    ElMessage.success('删除成功')
    loadEquipmentInstances()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 表单提交
const handleSubmit = async () => {
  try {
    // 先进行表单验证
    if (!formRef.value) return;
    
    console.log('表单验证前的数据:', form);
    console.log('function_description值:', form.function_description);
    
    await formRef.value.validate();
    
    // 准备提交数据
    const submitData = {
      ...form,
      // 明确添加function_description字段，确保它被包含在提交数据中
      function_description: form.function_description
    };
    
    console.log('提交的数据:', submitData);
    console.log('提交数据包含function_description:', 'function_description' in submitData);
    console.log('提交数据中的function_description值:', submitData.function_description);
    
    submitLoading.value = true
    
    if (dialogMode.value === 'add') {
      await createEquipmentInstance(submitData)
      ElMessage.success('新增成功')
    } else {
      await updateEquipmentInstance(currentId.value, submitData)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    loadEquipmentInstances()
  } catch (error) {
    console.log('提交失败的错误:', error);
    
    // 检查是否是序列号重复错误
    if (error.response?.data?.non_field_errors && error.response.data.non_field_errors.length > 0) {
      const errorMsg = error.response.data.non_field_errors[0];
      if (errorMsg.includes('serial_number') || errorMsg.includes('序列号')) {
        ElMessage.error('序列号不应该相同')
      } else {
        ElMessage.error(dialogMode.value === 'add' ? '新增失败' : '更新失败')
      }
    } else if (error.name !== 'ValidationError') {
      ElMessage.error(dialogMode.value === 'add' ? '新增失败' : '更新失败')
    }
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    serial_number: '',
    equipment_type: null,
    location: '',
    install_date: null,
    warranty_expire_date: null,
    status: 'operational',
    function_description: '',
    notes: '',
    custom_specifications: {} // 重置自定义规格字段
  })
}

// 对话框关闭处理
const handleDialogClose = () => {
  resetForm()
}

// 监听搜索查询
watch(searchQuery, (newValue) => {
  if (!newValue) {
    pagination.page = 1
    loadEquipmentInstances()
  }
})

onMounted(() => {
  loadEquipmentTypes()
  loadEquipmentInstances()
})
</script>

<style scoped>
.equipment-instances {
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
  margin-bottom: 16px;
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
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