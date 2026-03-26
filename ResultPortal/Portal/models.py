from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role= models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.role

# school
class School(models.Model):
    Board_choices = [("BSEB","BSEB"),("CBSE","CBSE"),("iCSE","ISCE"),("STATE","STATE")]
    board = models.CharField(max_length = 20,choices=Board_choices,null=True,blank=True)
    affliated = models.CharField(max_length=200)
    name= models.CharField(max_length=50)
    school_code =models.PositiveIntegerField(unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pin_code = models.IntegerField(max_length=6)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
#teacher
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name="school")
    # name = models.CharField(max_length=200)
    teacher_code = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        return self.user.username
    
    
#academic year

class AcademicYear(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    batch_year =models.CharField(max_length=200)
    start_date = models.DateField()
    end_date =  models.DateField()
    is_active =models.BooleanField(default=True)
    
    def __str__(self):
        return self.batch_year

#class
class ClassRoom(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name="schools")
    class_name = models.CharField(max_length=50)
    def __str__(self):
       return  self.class_name

#section 
class Section(models.Model):
    class_ref = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    section_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.class_ref}{self.section_name}"
    
# student
class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year= models.ForeignKey(AcademicYear,on_delete=models.CASCADE)
    admission_no = models.CharField(max_length=20)
    classes = models.ForeignKey(ClassRoom,on_delete=models.CASCADE,related_name="class_sec")
    section = models.ForeignKey(Section,on_delete=models.CASCADE,related_name="section_sec")
    reg_no = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=200)
    dob = models.DateField()
    Aadhar_no = models.CharField(unique=True,max_length=12)
    email = models.EmailField(null=True,blank=True)
    Phone = models.CharField(max_length=15,null=True,blank=True)
    gender=models.CharField(max_length =10 ,choices=[("Male","Male"),("Female","Female"),("Other","Other")])
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = [('school', 'reg_no'),('school','roll_no')]


    def __str__(self):
        return self.name
   
class Exam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)# 2025-2026
    name = models.CharField(max_length=100)  # Final/Half-Yearly
    status = models.CharField(
        max_length=20,
        choices=[("DRAFT", "Draft"), ("PUBLISHED", "Published")],
        default="DRAFT"
    )

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    classes = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default= 30)

    def __str__(self):
        return self.name

class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    classes = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.exam.name} - {self.subject.name}"



class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    class Meta:
        unique_together = ('student', 'exam','subject')

    def __str__(self):
        return f"{self.student.name} - {self.exam.name} - {self.subject.name}"
      

    
# class Role(models.Model):
#     role_choices = [("student", "Student"), ("teacher", "Teacher"),("school_admin", "School_Admin"),("marks_uploader", "Marks Uploader"),"Superadmin","Superadmin"),("portal_admin", "Portal Admin")]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=role_choices)
#     school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
#     student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)


#     def __str__(self):
#         return f"{self.user.username} - {self.role}" 


