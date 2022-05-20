import json

import dropbox
import redis as redis
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from rest_framework import generics, status

from EducationApp import settings
from ..models import Subject, Module, Content
from .serializers import TextSerializer, VideoSerializer, FileSerializer, ImageSerializer, \
    ModuleSerializer, ContentSerializer, SubjectSerializer, TestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .serializers import CourseSerializer
from .permissions import IsAuthor


# redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
#                                   port=settings.REDIS_PORT, db=0)
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
class SubjectViewAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self,request):
        if 'subjects' in cache:
            # get results from cache
            subjects = cache.get('subjects')
            return Response(subjects, status=status.HTTP_200_OK)

        else:
            subjects = Subject.objects.all()
            results = [subject.to_json() for subject in subjects]
            # store data in cache
            cache.set('subjects', results, timeout=CACHE_TTL)
            return Response(results, status=status.HTTP_200_OK)

    def post(self,request):
        serializer=SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#######FOR TUTORS#######################

class ManageCourseListViewAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        courses = Course.objects.filter(owner=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @method_decorator(permission_required("courses.add_course"))
    def post(self, request):
        print(request.data)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.create(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseViewApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        courses = Course.objects.filter()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageCourseViewAPI(APIView):
    permission_classes = (IsAuthenticated,IsAuthor)

    def delete(self, request, pk):
        self.check_object_permissions(request, pk)
        event = Course.objects.get(id=pk)
        if event:
            event.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseModuleAPI(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def get(self, request, pk):
        # self.check_object_permissions(request, pk)
        modules = Module.objects.filter(course=pk)
        self.check_object_permissions(request, pk)
        # self.get_permissions()[1].has_object_permission(request,CourseModuleAPI,2)
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        self.check_object_permissions(request, pk)
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            module = serializer.create(request, pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CourseModuleOrderAPI(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def post(self, request, pk):
        self.check_object_permissions(request, pk)
        ord = 0
        for i in request.data:
            print(i["id"])
            Module.objects.filter(id=i["id"], course__owner=request.user).update(order=ord)
            ord = ord + 1
        return Response(status.HTTP_202_ACCEPTED)

class ModuleContentOrderAPI(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def post(self, request, pk):
        ord = 0
        for i in request.data:
            print(i["id"])
            Content.objects.filter(id=i["id"]).update(order=ord)
            ord = ord + 1
        return Response(status.HTTP_202_ACCEPTED)


class ModuleManagerAPI(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def delete(self, request, pk):
        event = Module.objects.get(id=pk)
        if event:
            self.check_object_permissions(request, event.course.id)
            event.delete()
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentAPI(APIView):
    # parser_classes = [parsers.MultiPartParser, parsers.FormParser, FileUploadParser]
    permission_classes = (IsAuthenticated, IsAdminUser, IsAuthor)

    def get(self, request, module_id):
        #######################обработать ошибку если нету такого модуля
        # print(module_id)
        # # contents=Module.objects.filter()
        # print(module.id)
        # # serializer=ModuleWithContentsSerializer(module)


        contents = Content.objects.filter(module=module_id)

        serializer = ContentSerializer(contents, many=True)
        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, module_id):
        content_type = {"text": TextSerializer, "video": VideoSerializer, "file": FileSerializer,
                        "image": ImageSerializer,"test":TestSerializer}
        data = request.data.dict()
        print(data)
        try:
            data['content_type']
        except:
            raise
        if data['content_type'] in content_type.keys():
            # print('rrrr')
            # print(data)
            # print(request.FILES)
            serializer = content_type[data.get('content_type')](data=data)
            try:
                module = Module.objects.get(id=module_id)
            except:
                return Response({"detail", "нет такого модуля"}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                print(serializer.validated_data)

                obj = serializer.create(serializer.validated_data, request)
                # UploadedFile(file='courses/static/file_example_XLSX_50.xlsx')
                print(obj)
                content = Content.objects.create(module=module, item=obj)
                content.save()
                return Response({"detail": "item is created"}, status=status.HTTP_201_CREATED)

        #######################обработать ошибку если нету такого модуля

        return Response({"detail": "bad data"}, status=status.HTTP_400_BAD_REQUEST)
        # serializer = ContentSerializer()
        # if serializer.is_valid():
        #     module = serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentManagerAPI(APIView):
    permission_classes = (IsAuthenticated, IsAuthor)

    def delete(self, request, id):
        print(id)
        try:
            event = Content.objects.get(id=id)
            if event:
                self.check_object_permissions(request, event.module.course.id)
                event.delete()
            else:
                Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
# {"title":"smath",
# "slug":"sssssd"}