"""Custom pagination module"""
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    """Add content-range header to response"""
    def get_paginated_response(self, data):
        """
        Override default pagination to
        add Content-Range header and prettify links
        """
        limit_index = self.limit + self.offset
        to_number = limit_index if limit_index <= self.count else self.count
        content_range = f'{self.offset + 1}-{to_number}/{self.count}'
        headers = {"Content-Range": content_range}
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.count,
            'results': data
        }, headers=headers)
