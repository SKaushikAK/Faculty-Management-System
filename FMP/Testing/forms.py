from django import forms
from .models import Faculty

class UploadFileForm(forms.Form):
    file = forms.FileField()
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)
class FacultyUpdateForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'department']  # Include other fields as needed
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)
