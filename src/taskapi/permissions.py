from rest_framework import permissions
from django.conf import settings


class IsCreator(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to edit it.
    """

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
