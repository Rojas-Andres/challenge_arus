from django.urls import path, include
from rest_framework import routers
from django.urls import path
from administration import views

urlpatterns = [
    path("client/", views.clients, name="clients"),
    path("create_client/", views.create_client, name="create_client"),
]
