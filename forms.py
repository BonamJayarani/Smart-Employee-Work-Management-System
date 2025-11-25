from django import forms
from .models import Employee, Leave, Salary

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'position', 'salary', 'is_active']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason', 'status']
    widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'basic_salary', 'bonus', 'deductions']

class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'department', 'position', 'salary']
