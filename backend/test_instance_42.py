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

# 获取设备实例42的信息
def get_instance_42(token):
    url = 'http://localhost:8000/api/equipment/instances/42/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("设备实例42的信息:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return data
        else:
            print(f"获取设备实例42失败: {response.status_code}")
            print(f"响应: {response.json()}")
            return None
    except Exception as e:
        print(f"获取设备实例42异常: {str(e)}")
        return None

# 测试更新设备实例42
def update_instance_42(token, instance_data):
    url = 'http://localhost:8000/api/equipment/instances/42/'
    
    # 模拟前端发送的更新数据，包含数组格式的日期
    payload = {
        "equipment_type": instance_data['equipment_type'],
        "serial_number": instance_data['serial_number'],
        "name": instance_data['name'],
        "location": instance_data['location'],
        "install_date": ["2024-01-01"],  # 数组格式的日期
        "warranty_expire_date": ["2025-01-01"],  # 数组格式的日期
        "status": instance_data['status'],
        "function_description": instance_data.get('function_description', '')
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print("\n测试更新设备实例42...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n测试成功！设备实例42更新成功")
            return True
        else:
            print("\n测试失败！设备实例42更新失败")
            return False
    except Exception as e:
        print(f"\n请求异常: {str(e)}")
        return False

# 主测试流程
def main():
    print("=== 设备实例42更新测试 ===")
    
    # 获取token
    token = login()
    if not token:
        print("无法获取认证token，测试终止")
        return
    
    print("登录成功，获取到token")
    
    # 获取设备实例42的信息
    instance_data = get_instance_42(token)
    if not instance_data:
        print("无法获取设备实例42的信息，测试终止")
        return
    
    # 更新设备实例42
    success = update_instance_42(token, instance_data)
    if success:
        print("\n修复验证成功！设备实例42更新功能正常")
    else:
        print("\n修复验证失败！设备实例42更新功能仍然存在问题")

if __name__ == "__main__":
    main()
