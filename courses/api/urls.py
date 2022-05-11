from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'

urlpatterns = [
    path('mine/',
         views.ManageCourseListViewAPI.as_view()
         ),

    path('/', views.CourseViewApi.as_view()
         ),

    path('<pk>/',
         views.ManageCourseViewAPI.as_view()
         ),

    path('module/<pk>/', views.ModuleManagerAPI.as_view()),

    path('<pk>/module/',
         views.CourseModuleAPI.as_view()),

    path('<pk>/module/order/',
         views.CourseModuleOrderAPI.as_view()
         ),

    path('module/<int:module_id>/content/',
         views.ContentAPI.as_view()),
    path('module/content/<int:id>/',
         views.ContentManagerAPI.as_view()),
]
