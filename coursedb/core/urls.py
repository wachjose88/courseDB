from django.urls import path

from core.views import base
from django.contrib.auth import views as av

urlpatterns = [
    path('', base.index, name='core.index'),

    path("login/", av.LoginView.as_view(), name="login"),
    path("logout/", av.LogoutView.as_view(), name="logout"),
]
