from django import forms
from .models import PcbType

class PcbTypeForm(forms.ModelForm):
    class Meta:
        model = PcbType
        fields = ['name', 'description']
