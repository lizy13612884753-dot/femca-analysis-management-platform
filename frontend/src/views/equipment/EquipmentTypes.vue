<template>
  <div class="equipment-types">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>设备类型管理</h1>
      <p>管理系统中的设备类型信息</p>
    </div>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增设备类型
        </el-button>
      </div>
      <div class="toolbar-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索设备类型..."
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
    
    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="equipmentTypes"
        style="width: 100%"
        stripe
        @sort-change="handleSortChange"
      >
        <el-table-column label="ID" width="80" sortable="custom">
          <template #default="{ $index }">
            {{ ($index + 1) + (pagination.page - 1) * pagination.pageSize }}
          </template>
        </el-table-column>
        <el-table-column prop="name" label="设备类型名称" min-width="150" sortable="custom" />
        <el-table-column prop="code" label="设备类型编码" width="120" />
        <el-table-column prop="manufacturer" label="制造商" width="120" />
        <el-table-column prop="model" label="型号" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status_display }}
            </el-tag>
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
    
    <!-- 设备类型表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '新增设备类型' : '编辑设备类型'"
      width="600px"
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
            <el-form-item label="设备类型名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入设备类型名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设备类型编码" prop="code">
              <el-input v-model="form.code" placeholder="请输入设备类型编码" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="设备类别" prop="category">
              <el-input v-model="form.category" placeholder="请输入设备类别" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="制造商" prop="manufacturer">
              <el-input v-model="form.manufacturer" placeholder="请输入制造商" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="型号" prop="model">
              <el-input v-model="form.model" placeholder="请输入型号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="活跃" value="active" />
                <el-option label="不活跃" value="inactive" />
                <el-option label="已归档" value="archived" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="设备类型描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入设备类型描述"
          />
        </el-form-item>
        
        <el-form-item label="技术规格" prop="specifications">
          <el-input
            v-model="form.specifications"
            type="textarea"
            :rows="3"
            placeholder="请输入技术规格"
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
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import {
  getEquipmentTypes,
  createEquipmentType,
  updateEquipmentType,
  deleteEquipmentType
} from '@/api/equipment'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const searchQuery = ref('')
const equipmentTypes = ref([])

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
  prop: 'created_at',
  order: 'ascending'
})

// 表单数据
const form = reactive({
  name: '',
  code: '',
  category: '',
  manufacturer: '',
  model: '',
  status: 'active',
  description: '',
  specifications: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入设备类型名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度应在2-100个字符', trigger: 'blur' }
  ],
  code: [
    { required: false, message: '请输入设备类型编码', trigger: 'blur' }
  ],
  category: [
    { required: false, message: '请输入设备类别', trigger: 'blur' }
  ],
  status: [
    { required: false, message: '请选择状态', trigger: 'change' }
  ]
}

// 获取状态标签类型
const getStatusType = (status) => {
  const statusMap = {
    active: 'success',
    inactive: 'warning',
    archived: 'info'
  }
  return statusMap[status] || ''
}

// 加载设备类型列表
const loadEquipmentTypes = async () => {
  try {
    loading.value = true
    
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchQuery.value
    }
    
    if (sort.prop) {
      params.ordering = sort.order === 'descending' ? `-${sort.prop}` : sort.prop
    }
    
    const response = await getEquipmentTypes(params)
    const types = response.results || response.data || []
    // 转换时间格式
    equipmentTypes.value = types.map(item => ({
      ...item,
      created_at: dayjs(item.created_at).format('YYYY-MM-DD HH:mm:ss')
    }))
    pagination.total = response.count || response.total || 0
  } catch (error) {
    ElMessage.error('加载设备类型列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  loadEquipmentTypes()
}

// 排序变化处理
const handleSortChange = ({ prop, order }) => {
  sort.prop = prop
  sort.order = order
  pagination.page = 1
  loadEquipmentTypes()
}

// 分页变化处理
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadEquipmentTypes()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadEquipmentTypes()
}

// 新增设备类型
const handleAdd = () => {
  dialogMode.value = 'add'
  currentId.value = null
  resetForm()
  dialogVisible.value = true
}

// 编辑设备类型
const handleEdit = (row) => {
  dialogMode.value = 'edit'
  currentId.value = row.id
  Object.assign(form, {
    name: row.name,
    code: row.code,
    category: row.category,
    manufacturer: row.manufacturer,
    model: row.model,
    status: row.status,
    description: row.description,
    specifications: row.specifications
  })
  dialogVisible.value = true
}

// 删除设备类型
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设备类型"${row.name}"吗？此操作不可恢复。`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteEquipmentType(row.id)
    ElMessage.success('删除成功')
    loadEquipmentTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 表单提交
const handleSubmit = async () => {
  try {
    submitLoading.value = true
    
    if (dialogMode.value === 'add') {
      await createEquipmentType(form)
      ElMessage.success('新增成功')
    } else {
      await updateEquipmentType(currentId.value, form)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    loadEquipmentTypes()
  } catch (error) {
    ElMessage.error(dialogMode.value === 'add' ? '新增失败' : '更新失败')
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    code: '',
    category: '',
    manufacturer: '',
    model: '',
    status: 'active',
    description: '',
    specifications: ''
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
    loadEquipmentTypes()
  }
})

onMounted(() => {
  loadEquipmentTypes()
})
</script>

<style scoped>
.equipment-types {
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