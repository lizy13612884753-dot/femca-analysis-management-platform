import request from './request'

export function getUserSettings() {
  return request({
    url: '/api/users/settings/',
    method: 'get'
  })
}

export function updateUserSettings(data) {
  return request({
    url: '/api/users/settings/update_settings/',
    method: 'put',
    data
  })
}
