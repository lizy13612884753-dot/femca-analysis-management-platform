import request from '../request'

// 产品危害度分析API
export const productAnalysisApi = {
  // 产品危害度分析
  getAnalyses: (params) => {
    return request({
      url: '/api/product-analysis/analyses/',
      method: 'get',
      params
    })
  },
  
  getAnalysis: (id) => {
    return request({
      url: `/api/product-analysis/analyses/${id}/`,
      method: 'get'
    })
  },
  
  createAnalysis: (data) => {
    return request({
      url: '/api/product-analysis/analyses/',
      method: 'post',
      data
    })
  },
  
  updateAnalysis: (id, data) => {
    return request({
      url: `/api/product-analysis/analyses/${id}/`,
      method: 'put',
      data
    })
  },
  
  deleteAnalysis: (id) => {
    return request({
      url: `/api/product-analysis/analyses/${id}/`,
      method: 'delete'
    })
  },
  
  getAnalysisByEquipment: (equipmentId) => {
    return request({
      url: '/api/product-analysis/analyses/by_equipment/',
      method: 'get',
      params: { equipment_type: equipmentId }
    })
  },
  
  getLatestAnalysis: (equipmentId) => {
    return request({
      url: '/api/product-analysis/analyses/latest_analysis/',
      method: 'get',
      params: equipmentId ? { equipment_type: equipmentId } : {}
    })
  },
  
  recalculateAnalysis: (id) => {
    return request({
      url: `/api/product-analysis/analyses/${id}/recalculate/`,
      method: 'post'
    })
  },
  
  getAnalysisStatistics: () => {
    return request({
      url: '/api/product-analysis/analyses/statistics/',
      method: 'get'
    })
  },
  
  getOverallSummary: () => {
    return request({
      url: '/api/product-analysis/analyses/overall_summary/',
      method: 'get'
    })
  }
}

export default productAnalysisApi