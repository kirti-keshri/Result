from django.shortcuts import render
from .models import *
from django.db.models import Sum
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