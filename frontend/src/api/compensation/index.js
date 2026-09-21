import request from '@/api/request'

// 补偿措施相关API
export const getCompensationMeasures = (params) => {
  return request({
    url: '/api/compensation/measures/',
    method: 'get',
    params
  })
}

export const getCompensationMeasure = (id) => {
  return request({
    url: `/api/compensation/measures/${id}/`,
    method: 'get'
  })
}

export const createCompensationMeasure = (data) => {
  return request({
    url: '/api/compensation/measures/',
    method: 'post',
    data
  })
}

export const updateCompensationMeasure = (id, data) => {
  return request({
    url: `/api/compensation/measures/${id}/`,
    method: 'put',
    data
  })
}

export const deleteCompensationMeasure = (id) => {
  return request({
    url: `/api/compensation/measures/${id}/`,
    method: 'delete'
  })
}

export const searchCompensationMeasures = (params) => {
  return request({
    url: '/api/compensation/measures/search/',
    method: 'get',
    params
  })
}

export const getCompensationMeasuresByEquipmentType = (equipmentTypeId) => {
  return request({
    url: '/api/compensation/measures/by_equipment_type/',
    method: 'get',
    params: { equipment_type: equipmentTypeId }
  })
}

export const getCompensationMeasureEffectivenessAnalysis = (id) => {
  return request({
    url: `/api/compensation/measures/${id}/effectiveness_analysis/`,
    method: 'get'
  })
}

// 有效性评估相关API
export const getEffectivenessEvaluations = (params) => {
  return request({
    url: '/api/compensation/evaluations/',
    method: 'get',
    params
  })
}

export const getEffectivenessEvaluation = (id) => {
  return request({
    url: `/api/compensation/evaluations/${id}/`,
    method: 'get'
  })
}

export const createEffectivenessEvaluation = (data) => {
  return request({
    url: '/api/compensation/evaluations/',
    method: 'post',
    data
  })
}

export const updateEffectivenessEvaluation = (id, data) => {
  return request({
    url: `/api/compensation/evaluations/${id}/`,
    method: 'put',
    data
  })
}

export const deleteEffectivenessEvaluation = (id) => {
  return request({
    url: `/api/compensation/evaluations/${id}/`,
    method: 'delete'
  })
}

export const searchEffectivenessEvaluations = (params) => {
  return request({
    url: '/api/compensation/evaluations/search/',
    method: 'get',
    params
  })
}

export const getEffectivenessEvaluationsForCompensation = (compensationId) => {
  return request({
    url: '/api/compensation/evaluations/for_compensation/',
    method: 'get',
    params: { compensation_measure: compensationId }
  })
}

export const getRecentEvaluations = (days = 30) => {
  return request({
    url: '/api/compensation/evaluations/recent_evaluations/',
    method: 'get',
    params: { days }
  })
}

// 故障模式补偿关联相关API
export const getFailureModeCompensations = (params) => {
  return request({
    url: '/api/compensation/failure-mode/',
    method: 'get',
    params
  })
}

export const getFailureModeCompensation = (id) => {
  return request({
    url: `/api/compensation/failure-mode/${id}/`,
    method: 'get'
  })
}

export const createFailureModeCompensation = (data) => {
  return request({
    url: '/api/compensation/failure-mode/',
    method: 'post',
    data
  })
}

export const updateFailureModeCompensation = (id, data) => {
  return request({
    url: `/api/compensation/failure-mode/${id}/`,
    method: 'put',
    data
  })
}

export const deleteFailureModeCompensation = (id) => {
  return request({
    url: `/api/compensation/failure-mode/${id}/`,
    method: 'delete'
  })
}

export const searchFailureModeCompensations = (params) => {
  return request({
    url: '/api/compensation/failure-mode/search/',
    method: 'get',
    params
  })
}

export const getFailureModeCompensationEffectivenessAnalysis = (id) => {
  return request({
    url: `/api/compensation/failure-mode/${id}/effectiveness_analysis/`,
    method: 'get'
  })
}

export const updateCompensationRating = (id, rating) => {
  return request({
    url: `/api/compensation/failure-mode/${id}/update_rating/`,
    method: 'post',
    data: { effectiveness_rating: rating }
  })
}

export const getFailureModeCompensationsByFailureMode = (failureModeId) => {
  return request({
    url: '/api/compensation/failure-mode/for_failure_mode/',
    method: 'get',
    params: { failure_mode: failureModeId }
  })
}

export const getFailureModeCompensationsByCompensation = (compensationId) => {
  return request({
    url: '/api/compensation/failure-mode/for_compensation/',
    method: 'get',
    params: { compensation_measure: compensationId }
  })
}