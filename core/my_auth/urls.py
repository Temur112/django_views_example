from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'my_auth'
urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='my_auth/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('getCookie/', views.get_cookie_view, name='getCookie'),
    path('setCookie/', views.set_cookie_view, name='setCookie'),
    path('setSession/', views.set_session_view, name='setSession'),
    path('getSession/', views.get_session_view, name='getSession'),
    path('logout/', views.logout_view, name='logout'),
    # path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('about', views.AboutMeView.as_view(), name='aboutMe'),
    path('createUser/', views.CreateUserView.as_view(), name='createUser'),
]
