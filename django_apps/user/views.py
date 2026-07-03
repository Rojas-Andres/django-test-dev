"""
File with the user views.
"""

# Standard Library
import logging

from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_apps.user.filters import UserFilter
from django_apps.user.models import User
from django_apps.utils.views.generic_decorators import GenerateSwagger
from django_apps.utils.views.generic_views import ListCoreView
from django_apps.utils.views.mixins import APIErrorsMixin, LoggingRequestViewMixin
from django_apps.utils.views.pagination import CorePagination
from src.user.service_layer.services import CreateUser
from src.user.adapters.unit_of_work import UserUnitOfWork

logger = logging.getLogger(__name__)


@GenerateSwagger(swagger_auto_schema)
class UserCreateView(LoggingRequestViewMixin, APIErrorsMixin, APIView):
    """
    A view for handling user creation and update requests.

    This view allows users to be created and updated. It performs validation checks to ensure that the email address
    provided is unique and sends a welcome email to the user upon successful creation.

    Methods:
    - post: Create a new user.
    - put: Update an existing user.
    """

    permission_classes = [AllowAny]

    class InputPostSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        password = serializers.CharField(max_length=100)
        phone_number = serializers.CharField(
            max_length=20,
        )
        document = serializers.CharField(
            max_length=20,
        )
        code_phone = serializers.CharField(
            max_length=10,
        )

    class OutputPostSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        id = serializers.IntegerField()

    def post(self, request):
        """
        Create a new user.

        This method handles HTTP POST requests to create a new user. It performs validation checks to ensure that the
        email address provided is unique. Upon successful creation, it sends a welcome email to the user.

        Returns:
        - Response: A response indicating the success or failure of the user creation.
        """
        input_serializer = self.InputPostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        _user = CreateUser(uow=UserUnitOfWork()).create(
            **input_serializer.validated_data
        )
        serialize = self.OutputPostSerializer(data=_user)
        serialize.is_valid(raise_exception=True)
        return Response(data=serialize.data, status=status.HTTP_201_CREATED)


@GenerateSwagger(swagger_auto_schema)
class UserListView(APIErrorsMixin, ListCoreView):
    """
    A view for retrieving a list of all users.
    Requires authentication to access the view.
    """

    permission_classes = [AllowAny]
    permission_codename = "view_users"

    class OutputGetSerializer(serializers.Serializer):
        email = serializers.CharField()
        first_name = serializers.CharField(allow_null=True)
        phone_number = serializers.CharField(allow_null=True)
        document = serializers.CharField(allow_null=True)
        profile_image = serializers.ImageField(allow_null=True)

    serializer_class = OutputGetSerializer
    queryset = User.objects.all()
    pagination_class = CorePagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = UserFilter


# class UserDetailView(APIView):
#     """
#     A view that returns the details of a user.

#     Requires authentication and can receive a user id as a query parameter or use the id of the authenticated user.
#     It returns a serialized representation of the user object if it exists, or an error message if it doesn't.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self):
#         """
#         Retrieve the details of the user logged in.

#         If a user id is provided as a query parameter, it will retrieve the user with that id.
#         If no user id is provided, it will retrieve the user with the id of the authenticated user.

#         Returns:
#         - If the user is found, it returns a serialized representation of the user object with a status code of 200.
#         - If the user id is not found, it returns an error message with a status code of 400.
#         - If the user with the provided id is not found, it returns an error message with a status code of 404.
#         """
#         user_id = self.request.query_params.get("id", self.request.user.id)
#         if not user_id:
#             return Response(
#                 {"message": "User id not found"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         user = User.objects.filter(id=user_id).first()
#         if not user:
#             return Response(
#                 {"message": f"User with id {user_id} not found"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
