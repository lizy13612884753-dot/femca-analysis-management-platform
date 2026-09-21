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

# 获取设备类型
def get_equipment_type(token):
    url = 'http://localhost:8000/api/equipment/types/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                equipment_type = data['results'][0]
                print(f"使用设备类型: ID={equipment_type['id']}, 名称={equipment_type['name']}")
                return equipment_type['id']
        return None
    except Exception as e:
        print(f"获取设备类型异常: {str(e)}")
        return None

# 模拟前端创建设备实例
def create_equipment_instance(token, equipment_type_id):
    url = 'http://localhost:8000/api/equipment/instances/'
    
    # 模拟前端发送的完整数据结构
    import time
    unique_serial = f"TEST{int(time.time())}"
    
    # 模拟前端可能发送的数据结构，包括所有可能的字段
    payload = {
        "equipment_type": equipment_type_id,
        "serial_number": unique_serial,
        "name": "测试设备",
        "location": "测试位置",
        "install_date": ["2024-01-01"],  # 数组格式的日期
        "warranty_expire_date": ["2025-01-01"],  # 数组格式的日期
        "status": "operational",
        "custom_specifications": {},
        "function_description": "测试功能描述",
        "notes": ""
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print("\n测试设备实例创建请求...")
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            print("\n测试成功！设备实例创建成功")
            return True
        else:
            print("\n测试失败！设备实例创建失败")
            return False
    except Exception as e:
        print(f"\n请求异常: {str(e)}")
        return False

# 主测试流程
def main():
    print("=== 前端请求模拟测试 ===")
    
    # 获取token
    token = login()
    if not token:
        print("无法获取认证token，测试终止")
        return
    
    print("登录成功，获取到token")
    
    # 获取设备类型
    equipment_type_id = get_equipment_type(token)
    if not equipment_type_id:
        print("无法获取设备类型，测试终止")
        return
    
    # 创建设备实例
    success = create_equipment_instance(token, equipment_type_id)
    if success:
        print("\n✓ 修复验证成功！设备实例创建功能正常")
    else:
        print("\n✗ 修复验证失败！设备实例创建功能仍然存在问题")

if __name__ == "__main__":
    main()
