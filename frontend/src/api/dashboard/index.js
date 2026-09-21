import request from '../request'

const dashboardApi = {
  getOverview: () => {
    return request({
      url: '/api/dashboard/overview/',
      method: 'get'
    })
  },
  
  getEquipmentFailureDistribution: () => {
    return request({
      url: '/api/dashboard/equipment_failure_distribution/',
      method: 'get'
    })
  },
  
  getSeverityDistribution: () => {
    return request({
      url: '/api/dashboard/severity_distribution/',
      method: 'get'
    })
  },
  
  getRiskLevelDistribution: () => {
    return request({
      url: '/api/dashboard/risk_level_distribution/',
      method: 'get'
    })
  },
  
  getHazardTrend: (days = 30) => {
    return request({
      url: '/api/dashboard/hazard_trend/',
      method: 'get',
      params: { days }
    })
  },
  
  getTopRiskFailureModes: (limit = 10) => {
    return request({
      url: '/api/dashboard/top_risk_failure_modes/',
      method: 'get',
      params: { limit }
    })
  },
  
  getCompensationEffectiveness: () => {
    return request({
      url: '/api/dashboard/compensation_effectiveness/',
      method: 'get'
    })
  }
}

export default dashboardApi