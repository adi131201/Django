from django.shortcuts import render

def home(request):
    return render(request, 'Home.html')

def about(request):
    return render(request, 'About.html')