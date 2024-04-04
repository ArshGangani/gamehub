from django.shortcuts import render, redirect

from gameapp.models import Game
from authentication.models import ProfileStat
from .forms import NewUserForm
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login, authenticate, logout #add this
def home(request):
    games = Game.objects.all()
    return render(request,'home.html',{'games': games})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile_stat = ProfileStat.objects.create(Name=user)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("authentication:home")
        return render (request=request, template_name="register.html", context={"register_form":form,"error_message":messages})
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("authentication:home")
            else:
                return render(request=request, template_name="login.html", context={"login_form":form,"error_message":messages})
        else:
            return render(request=request, template_name="login.html", context={"login_form":form,"error_message":messages})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("authentication:home")