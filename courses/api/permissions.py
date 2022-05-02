from rest_framework.permissions import BasePermission

from courses.models import Course


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, id):
        print(id)
        if not Course.objects.filter(id=id).exists():
            return True
        return Course.objects.filter(id=id).first().owner == request.user
