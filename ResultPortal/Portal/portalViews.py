from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import *



# portal dashboard
def portal_dashboard(request):
    total_schools = School.objects.count()
    active_schools =School.objects.filter(is_active=True).count()
    inactive_schools = School.objects.filter(is_active=False).count()
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    active_years = AcademicYear.objects.filter(is_active=True).count()
    published_exam = Exam.objects.filter(status="Published").count()
    recent_schools =School.objects.order_by("-id")[:5]
    
    
    data = {
        "total_schools" : total_schools,
        "active_schools" :active_schools,
        "inactive_schools" :inactive_schools,
        "total_teachers" :total_teachers,
        "total_students" : total_students,
        "active_years" : active_years,
        "published_exam":published_exam,
        "recent_schools":recent_schools,
    }
    
    return render(request,"portal/portal_dashboard.html",data)

#school list
def school_list(request):
    schools = School.objects.all().order_by("-id")
    return render(request,"portal/school_list.html",{"schools":schools})


#active/inactive schools 
def toggle_school_status(request,school_id):
    school = School.objects.get(id=school_id)
    school.is_active = not school.is_active
    school.save()
    
    return redirect("school_list")

#add school
def add_school(request):
    form = SchoolForm(request.POST or None)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect("school_list")
        else:
            form = SchoolForm() 
    return render(request,"portal/school_form.html",{"form":form})

#update school
def update_school(request,school_id):
    school = get_object_or_404(School,id=school_id)
    form = SchoolForm(request.POST or None,instance=school)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect("school_list")
        
    return render(request,"portal/school_form.html",{"form":form,"school":school})
