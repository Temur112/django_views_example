from django.urls import path
from . import views


app_name = 'my_api'
urlpatterns = [
    path('hello/', views.hello_api, name='hello'),
    path('groups/', views.GroupsListView.as_view(), name='groups'),
]
