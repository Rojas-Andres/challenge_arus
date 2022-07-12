from django.urls import path, include
from rest_framework import routers
from django.urls import path
from administration.views import client, server, service
from django.conf.urls import url

urlpatterns = [
    # Clients
    path("client/", client.clients, name="clients"),
    path("create_client/", client.create_client, name="create_client"),
    path("show_clients/", client.show_clients, name="show_clients"),
    path("update_client/", client.update_client, name="update_client"),
    path("update_client/<int:id_client>", client.update_client, name="update_client"),
    path("delete_client/<int:id_client>", client.delete_client, name="delete_client"),
    path("get/ajax/validate_client", client.validate_client, name="validate_client"),
    # Servers
    path("server/", server.servers, name="servers"),
    path("create_server/", server.create_server, name="create_server"),
    path("show_servers/", server.show_servers, name="show_servers"),
    path("delete_server/<int:id_server>", server.delete_server, name="delete_server"),
    path("update_server/<int:id_server>", server.update_server, name="update_server"),
    path(
        "service/",
        service.show_service_by_server,
        name="show_service_by_server",
    ),
    path("get/ajax/validate_server", server.validate_server, name="validate_server"),
    # Services
    path("create_service/", service.create_service, name="create_service"),
    path("show_all_service/", service.show_all_service, name="show_all_service"),
]
