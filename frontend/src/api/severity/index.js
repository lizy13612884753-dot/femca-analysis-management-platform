import request from '../request'

// 获取严酷度等级列表
export const getSeverityLevels = (params) => {
  return request({
    url: '/api/severity/levels/',
    method: 'get',
    params
  })
}

// 创建严酷度等级
export const createSeverityLevel = (data) => {
  return request({
    url: '/api/severity/levels/',
    method: 'post',
    data
  })
}

// 获取严酷度等级详情
export const getSeverityLevelDetail = (id) => {
  return request({
    url: `/api/severity/levels/${id}/`,
    method: 'get'
  })
}

// 更新严酷度等级
export const updateSeverityLevel = (id, data) => {
  return request({
    url: `/api/severity/levels/${id}/`,
    method: 'put',
    data
  })
}

// 删除严酷度等级
export const deleteSeverityLevel = (id) => {
  return request({
    url: `/api/severity/levels/${id}/`,
    method: 'delete'
  })
}

// 获取严酷度指标列表
export const getSeverityIndicators = (params) => {
  return request({
    url: '/api/severity/indicators/',
    method: 'get',
    params
  })
}

// 创建严酷度指标
export const createSeverityIndicator = (data) => {
  return request({
    url: '/api/severity/indicators/',
    method: 'post',
    data
  })
}

// 获取严酷度指标详情
export const getSeverityIndicatorDetail = (id) => {
  return request({
    url: `/api/severity/indicators/${id}/`,
    method: 'get'
  })
}

// 更新严酷度指标
export const updateSeverityIndicator = (id, data) => {
  return request({
    url: `/api/severity/indicators/${id}/`,
    method: 'put',
    data
  })
}

// 删除严酷度指标
export const deleteSeverityIndicator = (id) => {
  return request({
    url: `/api/severity/indicators/${id}/`,
    method: 'delete'
  })
}

// 获取严酷度评定列表
export const getSeverityAssessments = (params) => {
  return request({
    url: '/api/severity/assessments/',
    method: 'get',
    params
  })
}

// 创建严酷度评定
export const createSeverityAssessment = (data) => {
  return request({
    url: '/api/severity/assessments/',
    method: 'post',
    data
  })
}

// 更新严酷度评定
export const updateSeverityAssessment = (id, data) => {
  return request({
    url: `/api/severity/assessments/${id}/`,
    method: 'put',
    data
  })
}

// 删除严酷度评定
export const deleteSeverityAssessment = (id) => {
  return request({
    url: `/api/severity/assessments/${id}/`,
    method: 'delete'
  })
}
