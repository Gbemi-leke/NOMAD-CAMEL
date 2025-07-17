from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.

def login(request):
    return render(request, 'backend/login.html')
