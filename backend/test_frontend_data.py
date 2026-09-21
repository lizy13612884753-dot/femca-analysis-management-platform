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

# 测试更新设备实例42，模拟前端可能发送的完整数据结构
def test_update_instance_42(token):
    url = 'http://localhost:8000/api/equipment/instances/42/'
    
    # 模拟前端可能发送的完整数据结构
    # 包括所有可能的字段，以及前端可能的格式
    payload = {
        "equipment_type": 38,
        "serial_number": "01",
        "name": "器身",
        "location": "",
        "install_date": ["2024-01-01"],  # 数组格式的日期
        "warranty_expire_date": ["2025-01-01"],  # 数组格式的日期
        "status": "maintenance",
        "custom_specifications": {},
        "function_description": "",
        "notes": ""
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

# 测试部分更新（PATCH请求）
def test_patch_instance_42(token):
    url = 'http://localhost:8000/api/equipment/instances/42/'
    
    # 模拟前端可能发送的部分更新数据
    payload = {
        "name": "更新后的器身",
        "install_date": ["2024-01-01"]  # 数组格式的日期
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print("\n测试部分更新设备实例42...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.patch(url, json=payload, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n测试成功！设备实例42部分更新成功")
            return True
        else:
            print("\n测试失败！设备实例42部分更新失败")
            return False
    except Exception as e:
        print(f"\n请求异常: {str(e)}")
        return False

# 主测试流程
def main():
    print("=== 前端数据模拟测试 ===")
    
    # 获取token
    token = login()
    if not token:
        print("无法获取认证token，测试终止")
        return
    
    print("登录成功，获取到token")
    
    # 测试完整更新
    print("\n=== 测试完整更新 ===")
    success1 = test_update_instance_42(token)
    
    # 测试部分更新
    print("\n=== 测试部分更新 ===")
    success2 = test_patch_instance_42(token)
    
    if success1 and success2:
        print("\n修复验证成功！设备实例更新功能正常")
    else:
        print("\n修复验证失败！设备实例更新功能仍然存在问题")

if __name__ == "__main__":
    main()
