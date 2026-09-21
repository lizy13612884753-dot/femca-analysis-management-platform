import requests

# 测试 overall_summary API
url = 'http://localhost:8000/api/product-analysis/analyses/overall_summary/'
response = requests.get(url)
print('Status Code:', response.status_code)
print('Response:')
print(response.json())
