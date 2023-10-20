from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatalogPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response({
            "items": data,
            "currentPage": self.page.number,
            "lastPage": self.page.paginator.num_pages,
        })
