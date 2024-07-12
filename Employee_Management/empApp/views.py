from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')


def allEmployees(request):
    emp = Employee.objects.all()
    context = {
        "emps": emp
    }
    return render(request, 'allEmployees.html', context)

def addEmployees(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])

        newEmp = Employee(firstname=firstname,lastname=lastname, dept_id=dept, role_id=role, salary=salary, bonus=bonus, phone=phone, hire_date=datetime.now())
        newEmp.save()

        return HttpResponse("New Employee added Successfully!")
    
    elif request.method=='GET':
        return render(request, 'addEmployees.html')
    
    else:
        return HttpResponse("An Exception occured")

def removeEmployees(request):
    
    emps = Employee.objects.all()
    context = {
        "emps": emps
    }
    return render(request, 'removeEmployees.html', context)

def removeEmployee(request, emp_id):
    if id:
        try:
            empRemove = Employee.objects.get(id=emp_id)
            empRemove.delete()
            return HttpResponse("Employee removed successfully!")
        
        except:
            return HttpResponse("Invalid Employee!")
        
    

def filterEmployees(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(firstname__icontains = name) | Q(lastname__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)
        
        context = {
            "emps": emps
        }

        return render(request,'allEmployees.html', context)
    elif request.method == 'GET':
        return render(request, 'filterEmployees.html')
    else:
        return HttpResponse("An error occured!")
    