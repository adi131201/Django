from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('allEmployees', views.allEmployees, name="all"),
    path('addEmployees', views.addEmployees, name="add"),
    path('removeEmployees', views.removeEmployees, name="remove"),
    path('removeEmployee/<int:emp_id>', views.removeEmployee, name="removeEmployee"),
    path('filterEmployees', views.filterEmployees, name="filter"),
]
