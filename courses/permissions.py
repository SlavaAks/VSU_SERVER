from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user
