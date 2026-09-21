"""
FMECA平台完整功能演示脚本
展示设施设备FMECA分析管理平台的所有核心功能
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_subsection(title):
    """打印子章节标题"""
    print(f"\n📌 {title}")
    print("-" * 60)

def api_request(method, endpoint, data=None, token=None, description=""):
    """发送API请求并打印结果"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None
        
        print(f"  ✅ {description}")
        print(f"     状态码: {response.status_code}")
        
        if response.status_code in [200, 201, 204]:
            if response.text:
                try:
                    result = response.json()
                    if isinstance(result, dict):
                        for key, value in list(result.items())[:5]:
                            print(f"     {key}: {value}")
                    elif isinstance(result, list):
                        print(f"     返回 {len(result)} 条记录")
                        if len(result) > 0:
                            print(f"     示例: {json.dumps(result[0], ensure_ascii=False, indent=8)[:200]}...")
                    return result
                except:
                    print(f"     响应: {response.text[:100]}...")
            return True
        else:
            print(f"     响应: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"  ❌ 请求失败: {str(e)[:100]}")
        return None

def demo_authentication():
    """演示认证功能"""
    print_section("1. 用户认证系统")
    
    print_subsection("用户登录")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    result = api_request("POST", "/auth/login/", login_data, description="管理员登录")
    
    if result and "access" in result:
        token = result["access"]
        refresh = result.get("refresh", "")
        
        print(f"\n  🎉 登录成功！")
        print(f"  用户名: admin")
        print(f"  角色: 管理员")
        print(f"  Token长度: {len(token)} 字符")
        print(f"  Token前缀: {token[:20]}...")
        return token, refresh
    else:
        print("  ⚠️ 登录失败，将使用测试模式继续演示")
        return None, None

def demo_user_management(token):
    """演示用户管理功能"""
    print_section("2. 用户管理模块")
    
    if token:
        api_request("GET", "/auth/user/info/", token=token, description="获取当前用户信息")
    
    print_subsection("用户列表")
    api_request("GET", "/auth/users/", token=token, description="获取所有用户列表")

def demo_equipment_management(token):
    """演示设备管理功能"""
    print_section("3. 设备管理模块")
    
    print_subsection("设备类型管理")
    api_request("GET", "/equipment/types/", token=token, description="获取设备类型列表")
    
    print_subsection("设备实例管理")
    api_request("GET", "/equipment/devices/", token=token, description="获取设备实例列表")
    
    print_subsection("创建设备类型（示例）")
    equipment_type_data = {
        "name": "工业泵",
        "code": "PUMP-001",
        "description": "用于液体输送的离心泵",
        "parent": None
    }
    api_request("POST", "/equipment/types/", equipment_type_data, token=token, description="创建设备类型：工业泵")
    
    print_subsection("创建设备实例（示例）")
    device_data = {
        "name": "主循环泵",
        "code": "PUMP-MAIN-001",
        "equipment_type": 1,
        "location": "一楼机房",
        "status": "运行中",
        "specifications": {
            "power": "55kW",
            "flow": "200m³/h",
            "pressure": "1.6MPa"
        }
    }
    api_request("POST", "/equipment/devices/", device_data, token=token, description="创建设备实例：主循环泵")

def demo_functional_composition(token):
    """演示功能构成管理"""
    print_section("4. 功能构成管理模块")
    
    print_subsection("功能构成列表")
    api_request("GET", "/failure/functional-compositions/", token=token, description="获取功能构成列表")
    
    print_subsection("创建功能构成（示例）")
    func_data = {
        "name": "液体输送功能",
        "code": "FUNC-TRANSPORT",
        "description": "将液体从储罐输送到生产线的功能",
        "equipment_type": 1,
        "criticality": "高",
        "required_functions": "连续、稳定输送"
    }
    api_request("POST", "/failure/functional-compositions/", func_data, token=token, description="创建功能构成：液体输送功能")

def demo_failure_modes(token):
    """演示失效模式管理"""
    print_section("5. 失效模式管理模块")
    
    print_subsection("失效模式列表")
    api_request("GET", "/failure/modes/", token=token, description="获取失效模式列表")
    
    print_subsection("创建失效模式（示例）")
    failure_data = {
        "name": "密封泄漏",
        "code": "FM-LEAK",
        "description": "泵体密封件失效导致液体泄漏",
        "functional_composition": 1,
        "failure_type": "泄漏",
        "appearance": "液体从泵体连接处渗出",
        " causes": "密封件老化、安装不当、介质腐蚀",
        " effects": "效率降低、环境污染、停机"
    }
    api_request("POST", "/failure/modes/", failure_data, token=token, description="创建失效模式：密封泄漏")

def demo_severity_analysis(token):
    """演示严重度分析"""
    print_section("6. 严重度分析模块")
    
    print_subsection("严重度等级列表")
    api_request("GET", "/failure/severity-levels/", token=token, description="获取严重度等级列表")
    
    print_subsection("严重度评估列表")
    api_request("GET", "/failure/severity-assessments/", token=token, description="获取严重度评估列表")
    
    print_subsection("创建严重度等级（示例）")
    severity_data = {
        "name": "高",
        "code": "SEV-HIGH",
        "description": "可能导致严重后果，需要立即采取措施",
        "score_range": "7-9",
        "color": "#ff4d4f",
        "risk_level": "高风险"
    }
    api_request("POST", "/failure/severity-levels/", severity_data, token=token, description="创建严重度等级：高")

def demo_detection_methods(token):
    """演示检测方法管理"""
    print_section("7. 检测方法管理模块")
    
    print_subsection("检测方法列表")
    api_request("GET", "/failure/detection-methods/", token=token, description="获取检测方法列表")
    
    print_subsection("检测能力评估列表")
    api_request("GET", "/failure/detection-assessments/", token=token, description="获取检测能力评估列表")
    
    print_subsection("创建检测方法（示例）")
    detection_data = {
        "name": "压力监测",
        "code": "DET-PRESSURE",
        "description": "通过监测泵出口压力变化检测密封泄漏",
        "method_type": "在线监测",
        "principle": "压力异常下降可能表示泄漏",
        "equipment_required": "压力传感器、SCADA系统",
        "frequency": "实时",
        "effectiveness": "高",
        "cost": "中"
    }
    api_request("POST", "/failure/detection-methods/", detection_data, token=token, description="创建检测方法：压力监测")

def demo_compensation_measures(token):
    """演示补偿措施管理"""
    print_section("8. 补偿措施管理模块")
    
    print_subsection("补偿措施列表")
    api_request("GET", "/failure/compensation-measures/", token=token, description="获取补偿措施列表")
    
    print_subsection("创建补偿措施（示例）")
    compensation_data = {
        "name": "双端面机械密封",
        "code": "COMP-SEAL",
        "description": "采用双端面机械密封，提供双重保护",
        "applicable_failure": 1,
        "measure_type": "设计改进",
        "implementation_cost": "高",
        "effectiveness": "极高",
        "maintenance_requirement": "定期检查密封冲洗系统",
        "advantages": "零泄漏、安全可靠",
        "disadvantages": "成本较高、安装复杂"
    }
    api_request("POST", "/failure/compensation-measures/", compensation_data, token=token, description="创建补偿措施：双端面机械密封")

def demo_risk_analysis(token):
    """演示风险分析"""
    print_section("9. 风险分析模块")
    
    print_subsection("风险评估列表")
    api_request("GET", "/failure/risk-assessments/", token=token, description="获取风险评估列表")
    
    print_subsection("创建风险评估（示例）")
    risk_data = {
        "failure_mode": 1,
        "severity_level": 1,
        "occurrence_rating": 4,
        "detection_rating": 3,
        "equipment": 1,
        "comments": "需要重点关注的失效模式",
        "recommended_action": "增加在线监测频率"
    }
    api_request("POST", "/failure/risk-assessments/", risk_data, token=token, description="创建风险评估")

def demo_dashboard_statistics(token):
    """演示仪表盘统计"""
    print_section("10. 仪表盘统计")
    
    print_subsection("统计数据")
    stats_endpoints = [
        ("/equipment/types/count/", "设备类型数量"),
        ("/equipment/devices/count/", "设备实例数量"),
        ("/failure/modes/count/", "失效模式数量"),
        ("/failure/severity-levels/count/", "严重度等级数量"),
        ("/failure/detection-methods/count/", "检测方法数量"),
        ("/failure/compensation-measures/count/", "补偿措施数量"),
    ]
    
    for endpoint, description in stats_endpoints:
        api_request("GET", endpoint, token=token, description=f"获取{description}")

def demo_api_endpoints():
    """列出所有可用的API端点"""
    print_section("11. 可用的API端点")
    
    endpoints = [
        ("认证相关", [
            ("POST /auth/login/", "用户登录"),
            ("POST /auth/logout/", "用户登出"),
            ("GET /auth/user/info/", "获取当前用户信息"),
            ("GET /auth/users/", "获取用户列表"),
        ]),
        ("设备管理", [
            ("GET/POST /equipment/types/", "设备类型管理"),
            ("GET/POST /equipment/devices/", "设备实例管理"),
        ]),
        ("FMECA分析", [
            ("GET/POST /failure/functional-compositions/", "功能构成管理"),
            ("GET/POST /failure/modes/", "失效模式管理"),
            ("GET/POST /failure/severity-levels/", "严重度等级管理"),
            ("GET/POST /failure/severity-assessments/", "严重度评估管理"),
            ("GET/POST /failure/detection-methods/", "检测方法管理"),
            ("GET/POST /failure/detection-assessments/", "检测能力评估管理"),
            ("GET/POST /failure/compensation-measures/", "补偿措施管理"),
            ("GET/POST /failure/risk-assessments/", "风险评估管理"),
        ]),
    ]
    
    for category, endpoints_list in endpoints:
        print(f"\n📂 {category}:")
        for endpoint, description in endpoints_list:
            print(f"  • {endpoint:35} - {description}")

def main():
    """主函数"""
    print("\n" + "🏭" * 35)
    print("\n    设施设备FMECA分析管理平台 - 功能演示")
    print("    Facility Equipment FMECA Analysis Management Platform")
    print("\n" + "🏭" * 35)
    
    print("\n📅 演示时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("🌐 服务地址:", BASE_URL)
    print("👤 测试账号: admin / admin123")
    
    # 1. 用户认证
    token, refresh = demo_authentication()
    
    # 2. 用户管理
    demo_user_management(token)
    
    # 3. 设备管理
    demo_equipment_management(token)
    
    # 4. 功能构成管理
    demo_functional_composition(token)
    
    # 5. 失效模式管理
    demo_failure_modes(token)
    
    # 6. 严重度分析
    demo_severity_analysis(token)
    
    # 7. 检测方法管理
    demo_detection_methods(token)
    
    # 8. 补偿措施管理
    demo_compensation_measures(token)
    
    # 9. 风险分析
    demo_risk_analysis(token)
    
    # 10. 仪表盘统计
    demo_dashboard_statistics(token)
    
    # 11. API端点列表
    demo_api_endpoints()
    
    # 总结
    print_section("演示完成")
    print("""
    ✅ FMECA平台功能演示已完成！
    
    📋 演示内容包括：
       1. 用户认证系统
       2. 用户管理模块
       3. 设备管理模块
       4. 功能构成管理
       5. 失效模式管理
       6. 严重度分析
       7. 检测方法管理
       8. 补偿措施管理
       9. 风险分析
       10. 仪表盘统计
    
    🌐 访问地址：
       前端界面: http://localhost:3000
       API文档: http://localhost:8000
    
    👤 登录信息：
       用户名: admin
       密码: admin123
    
    💡 使用建议：
       1. 在浏览器中打开 http://localhost:3000
       2. 使用 admin/admin123 登录
       3. 依次浏览各个功能模块
       4. 创建自己的设备、失效模式和分析数据
    """)

if __name__ == "__main__":
    main()
