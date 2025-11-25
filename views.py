from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Department, Leave, Salary, Setting
from .forms import EmployeeForm, LeaveForm, SalaryForm
from django.contrib.auth.decorators import user_passes_test,login_required
from .forms import EmployeeRegistrationForm
from django.contrib.auth import get_user_model
from django.apps import apps  # Import apps module

def home(request):
    return render(request, "home.html")  # Ensure this template exists

def my_view(request):
    Employee = apps.get_model('employee_management_system', 'Employee')  # ✅ Correct

def emp(request):
    from employee_management_system.models import Employee  # ✅ Move inside function
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})

def is_admin(user):
    return user.is_superuser  # Restrict access to superusers only

@user_passes_test(is_admin)
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')  # Redirect to employees list
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'register_employee.html', {'form': form})

@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_leaves = Leave.objects.filter(status='Pending').count()
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_leaves': total_leaves,
    }
    return render(request, 'dashboard.html', context)

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employee_management_system/departments/department_list.html', {'departments': departments})

# Employee Views
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/list.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employees/detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, "employee_management_system/employees/form.html", {"form": form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')

# Leave Views
# ✅ List all leaves
def leave_list(request):
    leaves = Leave.objects.all()
    return render(request, 'employee_management_system/leave_list.html', {'leaves': leaves})

# ✅ Add a new leave
def add_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_list')  # Redirect after adding leave
    else:
        form = LeaveForm()
    
    return render(request, 'employee_management_system/leave_form.html', {'form': form})

# ✅ Edit an existing leave
def edit_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)  # Get leave record or return 404
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_list')  # Redirect after updating leave
    else:
        form = LeaveForm(instance=leave)
    
    return render(request, 'employee_management_system/leave_form.html', {'form': form})

# ✅ Delete a leave
def delete_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)  # Get leave record or return 404
    if request.method == 'POST':
        leave.delete()
        return redirect('leave_list')  # Redirect after deleting leave
    
    return render(request, 'employee_management_system/leave_confirm_delete.html', {'leave': leave})

# View Salary List

def salary_list(request):
    salaries = Salary.objects.all()

    # Compute total salary for each salary record (avoid database error)
    for salary in salaries:
        salary.calculated_total_salary = salary.basic_salary + salary.bonus - salary.deductions
    return render(request, 'employee_management_system/salary_list.html', {'salaries': salaries})

# ✅ Add Salary
def add_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salary_list')  # Redirect to salary list after adding salary
    else:
        form = SalaryForm()
    return render(request, 'employee_management_system/salary_form.html', {'form': form})

# ✅ Edit Salary
def edit_salary(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('salary_list')  # Redirect to salary list after editing
    else:
        form = SalaryForm(instance=salary)
    return render(request, 'employee_management_system/salary_form.html', {'form': form})

# ✅ Delete Salary
def delete_salary(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)
    if request.method == 'POST':
        salary.delete()
        return redirect('salary_list')  # Redirect to salary list after deleting
    return render(request, 'employee_management_system/salary_confirm_delete.html', {'salary': salary})

# ✅ List Salaries
def salary_list(request):
    salaries = Salary.objects.all()
    return render(request, 'employee_management_system/salary_list.html', {'salaries': salaries})

# Settings Views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def settings_view(request):
    """Render the main settings page."""
    return render(request, "employee_management_system/settings/settings.html", {"user": request.user})


def settings_list_view(request):
    """Retrieve and display all settings from the database."""
    from .models import Setting  # ✅ Ensure this import is inside the function
    settings = Setting.objects.all() if Setting.objects.exists() else []
    return render(request, "employee_management_system/settings/list.html", {"settings": settings})


def employee_list(request):
    Employee = apps.get_model('employee_management_system', 'Employee')  # ✅ Lazy import
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})

