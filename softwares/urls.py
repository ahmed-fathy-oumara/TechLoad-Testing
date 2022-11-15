from django.urls import path
from . import views

urlpatterns = [
    path('', views.softwaresCatalogue, name='softwares'),
]
