from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'students'


#
router = routers.DefaultRouter()
router.register('st', views.CourseViewSet)


urlpatterns = [
    path('course/',views.StudentCourseListView.as_view()),
    path('course/<id>/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('course/<id>/module/',views.StudentModuleListView.as_view()),
    path('course/module/<id>/content/',views.StudentContentListView.as_view()),




    path('subjects/',
         views.SubjectListView.as_view(),
         name='subject_list'),
    path('subjects/<pk>/',
         views.SubjectDetailView.as_view(),
         name='subject_detail'),
    path('subject/<id>/course/',views.StudentSubjectCoursesAPI.as_view()),


    path('download/media/video/<url>/',views.VideoView.as_view()),
    path('', include(router.urls)),

]



