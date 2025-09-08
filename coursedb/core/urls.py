from django.urls import path

from core.views import base

urlpatterns = [
    path('', base.index, name='core.index'),
]
