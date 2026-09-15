from django.shortcuts import render

def home(request):
    return render(request, 'ingressos/home.html')

# Create your views here.
