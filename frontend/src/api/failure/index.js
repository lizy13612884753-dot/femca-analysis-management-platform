import request from '@/api/request'

// 故障模式相关API

// 获取故障模式列表
export const getFailureModes = (params) => {
  return request({
    url: '/api/failure/modes/',
    method: 'get',
    params
  })
}

// 获取故障模式详情
export const getFailureMode = (id) => {
  return request({
    url: `/api/failure/modes/${id}/`,
    method: 'get'
  })
}

// 创建故障模式
export const createFailureMode = (data) => {
  return request({
    url: '/api/failure/modes/',
    method: 'post',
    data
  })
}

// 更新故障模式
export const updateFailureMode = (id, data) => {
  return request({
    url: `/api/failure/modes/${id}/`,
    method: 'put',
    data
  })
}

// 删除故障模式
export const deleteFailureMode = (id) => {
  return request({
    url: `/api/failure/modes/${id}/`,
    method: 'delete'
  })
}

// 搜索故障模式
export const searchFailureModes = (params) => {
  return request({
    url: '/api/failure/modes/search/',
    method: 'get',
    params
  })
}

// 获取故障原因列表
export const getFailureCauses = (params) => {
  return request({
    url: '/api/failure/causes/',
    method: 'get',
    params
  })
}

// 获取故障影响列表
export const getFailureEffects = (params) => {
  return request({
    url: '/api/failure/effects/',
    method: 'get',
    params
  })
}
