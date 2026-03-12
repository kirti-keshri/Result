"""
URL configuration for ResultPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from Portal.views import *
 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",result_search, name="result_search"),  # home
    path("result/", result_view, name="result_view"),
    path("login_view/",login_view,name="login"),
    path("logout_view/",logout_view,name="logout"),
    path("student_dashboard/",student_dashboard,name="student_dash"),
    path("teacher_dashboard/",teacher_dashboard,name="teacher_dash"),
    path("school_dashboard/",school_dashboard,name="school_dash"),
    path("portal_dashboard/",portal_dashboard,name="portal_dash"),

]
