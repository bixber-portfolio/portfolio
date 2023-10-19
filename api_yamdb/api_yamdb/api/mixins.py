from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.permissions import BasePermission

from users.validators import value_validator

User = get_user_model()


class CreateOnlyModelMixin(mixins.CreateModelMixin,
                           GenericViewSet):
    """Creation only mixin"""


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


USERNAME_REGEX = UnicodeUsernameValidator.regex


class UserBaseSerializer(serializers.ModelSerializer):
    """General serializer for all types of users"""
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=150,
        required=True,
        validators=[value_validator],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class AdminPermissionMixin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
