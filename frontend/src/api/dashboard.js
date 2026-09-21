import request from './request'

export function getDashboardOverview() {
  return request({
    url: '/api/dashboard/overview/',
    method: 'get'
  })
}

export function getEquipmentFailureDistribution() {
  return request({
    url: '/api/dashboard/equipment_failure_distribution/',
    method: 'get'
  })
}

export function getSeverityDistribution() {
  return request({
    url: '/api/dashboard/severity_distribution/',
    method: 'get'
  })
}

export function getRiskLevelDistribution() {
  return request({
    url: '/api/dashboard/risk_level_distribution/',
    method: 'get'
  })
}

export function getHazardTrend(params) {
  let url = '/api/dashboard/hazard_trend/'
  if (params) {
    const searchParams = new URLSearchParams()
    Object.keys(params).forEach(key => {
      searchParams.append(key, params[key])
    })
    url += '?' + searchParams.toString()
  }
  return request({
    url: url,
    method: 'get'
  })
}

export function getTopRiskFailureModes(params) {
  let url = '/api/dashboard/top_risk_failure_modes/'
  if (params) {
    const searchParams = new URLSearchParams()
    Object.keys(params).forEach(key => {
      searchParams.append(key, params[key])
    })
    url += '?' + searchParams.toString()
  }
  return request({
    url: url,
    method: 'get'
  })
}

export function getCompensationEffectiveness() {
  return request({
    url: '/api/dashboard/compensation_effectiveness/',
    method: 'get'
  })
}
