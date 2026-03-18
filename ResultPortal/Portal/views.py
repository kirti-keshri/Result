from django.shortcuts import render,redirect
from .models import *
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def result_search(request):
    schools = School.objects.filter(is_active=True).order_by('name')
    exams = Exam.objects.filter(status="PUBLISHED")
    
    school_code = request.GET.get("school_code")
    if school_code:
        exams = exams.filter(school__school_code=school_code)

    search_name = request.GET.get("search_name")
    if search_name:
        exams = exams.filter(name__icontains=search_name)

    return render(request, "result_search.html", {"exams": exams, "schools": schools})

def result_view(request):
    school_code = request.GET.get("school_code")
    reg_no = request.GET.get("reg_no")
    exam_id = request.GET.get("exam_id")

    if not (school_code and reg_no and exam_id):
        return render(request, "result_page.html", {"error": "Please fill all fields."})

    school = School.objects.filter(school_code=school_code, is_active=True).first()
    if not school:
        return render(request, "result_page.html", {"error": "Invalid school code."})

    exam = Exam.objects.filter(id=exam_id, school=school, status="PUBLISHED").first()
    if not exam:
        return render(request, "result_page.html", {"error": "Exam not found / not published."})

    student = Student.objects.filter(school=school, reg_no=reg_no).first()
    if not student:
        return render(request, "result_page.html", {"error": "Student not found."})

    subjects = Subject.objects.filter(exam=exam)
    marks_qs = Mark.objects.filter(student=student, subject__in=subjects).select_related("subject")
    marks_map = {m.subject_id: m.marks_obtained for m in marks_qs}

    rows = []
    total_obt = 0
    total_max = 0
    is_pass = True

    for sub in subjects:
        obtained = marks_map.get(sub.id, 0)
        total_obt += obtained
        total_max += sub.max_marks
        if obtained < sub.pass_marks:
            is_pass = False

        rows.append({"subject": sub.name, "max": sub.max_marks, "pass": sub.pass_marks, "obtained": obtained})

    percentage = round((total_obt / total_max) * 100, 2) if total_max else 0

    # Logic for Grade
    grade = "F"
    if percentage >= 90: grade = "A+"
    elif percentage >= 80: grade = "A"
    elif percentage >= 70: grade = "B"
    elif percentage >= 60: grade = "C"
    elif percentage >= 50: grade = "D"
    elif is_pass: grade = "E"

    return render(request, "result_page.html", {
        "school": school,
        "exam": exam,
        "student": student,
        "rows": rows,
        "total_obt": total_obt,
        "total_max": total_max,
        "percentage": percentage,
        "grade": grade,
        "result_status": "PASS" if is_pass else "FAIL",
    })
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            role = Role.objects.get(user=user)
            
            if role.role == "student":
                return redirect("student_dashboard")
            elif role.role == "teacher":
                return redirect("teacher_dashboard")    
            elif role.role == "school_admin":
                return redirect("school_admin_dashboard")
            elif role.role == "portal_admin":
                return redirect("portal_admin_dashboard")
            
        return render(request, "login.html", {"error": "Invalid username or password."})
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def student_dashboard(request):
    profile =Role.objects.get(user=request.user)
    student = profile.student
    return render(request, "student_dashboard.html",{"student":student})

@login_required
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")

# @login_required
def school_dashboard(request):
    # profile =UserProfile.objects.get(user=request.user)
    # school = role.school
    return render(request, "school_dashboard.html",)
# {"school":school}

@login_required
def portal_dashboard(request):
    schools = School.objects.all()
    data = {"schools":schools}
    return render(request, "portal_dashboard.html",data)