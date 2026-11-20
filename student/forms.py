from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Student_table


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student_table
        fields = ('reg_no', 'name', 'email', 'marks', 'date')
        labels = {
            'reg_no': 'Registration number',
            'date': 'Date of birth',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_reg_no(self):
        reg_no = self.cleaned_data['reg_no']
        qs = Student_table.objects.filter(reg_no=reg_no)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                'A student with this registration number is already registered.'
            )
        return reg_no


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')