# forms.py
from django import forms

class StudentProfileForm(forms.Form):
    student_research_description = forms.CharField(
        label='Your Research Profile',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter your research profile...'})
    )
