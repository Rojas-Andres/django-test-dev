from collections import OrderedDict
from math import ceil

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.conf import settings


class CorePagination(LimitOffsetPagination):
    """Pagination class that overrides the get_paginated_response method to
    add the filtered count."""

    page_query_param = "page"
    default_limit = settings.DEFAULT_PAGE_SIZE

    def get_paginated_response(self, data) -> Response:
        """
        Overridden method to customize the paginated response structure.

        This method returns the paginated data along with a metadata
        section that includes pagination details and a timestamp.

        Args:
            data (list): List of serialized items for the current page.

        Returns:
            Response: A Response object with paginated data and
                metadata.
        """

        # Calculate the number of items per page (page size)
        page_size = self.limit

        # Calculate the total number of pages required
        total_pages = ceil(self.count / page_size)

        return Response(
            OrderedDict(
                [
                    ("results", data),
                    ("filtered", self.count),
                    ("limit", self.limit),
                    ("total_pages", total_pages),
                    (
                        "links",
                        {
                            "next": self.get_next_link(),
                            "previous": self.get_previous_link(),
                        },
                    ),
                ]
            )
        )
