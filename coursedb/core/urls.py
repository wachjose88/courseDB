from django.urls import path

from core.views import base, clients
from django.contrib.auth import views as av

urlpatterns = [
    path('', base.index, name='core.index'),
    path('client/list', clients.client_list, name='core.client.list'),
    path('client/create', clients.client_create_edit,
         name='core.client.create'),
    path('client/<int:client_id>/edit', clients.client_create_edit,
         name='core.client.edit'),

    path("login/", av.LoginView.as_view(), name="login"),
    path("logout/", av.LogoutView.as_view(), name="logout"),
]
