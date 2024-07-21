from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import UserProfile
from django.contrib.auth.mixins import UserPassesTestMixin


# Create your views here.


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("cookie set")
    response.set_cookie("name", "value")
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("name", "Default")
    return HttpResponse(f"The cookie u have set is {value}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["name"] = "Konte"
    return HttpResponse("session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("name", "Default")
    return HttpResponse(f"The session u have set is {value}")


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("my_auth:login")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("my_auth:login")


class AboutMeView(TemplateView):
    template_name = "my_auth/about-me.html"


class CreateUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'my_auth/create_user.html'
    success_url = reverse_lazy("my_auth:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"]
        )
        login(request=self.request, user=user)
        return response


class UpdateUserProfileView(UserPassesTestMixin, UpdateView):
    template_name = 'my_auth/update_user_profile.html'
    success_url = reverse_lazy("my_auth:aboutMe")
    model = UserProfile
    fields = ["bio", "avatar", "agreement_accepted"]

    def test_func(self):
        user = self.request.user
        my_object = self.get_object()
        return user.userprofile.pk == my_object.pk or user.is_superuser or user.is_staff


