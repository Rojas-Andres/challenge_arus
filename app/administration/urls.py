from django.urls import path, include
from rest_framework import routers
from django.urls import path
from administration import views
from django.conf.urls import url

urlpatterns = [
    path("client/", views.clients, name="clients"),
    path("create_client/", views.create_client, name="create_client"),
    path("show_clients/", views.show_clients, name="show_clients"),
    path("update_client/", views.update_client, name="update_client"),
    path("update_client/<int:id_client>", views.update_client, name="update_client"),
    path("delete_client/<int:id_client>", views.delete_client, name="delete_client"),
]
