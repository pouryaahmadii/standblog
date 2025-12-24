from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm, UserEditForm, RegisterForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home_app:main')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get('username'))
            login(request, user)
            return redirect('home_app:main')
    else:
        form = UserLoginForm()
    return render(request, 'account/user_login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect('home_app:main')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You are successfully registered")
            return redirect('home_app:main')
    else:
        form = RegisterForm()

    return render(request, 'account/user_register.html', {"form": form})


def user_edit(request):
    user = request.user
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'account/user_edite.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home_app:main')
