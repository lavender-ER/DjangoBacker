from rest_framework.pagination import PageNumberPagination


class MyPag(PageNumberPagination):
    page_size_query_param = "max_page"
    page_query_param = "page"
