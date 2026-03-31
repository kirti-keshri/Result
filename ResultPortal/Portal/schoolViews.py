from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *


#dashboard
def school_dashboard(request):
    school = School.objects.first()
    
    total_teachers = Teacher.objects.filter(school=school).count()
    total_students = Student.objects.filter(school=school).count()
    total_classes = ClassRoom.objects.filter(school=school).count()
    total_sections = Section.objects.filter(class_ref__school =school).count()
    active_years = AcademicYear.objects.filter(school=school,is_active=True).count()
    total_subjects = Subject.objects.filter(classes__school=school).count()
    total_exams = Exam.objects.filter(school=school).count()
    
    data ={
        "school" : school,
        "total_teachers" : total_teachers,
        "total_students" : total_students,
        "total_classes" : total_classes,
        "total_sections" : total_sections,
        "active_years" : active_years,
        "total_subjects":total_subjects,
        "total_exams":total_exams,
    }
    return render(request,"school/school_dashboard.html",data)

#read academic year list
def academic_year_list(request):
    school = School.objects.first()
    years = AcademicYear.objects.filter(school=school).order_by("-id")
    return render(request,"school/academic_year_list.html",{"school":school,"years":years})

#create academicyear
def add_academic_year(request):
    school = School.objects.first()
    form = AcademicForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.save(commit=False)
            academic_year.school = school
            academic_year.save()
            return redirect("academic_year_list")
        else:
            form = AcademicForm()
            
    return render(request,"school/academic_year_form.html",{"form":form,"school":school})

#edit academicyear
def update_academic_year(request,academic_id):
    school = School.objects.first()
    year = get_object_or_404(AcademicYear,id=academic_id)
    form = AcademicForm(request.POST or None , instance= year)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("academic_year_list")
        else:
            form = AcademicForm(instance=year)

    return render(request,"school/academic_year_form.html",{"form":form,"school":school,"year":year})   

#delete academic_year
def delete_academic_year(request,academic_id):
    school = School.objects.first()
    year = get_object_or_404(AcademicYear, id = academic_id,school = school)
    
    if request.method == "POST":
        year.delete()
        return redirect("academic_year_list")
    
    
#active/inactive year

def toggle_academic_year(request,academic_id):
    school = School.objects.first()
    year = get_object_or_404(AcademicYear, id = academic_id, school = school)
    
    year.is_active = not year.is_active
    year.save()
    
    return redirect("academic_year_list")


#class_list

def student_list(request):
    school = School.objects.first()
    student = Student.objects.all()
    
    return render(request,"school/student_list.html",{"school":school,"student":student})

def add_student(request):
    school =School.objects.first()
    form = StudentForm(request.POST or None)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect("student_list")
    return render(request,"school/student_form.html",{"form":form,"school":school})

#update student

def edit_student(request,student_id):
    school = School.objects.first()
    student = get_object_or_404(Student, id = student_id)
    form = StudentForm(request.POST or None, instance= student)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("student_list")
    return render(request,"school/student_form.html",{"form":form,"school":school,"student":student})
            
#delete student

def delete_student(request,student_id):
    student = get_object_or_404(Student, id=student_id)           
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request,"school/student_confirm_delete.html",{"student":student})    

# crud class

def class_list(request):
    school = School.objects.first()
    class_ref = ClassRoom.objects.filter(school=school)
    
    return render(request,"school/class_list.html",{"school":school,"class_ref":class_ref})

def add_class(request):
    school = School.objects.first()
    form = ClassForm(request.POST or None)
    if request.method =="POST":
       if form.is_valid():
           data = form.save(commit=False)
           data.school= school
           data.save()
           return redirect("class_list")
    return render(request,"school/class_form.html",{"form":form})
       
def edit_class(request,class_id):
    school = School.objects.first()
    class_ref = get_object_or_404(ClassForm,id =class_id,school=school)
    form = ClassForm(request.POST or None, instance=class_ref)
    
    if form.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("class_list")
    return render(request,"school/class_form.html",{"form":form})

def delete_class(request,class_id):
    school = School.objects.first()
    class_ref = get_object_or_404(ClassRoom,id=class_id,school=school)
    if request.method =="POST":
        class_ref.delete()
        return redirect("class_list")
    
# crud of section
def section_list(request):
    school=School.objects.first()
    section = Section.objects.filter(class_ref__school=school)
    
    return render(request,"school/section.html",{"section":section,"school":school})

def add_section(request):
    school = School.objects.first()
    form = SectionForm(request.POST or None)
    # restrict class dropdown to current school
    form.fields["class_ref"].queryset = ClassRoom.objects.filter(school=school)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("section_list")
    return redirect(request,"school/section_form.html",{"school":school,"form":form})

def edit_section(request,section_id):
    school = School.objects.first()
    section = get_object_or_404(Section,id=section_id,school=school)
    form = SectionForm(request.POST or None ,instance=section)
    
    # restrict class dropdown to current school
    form.fields["class_ref"].queryset = ClassRoom.objects.filter(school=school)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("section_list")
        return redirect(request,"school/section_form.list",{"form":form,"section":section})
    
def delete_section(request,section_id):
    school = School.objects.first()
    section = get_object_or_404(Section,id=section_id,school=school)
    if request.method == "POST":
        section.delete()
        return redirect("section_list")