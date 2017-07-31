from django.http import  HttpResponse
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.shortcuts import render, redirect
from .forms import UserloginForm, UserregisterForm

# Create your views here.
def login_view(request):
    form = UserloginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect("/")
    return render(request, 'pages/examples/login.html', {"form":form})

def register(request):
    form = UserregisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit= False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user= authenticate(username=user.username, password = password)
        login(request, new_user)
        return redirect("/login")
    return render(request, 'pages/examples/register.html', {"form":form})

def logout_view(request):
    logout(request)
    return redirect ("/")

def home(request):
    return render(request, 'index2.html', {})