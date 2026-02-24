from django.shortcuts import render
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт!")
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Вход",
        "form": form,
    }

    return render(request, "users/login.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(
                request, f"{user.username}, Вы успешно зарегистрировались!")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Регистрация",
        "form": form,
    }

    return render(request, "users/register.html", context)


@login_required(login_url='/user/login/')
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return HttpResponseRedirect(reverse("users:profile"))

    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "Профиль",
        "form": form,
    }

    return render(request, "users/profile.html", context)


@login_required(login_url='/user/login/')
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта!")
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))


def users_cart(request):
    return render(request, "users/users_cart.html")