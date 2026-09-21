import request from '@/api/request'

// 设备类型相关API
export const getEquipmentTypes = (params) => {
  return request({
    url: '/api/equipment/types/',
    method: 'get',
    params
  })
}

export const createEquipmentType = (data) => {
  return request({
    url: '/api/equipment/types/',
    method: 'post',
    data
  })
}

export const updateEquipmentType = (id, data) => {
  return request({
    url: `/api/equipment/types/${id}/`,
    method: 'put',
    data
  })
}

export const deleteEquipmentType = (id) => {
  return request({
    url: `/api/equipment/types/${id}/`,
    method: 'delete'
  })
}

// 设备实例相关API
export const getEquipmentInstances = (params) => {
  return request({
    url: '/api/equipment/instances/',
    method: 'get',
    params
  })
}

export const createEquipmentInstance = (data) => {
  console.log('创建设备实例请求数据:', data);
  return request({
    url: '/api/equipment/instances/',
    method: 'post',
    data
  }).catch(error => {
    console.log('创建设备实例错误:', error.response?.data || error.message);
    throw error;
  });
}

export const updateEquipmentInstance = (id, data) => {
  console.log('API调用：更新设备实例', id);
  console.log('更新数据包含function_description:', 'function_description' in data);
  console.log('更新数据中的function_description值:', data.function_description);
  return request({
    url: `/api/equipment/instances/${id}/`,
    method: 'put',
    data
  })
}

export const deleteEquipmentInstance = (id) => {
  return request({
    url: `/api/equipment/instances/${id}/`,
    method: 'delete'
  })
}
