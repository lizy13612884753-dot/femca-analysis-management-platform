import requests
import json

# 登录获取token
def login():
    login_url = 'http://localhost:8000/api/auth/login/'
    login_data = {
        "username": "admin",  # 假设存在admin用户
        "password": "admin123"  # 假设密码是admin123
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

# 获取token
token = login()
if not token:
    print("无法获取认证token，测试终止")
    exit(1)

print("登录成功，获取到token")

# 测试设备实例创建
url = 'http://localhost:8000/api/equipment/instances/'

# 模拟前端发送的请求数据，包含数组格式的日期
payload = {
    "equipment_type": 1,  # 假设存在ID为1的设备类型
    "serial_number": "TEST001",
    "name": "测试设备",
    "location": "测试位置",
    "install_date": ["2024-01-01"],  # 数组格式的日期
    "warranty_expire_date": ["2025-01-01"],  # 数组格式的日期
    "status": "operational",
    "function_description": "测试功能描述"
}

# 添加认证头
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
    else:
        print("\n测试失败！设备实例创建失败")
        
except Exception as e:
    print(f"\n请求异常: {str(e)}")
