from django.forms import ModelForm,DateInput
from .models import *

class SchoolForm(ModelForm):
    class Meta:
        model =School
        fields = "__all__"
        
class AcademicForm(ModelForm):
    class Meta:
        model =AcademicYear
        exclude =["school"]
        widgets ={
            "start_date":DateInput(attrs={"type":"date"}),
            "end_date":DateInput(attrs={"type":"date"})
        }
        
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields ="__all__"   
        
        
        