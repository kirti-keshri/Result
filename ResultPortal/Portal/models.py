from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class School(models.Model):
    name= models.CharField(max_length=50)
    school_code =models.PositiveIntegerField(unique=True)
    address = models.CharField(max_length=200)
    Phone = models.IntegerField()
    email = models.EmailField()
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year = models.CharField(max_length=9)  # 2025-2026
    name = models.CharField(max_length=100)  # Final/Half-Yearly
    status = models.CharField(
        max_length=20,
        choices=[("DRAFT", "Draft"), ("PUBLISHED", "Published")],
        default="DRAFT"
    )

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default= 30)

    def __str__(self):
        return self.name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=200)
    dob = models.DateField()
    Aadhar_no = models.CharField(unique=True,max_length=12)
    email = models.EmailField(null=True,blank=True)
    Phone = models.CharField(max_length=15,null=True,blank=True)
    Class = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    
    

    class Meta:
        unique_together = ('school', 'reg_no'),('school','roll_no')


    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"
    
class UserProfile(models.Model):
    role_choices = [("student", "Student"), ("teacher", "Teacher"),("school_admin", "School_Admin"),("marks_uploader", "Marks Uploader"),("portal_admin", "Portal Admin")]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=role_choices)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


