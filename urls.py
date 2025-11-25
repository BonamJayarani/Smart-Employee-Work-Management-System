from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from employee_management_system.views import dashboard,home,salary_list, add_salary, edit_salary, delete_salary

urlpatterns = [
    path("", home, name="home"),  # ✅ Add this for the homepage
    path("admin/", admin.site.urls),  # ✅ Ensure this appears only once
    path('dashboard/', dashboard, name='dashboard'),  # ✅ Register dashboard route
    path('', include('employee_management_system.urls')),
     # Authentication (Django Allauth)
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('salaries/', salary_list, name='salary_list'),
    path('salaries/add/', add_salary, name='add_salary'),
    path('salaries/edit/<int:salary_id>/', edit_salary, name='edit_salary'),
    path('salaries/delete/<int:salary_id>/', delete_salary, name='delete_salary'),

]
