from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UserLoginForm, UserEditForm, RegisterForm


class UserLogin(FormView):
    template_name = 'account/user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home_app:main')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You are already logged in")
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=form.cleaned_data.get('password'))
        login(self.request, user)
        messages.success(self.request, "You are successfully logged in")
        return super().form_valid(form)


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
