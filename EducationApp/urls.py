"""EducationApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from django.urls import path, include
# from courses.views import CourseListView
#
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from django.conf import settings  # new
from django.conf.urls.static import static  # new

from courses.api.views import SubjectViewAPI
from courses.views import CourseListView
from tickets.views import APIUserTickets, APISupportTicket, ViewTickets, ViewResponse
from users.views import *
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from users.permissions import IsTokenValid
permission_cls = {"permission_classes": (IsTokenValid,)}
# obtain_jwt_token = ObtainJSONWebToken.as_view(**permission_cls)
# refresh_jwt_token = RefreshJSONWebToken.as_view(**permission_cls)
# verify_jwt_token = VerifyJSONWebToken.as_view(**permission_cls)


urlpatterns = [
 path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
 path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
 path('admin/', admin.site.urls),
 path('course/', include('courses.urls')),
 path('api/course/',include('courses.api.urls', namespace='api')),
 path('api/subject/',SubjectViewAPI.as_view()),
 path('api/student/',include('students.api.urls')),
 path('user_tickets/', APIUserTickets.as_view()),
 path('tickets/', ViewTickets.as_view()),
 path('support_response/<int:ticket_id>/', APISupportTicket.as_view()),
 path('ticket_response/<int:ticket_id>/', ViewResponse.as_view()),
 path('', CourseListView.as_view(), name='course_list'),
 path('students/', include('students.urls')),
 path('login/', ObtainJSONWebToken.as_view()),
 path('refresh/',RefreshJSONWebToken.as_view(**permission_cls)),
 path('registration/', CreateUserAPIView.as_view()),
path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
activate, name='activate'),
#     path('', CourseListView.as_view(), name='course_list'),
 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
