import request from '../request'

// 故障模式危害度分析API
export const failureAnalysisApi = {
  // 危害度参数配置
  getParameters: (params) => {
    return request({
      url: '/api/failure-analysis/parameters/',
      method: 'get',
      params
    })
  },
  
  getActiveParameters: () => {
    return request({
      url: '/api/failure-analysis/parameters/active_parameters/',
      method: 'get'
    })
  },
  
  getParametersByType: (type) => {
    return request({
      url: '/api/failure-analysis/parameters/by_type/',
      method: 'get',
      params: { type }
    })
  },
  
  createParameter: (data) => {
    return request({
      url: '/api/failure-analysis/parameters/',
      method: 'post',
      data
    })
  },
  
  updateParameter: (id, data) => {
    return request({
      url: `/api/failure-analysis/parameters/${id}/`,
      method: 'put',
      data
    })
  },
  
  deleteParameter: (id) => {
    return request({
      url: `/api/failure-analysis/parameters/${id}/`,
      method: 'delete'
    })
  },
  
  // 故障模式危害度分析
  getAnalyses: (params) => {
    return request({
      url: '/api/failure-analysis/analyses/',
      method: 'get',
      params
    })
  },
  
  getAnalysis: (id) => {
    return request({
      url: `/api/failure-analysis/analyses/${id}/`,
      method: 'get'
    })
  },
  
  createAnalysis: (data) => {
    return request({
      url: '/api/failure-analysis/analyses/',
      method: 'post',
      data
    })
  },
  
  updateAnalysis: (id, data) => {
    return request({
      url: `/api/failure-analysis/analyses/${id}/`,
      method: 'put',
      data
    })
  },
  
  deleteAnalysis: (id) => {
    return request({
      url: `/api/failure-analysis/analyses/${id}/`,
      method: 'delete'
    })
  },
  
  getAnalysisStatistics: () => {
    return request({
      url: '/api/failure-analysis/analyses/statistics/',
      method: 'get'
    })
  },
  
  getTopRiskAnalyses: (limit) => {
    return request({
      url: '/api/failure-analysis/analyses/top_risk/',
      method: 'get',
      params: { limit }
    })
  }
}

export default failureAnalysisApi