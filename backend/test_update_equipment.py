import requests
import json

# 登录获取token
def login():
    login_url = 'http://localhost:8000/api/auth/login/'
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            data = response.json()
            return data.get('tokens', {}).get('access')
        else:
            print(f"登录失败: {response.status_code}")
            print(f"响应: {response.json()}")
            return None
    except Exception as e:
        print(f"登录异常: {str(e)}")
        return None

# 获取设备实例列表
def get_equipment_instances(token):
    url = 'http://localhost:8000/api/equipment/instances/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                print(f"找到 {len(data['results'])} 个设备实例")
                for instance in data['results'][:5]:  # 只显示前5个
                    print(f"ID: {instance['id']}, 名称: {instance['name']}, 序列号: {instance['serial_number']}")
                return data['results']
        return []
    except Exception as e:
        print(f"获取设备实例列表异常: {str(e)}")
        return []

# 更新设备实例
def update_equipment_instance(token, instance_id):
    url = f'http://localhost:8000/api/equipment/instances/{instance_id}/'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # 模拟前端发送的更新数据，包含数组格式的日期
    # 获取原始设备实例的信息，确保包含必填字段
    try:
        get_url = f'http://localhost:8000/api/equipment/instances/{instance_id}/'
        get_response = requests.get(get_url, headers=headers)
        if get_response.status_code == 200:
            original_data = get_response.json()
            payload = {
                "equipment_type": original_data['equipment_type'],
                "serial_number": original_data['serial_number'],
                "name": "更新后的测试设备",
                "location": "更新后的测试位置",
                "install_date": ["2024-01-02"],  # 数组格式的日期
                "warranty_expire_date": ["2025-01-02"],  # 数组格式的日期
                "status": "operational",
                "function_description": "更新后的测试功能描述"
            }
        else:
            print(f"获取设备实例信息失败: {get_response.status_code}")
            return False
    except Exception as e:
        print(f"获取设备实例信息异常: {str(e)}")
        return False
    
    print(f"\n测试更新设备实例 {instance_id}...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n测试成功！设备实例更新成功")
            return True
        else:
            print("\n测试失败！设备实例更新失败")
            return False
    except Exception as e:
        print(f"\n请求异常: {str(e)}")
        return False

# 主测试流程
def main():
    print("=== 设备实例更新测试 ===")
    
    # 获取token
    token = login()
    if not token:
        print("无法获取认证token，测试终止")
        return
    
    print("登录成功，获取到token")
    
    # 获取设备实例列表
    instances = get_equipment_instances(token)
    if not instances:
        print("没有找到设备实例，测试终止")
        return
    
    # 选择第一个设备实例进行更新
    instance_id = instances[0]['id']
    print(f"\n选择设备实例 {instance_id} 进行更新测试")
    
    # 更新设备实例
    success = update_equipment_instance(token, instance_id)
    if success:
        print("\n✓ 修复验证成功！设备实例更新功能正常")
    else:
        print("\n✗ 修复验证失败！设备实例更新功能仍然存在问题")

if __name__ == "__main__":
    main()
