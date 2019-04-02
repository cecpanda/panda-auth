from faker import Faker, Factory
from rest_framework.pagination import PageNumberPagination


fake = Faker()


class UserPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page-size'
    page_query_param = "page"
    max_page_size = 100
