from django.forms import ModelForm
from .models import *

class SchoolForm(ModelForm):
    class Meta:
        model =School
        fields = "__all__"
        
        
        