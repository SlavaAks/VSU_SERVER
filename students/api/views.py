from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework import status, renderers
from rest_framework.response import Response

from courses.api.serializers import CourseSerializer, SubjectSerializer, CourseWithContentsSerializer, ModuleSerializer, \
    ContentSerializer, ModuleWithContentsSerializer, CourseWithModuleSerializer
from courses.models import Course, Subject, Module, Content, Video
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from students.api.permissions import IsEnrolled

from rest_framework import generics

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from rest_framework.decorators import action
from .permissions import IsEnrolled


class StudentEnrollCourseView(APIView):

    def post(self, request, id):
        print(request.user)
        try:
            course = Course.objects.get(id=id)
            course.students.add(request.user)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class StudentCourseListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        qs = Course.objects.all()
        courses = qs.filter(students__in=[request.user])
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentModuleListView(APIView):
    permission_classes = (IsAuthenticated,IsEnrolled)

    def get(self,request,id):
        try:
            course=Course.objects.get(id=id)
            print(course)
            try:
                self.check_object_permissions(request, course)
                modules = Module.objects.filter(course=course)
                print(modules)
                serializer = ModuleSerializer(modules,many=True)
                return  Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class StudentContentListView(APIView):
    permission_classes = (IsAuthenticated,IsEnrolled)

    def get(self,request,id):
        try:
            module=Module.objects.get(id=id)
            try:
                self.check_object_permissions(request, module.course)
                contents=Content.objects.filter(module=module)
                serializer = ContentSerializer(contents,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                 return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,methods=['post'],
            # authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True, methods=['get'],
            serializer_class=CourseWithModuleSerializer,
            # authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated,
                                IsEnrolled])
    def modules(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True,methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            # authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated,
                                IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



class VideoRenderer(renderers.BaseRenderer):
    media_type = 'video/mp4'
    format = 'mp4'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        a='D:/EducationApp/EducationApp/media/video/file_1652012439956.mp4'
        print('D:/EducationApp/EducationApp/media/video/file_1652012439956.mp4',"   pizdec")
        with open('media/video/file_1652012439956.mp4','rb') as file:
            data=file.read()
        return data


class VideoView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes=[VideoRenderer]

    def get(self,request,url):
        print(url)
        data = Video.objects.all()[0]
        print(data.video)
        return Response(data.video)
