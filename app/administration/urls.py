from django.urls import path, include
from rest_framework import routers
from django.urls import path
from administration.views import client, server
from django.conf.urls import url

urlpatterns = [
    # Clients
    path("client/", client.clients, name="clients"),
    path("create_client/", client.create_client, name="create_client"),
    path("show_clients/", client.show_clients, name="show_clients"),
    path("update_client/", client.update_client, name="update_client"),
    path("update_client/<int:id_client>", client.update_client, name="update_client"),
    path("delete_client/<int:id_client>", client.delete_client, name="delete_client"),
    # Servers
    path("server/", server.servers, name="servers"),
    path("create_server/", server.create_server, name="create_server"),
    path("show_servers/", server.show_servers, name="show_servers"),
    path("delete_server/<int:id_server>", server.delete_server, name="delete_server"),
    path("update_server/<int:id_server>", server.update_server, name="update_server"),
    path("get/ajax/validate_client", client.validate_client, name="validate_client"),
]
