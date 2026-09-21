from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """自定义分页类，支持前端传入page_size参数"""
    # 允许前端通过page_size参数控制每页显示的记录数
    page_size_query_param = 'page_size'
    # 最大页面大小，防止前端请求过大的页面
    max_page_size = 100
