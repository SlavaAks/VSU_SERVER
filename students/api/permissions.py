from rest_framework.permissions import BasePermission

from courses.models import Course


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        print(request.user.id)
        print(obj.students.filter(id=request.user.id).exists())
        return obj.students.filter(id=request.user.id).exists()