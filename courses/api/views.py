from rest_framework import generics, status
from ..models import Subject, Module, Content
from .serializers import TextSerializer, VideoSerializer, FileSerializer, ImageSerializer, \
    ModuleSerializer, ContentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .serializers import CourseSerializer
from .permissions import IsEnrolled, IsAuthor


# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#
#
# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#
#
# class CourseViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#
#     @detail_route(methods=['post'],
#                       authentication_classes=[BasicAuthentication],
#                       permission_classes=[IsAuthenticated])
#     def enroll(self, request, *args, **kwargs):
#         course = self.get_object()
#         course.students.add(request.user)
#         return Response({'enrolled': True})
#
#     @detail_route(methods=['get'],
#                   serializer_class=CourseWithContentsSerializer,
#                   authentication_classes=[BasicAuthentication],
#                   permission_classes=[IsAuthenticated,
#                                       IsEnrolled])
#     def contents(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)





#######FOR TUTORS#######################

class ManageCourseListViewAPI(APIView):
    permission_classes=(IsAuthenticated,IsAdminUser)

    def get(self,request):
        courses = Course.objects.filter(owner=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request):
        print(request.data)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.create(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoueseViewApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        courses = Course.objects.filter()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageCourseViewAPI(APIView):
    permission_classes=(IsAuthenticated,IsAdminUser)

    def delete(self, request, pk):
        print(pk)
        event = Course.objects.get(id=pk)
        if event:
            event.delete()
        else: Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CourseModuleAPI(APIView):
    permission_classes=(IsAuthenticated,IsAuthor)

    def get(self, request,pk):
        # self.check_object_permissions(request, pk)
        moduls = Module.objects.filter(course=pk)
        serializer = ModuleSerializer(moduls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,pk):
        self.check_object_permissions(request, pk)
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            module = serializer.create(request,pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseModuleOrderAPI(APIView):
    permission_classes=(IsAuthenticated,IsAuthor)

    def post(self, request,pk):

        ord=0
        for i in request.data:
            print(i["id"])
            Module.objects.filter(id=i["id"],course__owner=request.user).update(order=ord)
            ord=ord+1
        return Response(status.HTTP_202_ACCEPTED)

class ContentAPI(APIView):
    # parser_classes = [parsers.MultiPartParser, parsers.FormParser, FileUploadParser]
    permission_classes=(IsAuthenticated,IsAdminUser,IsAuthor)

    def get(self,request,module_id):
        #######################обработать ошибку если нету такого модуля
        # print(module_id)
        # # contents=Module.objects.filter()
        # print(module.id)
        # # serializer=ModuleWithContentsSerializer(module)
        contents=Content.objects.filter(module=module_id)

        # print(contents)

        serializer=ContentSerializer(contents,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



    def post(self,request,module_id):
        print("dddddd")
        content_type={"text":TextSerializer,"video":VideoSerializer,"file":FileSerializer,"image":ImageSerializer}
        print("dddddd")
        data=request.data.dict()
        try:
            data['content_type']
        except:
            raise
        if data['content_type'] in content_type.keys():
            print('rrrr')
            print(data)
            print(request.FILES)
            serializer=content_type[data.get('content_type')](data=data)
            try:
                module=Module.objects.get(id=module_id)
            except:
                return Response({"detail","нет такого модуля"}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                print(serializer.validated_data)
                obj=serializer.create(serializer.validated_data,request)
                content=Content.objects.create(module=module, item=obj)
                content.save()
                return Response({"detail": "item is created"}, status=status.HTTP_201_CREATED)

        #######################обработать ошибку если нету такого модуля

        return Response({"detail":"bad data"}, status=status.HTTP_400_BAD_REQUEST)
        # serializer = ContentSerializer()
        # if serializer.is_valid():
        #     module = serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

