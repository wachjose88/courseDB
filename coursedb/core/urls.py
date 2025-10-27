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

    path('course/list', courses.course_list,
         name='core.course.list'),
    path('course/create', courses.course_create,
         name='core.course.create'),
    path('course/<int:course_id>', courses.course_details,
         name='core.course.details'),
    path('course/<int:course_id>/edit', courses.course_edit,
         name='core.course.edit'),
    path('course/<int:course_id>/delete', courses.course_delete,
         name='core.course.delete'),
    path('course/<int:course_id>/unit/<int:unit_id>/delete', courses.unit_delete,
         name='core.course.unit.delete'),
    path('course/<int:course_id>/unit/<int:unit_id>/edit', courses.unit_create_edit,
         name='core.course.unit.edit'),
    path('course/<int:course_id>/unit/create', courses.unit_create_edit,
         name='core.course.unit.create'),
    path('course/<int:course_id>/attendee/<int:attendance_id>/edit', courses.course_attendance_create_edit,
         name='core.course.attendance.edit'),
    path('course/<int:course_id>/attendee/new', courses.course_attendance_create_edit,
         name='core.course.attendance.create'),

    path("login/", av.LoginView.as_view(), name="login"),
    path("logout/", av.LogoutView.as_view(), name="logout"),
]
