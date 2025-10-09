from django.urls import path

from core.views import base, clients, courses
from django.contrib.auth import views as av

urlpatterns = [
    path('', base.index, name='core.index'),
    path('client/list', clients.client_list, name='core.client.list'),
    path('client/create', clients.client_create_edit,
         name='core.client.create'),
    path('client/<int:client_id>/edit', clients.client_create_edit,
         name='core.client.edit'),
    path('client/<int:client_id>/delete', clients.client_delete,
         name='core.client.delete'),
    path('client/<int:client_id>/copy', clients.client_copy,
         name='core.client.copy'),

    path('course/description/list', courses.course_description_list,
         name='core.course.description.list'),
    path('course/description/create', courses.course_description_create_edit,
         name='core.course.description.create'),
    path('course/description/<int:description_id>/edit', courses.course_description_create_edit,
         name='core.course.description.edit'),
    path('course/description/<int:description_id>/delete', courses.course_description_delete,
         name='core.course.description.delete'),
    path('course/description/<int:description_id>/copy', courses.course_description_copy,
         name='core.course.description.copy'),

    path("login/", av.LoginView.as_view(), name="login"),
    path("logout/", av.LogoutView.as_view(), name="logout"),
]
