<template>
  <div class="detection-ratings">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>检测评级管理</h1>
      <p>管理检测方法的有效性等级和RPN分数</p>
    </div>
    
    <!-- 操作栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增检测评级
        </el-button>
      </div>
    </div>
    
    <!-- 检测评级表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="detectionRatings"
        style="width: 100%"
        stripe
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column prop="rating" label="评级" width="100" sortable="custom">
          <template #default="{ row }">
            <el-tag :type="getRatingColor(row.rating)" size="large">
              {{ row.rating }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="等级名称" width="150" sortable="custom" />
        <el-table-column prop="description" label="等级描述" min-width="200" />
        <el-table-column prop="rpn_score" label="RPN分数" width="120" sortable="custom" />
        <el-table-column prop="detection_time" label="检测时间(分钟)" width="140" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
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
    
    <!-- 检测评级表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '新增检测评级' : '编辑检测评级'"
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
            <el-form-item label="评级" prop="rating">
              <el-select v-model="form.rating" placeholder="请选择评级" @change="handleRatingChange">
                <el-option
                  v-for="rating in ratingOptions"
                  :key="rating.value"
                  :label="rating.label"
                  :value="rating.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="等级名称" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="等级描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="RPN分数" prop="rpn_score">
              <el-input-number v-model="form.rpn_score" :min="1" :max="10" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="检测时间(分钟)" prop="detection_time">
              <el-input-number v-model="form.detection_time" :min="0" :step="5" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import {
  getDetectionRatings,
  createDetectionRating,
  updateDetectionRating,
  deleteDetectionRating
} from '@/api/detection'

// 响应式数据
const loading = ref(false)
const detectionRatings = ref([])
const dialogVisible = ref(false)
const submitLoading = ref(false)
const dialogMode = ref('add') // add, edit
const formRef = ref(null)
const form = reactive({
  rating: '',
  name: '',
  description: '',
  rpn_score: 1,
  detection_time: 0,
  is_active: true
})

// 评级选项
const ratingOptions = [
  { value: 'A', label: 'A - 几乎确定' },
  { value: 'B', label: 'B - 非常高' },
  { value: 'C', label: 'C - 高' },
  { value: 'D', label: 'D - 中等' },
  { value: 'E', label: 'E - 低' },
  { value: 'F', label: 'F - 非常低' },
  { value: 'G', label: 'G - 几乎不可能' }
]

// RPN分数映射
const rpnScoreMap = {
  A: 1,
  B: 2,
  C: 3,
  D: 4,
  E: 5,
  F: 8,
  G: 10
}

// 表单验证规则
const formRules = {
  rating: [
    { required: true, message: '请选择评级', trigger: 'change' }
  ],
  name: [
    { required: true, message: '请输入等级名称', trigger: 'blur' }
  ],
  rpn_score: [
    { required: true, message: '请输入RPN分数', trigger: 'blur' }
  ]
}

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 排序
const sortField = ref('')
const sortOrder = ref('')

// 获取检测评级
const fetchDetectionRatings = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    
    if (sortField.value) {
      params.ordering = sortOrder.value === 'ascending' ? sortField.value : `-${sortField.value}`
    }
    
    const response = await getDetectionRatings(params)
    if (response) {
      detectionRatings.value = response.results || []
      pagination.total = response.count || 0
    }
  } catch (error) {
    console.error('获取检测评级失败:', error)
    ElMessage.error('获取检测评级失败')
  } finally {
    loading.value = false
  }
}

// 处理排序
const handleSortChange = ({ prop, order }) => {
  sortField.value = prop
  sortOrder.value = order
  fetchDetectionRatings()
}

// 处理分页
const handleSizeChange = (val) => {
  pagination.pageSize = val
  pagination.page = 1
  fetchDetectionRatings()
}

const handleCurrentChange = (val) => {
  pagination.page = val
  fetchDetectionRatings()
}

// 打开添加对话框
const handleAdd = () => {
  dialogMode.value = 'add'
  Object.assign(form, {
    rating: '',
    name: '',
    description: '',
    rpn_score: 1,
    detection_time: 0,
    is_active: true
  })
  dialogVisible.value = true
}

// 打开编辑对话框
const handleEdit = (row) => {
  dialogMode.value = 'edit'
  Object.assign(form, {
    id: row.id,
    rating: row.rating,
    name: row.name,
    description: row.description,
    rpn_score: row.rpn_score,
    detection_time: row.detection_time,
    is_active: row.is_active
  })
  dialogVisible.value = true
}

// 关闭对话框
const handleDialogClose = () => {
  formRef.value?.resetFields()
}

// 处理评级变化
const handleRatingChange = (rating) => {
  // 自动设置RPN分数
  if (rpnScoreMap[rating]) {
    form.rpn_score = rpnScoreMap[rating]
  }
  
  // 自动设置等级名称
  const ratingOption = ratingOptions.find(option => option.value === rating)
  if (ratingOption && !form.name) {
    form.name = ratingOption.label.split(' - ')[1]
  }
}

// 提交表单
const handleSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (dialogMode.value === 'add') {
          await createDetectionRating(form)
          ElMessage.success('添加成功')
        } else if (dialogMode.value === 'edit') {
          await updateDetectionRating(form.id, form)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        fetchDetectionRatings()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 删除检测评级
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除检测评级"${row.rating}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteDetectionRating(row.id)
    ElMessage.success('删除成功')
    fetchDetectionRatings()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 获取评级颜色
const getRatingColor = (rating) => {
  const colorMap = {
    A: 'success',
    B: 'success',
    C: 'primary',
    D: 'primary',
    E: 'warning',
    F: 'danger',
    G: 'danger'
  }
  return colorMap[rating] || ''
}

// 初始化
onMounted(() => {
  fetchDetectionRatings()
})
</script>

<style scoped>
.detection-ratings {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 22px;
  margin-bottom: 5px;
}

.page-header p {
  color: #666;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
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
}
</style>