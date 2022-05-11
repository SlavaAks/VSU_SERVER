from rest_framework.permissions import BasePermission

from courses.models import Course


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, id):
        print(id)
        if not Course.objects.filter(id=id).exists():
            return False
        print(Course.objects.filter(id=id).first().owner)
        print( request.user)
        return Course.objects.filter(id=id).first().owner == request.user
