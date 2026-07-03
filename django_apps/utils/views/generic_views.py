from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class ListCoreView(GenericAPIView):
    """Class that adds the unfiltered_count to the filtered results of a
    view."""

    unfiltered_count = None
    filtered_count = None

    def get_paginated_response(self, data):
        unfiltered_count = {"count": self.unfiltered_count}
        result = super().get_paginated_response(data)
        result.data.update(**unfiltered_count)
        return result

    def get(self, request, *args, **kwargs):
        unfiltered_queryset = self.get_queryset()
        self.unfiltered_count = unfiltered_queryset.count()

        queryset = self.filter_queryset(unfiltered_queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListCoreViewFilterQuery(ListCoreView):
    def get_paginated_response(self, data):
        filtered_count = {"count": self.filtered_count}
        result = super().get_paginated_response(data)
        result.data.update(**filtered_count)
        return result

    def get(self, request, *args, **kwargs):
        unfiltered_queryset = self.get_queryset()

        queryset = self.filter_queryset(unfiltered_queryset)
        page = self.paginate_queryset(queryset)
        self.filtered_count = queryset.count()

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListCoreViewUnfilteredQuery(ListCoreView):
    def get(self, request, *args, **kwargs):
        unfiltered_queryset = self.get_queryset()
        self.unfiltered_count = unfiltered_queryset.count()

        page = self.paginate_queryset(unfiltered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(unfiltered_queryset, many=True)
        return Response(serializer.data)
