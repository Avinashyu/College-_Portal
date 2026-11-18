from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home (request):
    data = {
        'name': 'Avinash',
        'age': 20,
        'department': 'Computer Science',
    }
    marks = [85, 90, 78, 92, 88]
    return render(request, 'home.html', {'data1': data, 'marks1': marks})
        

def about(request):
    return render (request,'about.html')
def contact(request):
    return render (request,'contact.html')