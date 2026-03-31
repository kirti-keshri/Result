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
from Portal.portalViews import *
from Portal.schoolViews import *
 


urlpatterns = [
    #superadmin
    path('admin/', admin.site.urls),
    
    
    #authentication
    path("login_view/",login_view,name="login"),
    path("logout_view/",logout_view,name="logout"),
    
    #portal
    path("portal_dashboard/",portal_dashboard,name="portal_dash"),
    path("schools/",school_list,name="school_list"),
    path("schools/add/",add_school,name="add_school"),
    path("schools/edit/<int:school_id>/",update_school,name="update_school"),
    path("schools/toggle/<int:school_id>/",toggle_school_status,name="toggle_school_status"),
    
    #school admin
    path("school_dashboard/",school_dashboard,name="school_dash"),
    path("school/academic_years/",academic_year_list,name="academic_year_list"),
    path("school/academic_years/add/",add_academic_year,name="add_academic_year"),
    path("school/academic_years/edit/<int:academic_id>/",update_academic_year,name="update_academic_year"),
    path("school/academic_years/delete/<int:academic_id>/",delete_academic_year,name="delete_academic_year"),
    path("school/academic_years/toggle/<int:academic_id>/",toggle_academic_year,name="toggle_academic_year"),
    path("school/students/", student_list, name="student_list"),
    path("school/students/add/",add_student, name="add_student"),
    path("school/students/edit/<int:student_id>/", edit_student, name="edit_student"),
    path("school/students/delete/<int:student_id>/",delete_student, name="delete_student"),
    path("school/class/", class_list, name="class_list"),
    path("school/class/add/",add_class, name="add_class"),
    path("school/class/edit/<int:class_id>/", edit_class, name="edit_class"),
    path("school/class/delete/<int:class_id>/",delete_class, name="delete_class"),
    path("school/section", section_list, name="section_list"),
    path("school/section/add/",add_section, name="add_section"),
    path("school/section/edit/<int:section_id>/", edit_section, name="edit_section"),
    path("school/section/delete/<int:section_id>/",delete_section, name="delete_section"),
    
    #teacher
    path("teacher_dashboard/",teacher_dashboard,name="teacher_dash"),
    
    #student
    path("student_dashboard/",student_dashboard,name="student_dash"),
    path("",result_search, name="result_search"),  # home
    path("result/", result_view, name="result_view"),
    
    

]
