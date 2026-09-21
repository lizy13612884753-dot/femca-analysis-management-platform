import request from './request'

// 登录
export const login = (data) => {
  return request({
    url: '/api/auth/login/',
    method: 'post',
    data
  })
}

// 登出
export const logout = () => {
  return request({
    url: '/api/auth/logout/',
    method: 'post'
  })
}

// 获取用户信息
export const getUserInfo = () => {
  return request({
    url: '/api/auth/user/info/',
    method: 'get'
  })
}

// 刷新Token
export const refreshToken = (data) => {
  return request({
    url: '/api/auth/token/refresh/',
    method: 'post',
    data
  })
}

// 用户注册
export const register = (data) => {
  return request({
    url: '/api/auth/register/',
    method: 'post',
    data
  })
}

// 修改密码
export const changePassword = (data) => {
  return request({
    url: '/api/auth/change-password/',
    method: 'post',
    data
  })
}

// 重置密码
export const resetPassword = (data) => {
  return request({
    url: '/api/auth/reset-password/',
    method: 'post',
    data
  })
}