import request from '@/api/request'

// 检测方法相关API
export const getDetectionMethods = (params) => {
  return request({
    url: '/api/detection/methods/',
    method: 'get',
    params
  })
}

export const getDetectionMethod = (id) => {
  return request({
    url: `/api/detection/methods/${id}/`,
    method: 'get'
  })
}

export const createDetectionMethod = (data) => {
  return request({
    url: '/api/detection/methods/',
    method: 'post',
    data
  })
}

export const updateDetectionMethod = (id, data) => {
  return request({
    url: `/api/detection/methods/${id}/`,
    method: 'put',
    data
  })
}

export const deleteDetectionMethod = (id) => {
  return request({
    url: `/api/detection/methods/${id}/`,
    method: 'delete'
  })
}

export const searchDetectionMethods = (params) => {
  return request({
    url: '/api/detection/methods/search/',
    method: 'get',
    params
  })
}

export const getDetectionMethodsByEquipmentType = (equipmentTypeId) => {
  return request({
    url: '/api/detection/methods/by_equipment_type/',
    method: 'get',
    params: { equipment_type: equipmentTypeId }
  })
}

// 检测评级相关API
export const getDetectionRatings = (params) => {
  return request({
    url: '/api/detection/ratings/',
    method: 'get',
    params
  })
}

export const getDetectionRating = (id) => {
  return request({
    url: `/api/detection/ratings/${id}/`,
    method: 'get'
  })
}

export const createDetectionRating = (data) => {
  return request({
    url: '/api/detection/ratings/',
    method: 'post',
    data
  })
}

export const updateDetectionRating = (id, data) => {
  return request({
    url: `/api/detection/ratings/${id}/`,
    method: 'put',
    data
  })
}

export const deleteDetectionRating = (id) => {
  return request({
    url: `/api/detection/ratings/${id}/`,
    method: 'delete'
  })
}

export const getActiveDetectionRatings = () => {
  return request({
    url: '/api/detection/ratings/active/',
    method: 'get'
  })
}

// 故障模式检测关联相关API
export const getFailureModeDetections = (params) => {
  return request({
    url: '/api/detection/failure-mode/',
    method: 'get',
    params
  })
}

export const getFailureModeDetection = (id) => {
  return request({
    url: `/api/detection/failure-mode/${id}/`,
    method: 'get'
  })
}

export const createFailureModeDetection = (data) => {
  return request({
    url: '/api/detection/failure-mode/',
    method: 'post',
    data
  })
}

export const updateFailureModeDetection = (id, data) => {
  return request({
    url: `/api/detection/failure-mode/${id}/`,
    method: 'put',
    data
  })
}

export const deleteFailureModeDetection = (id) => {
  return request({
    url: `/api/detection/failure-mode/${id}/`,
    method: 'delete'
  })
}

export const searchFailureModeDetections = (params) => {
  return request({
    url: '/api/detection/failure-mode/search/',
    method: 'get',
    params
  })
}

export const getDetectionAnalysis = (id) => {
  return request({
    url: `/api/detection/failure-mode/${id}/detection_analysis/`,
    method: 'get'
  })
}

export const updateFailureModeDetectionRating = (id, ratingId) => {
  return request({
    url: `/api/detection/failure-mode/${id}/update_rating/`,
    method: 'post',
    data: { detection_rating: ratingId }
  })
}

export const getFailureModeDetectionsByFailureMode = (failureModeId) => {
  return request({
    url: '/api/detection/failure-mode/for_failure_mode/',
    method: 'get',
    params: { failure_mode: failureModeId }
  })
}