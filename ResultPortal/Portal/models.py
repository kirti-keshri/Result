from django.db import models

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
    reg_no = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=200)
    dob = models.DateField()
    Aadhar_no = models.CharField(unique=True)

    class Meta:
        unique_together = ('school', 'reg_no')

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
    
class Role(models.Model):
    choice = [("student","student"),("teacher","teacher"),("marks_uploader","marks_uploader")]
    role = models.CharField(max_length=20,choices=choice,null=True,blank=True)
