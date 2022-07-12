from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Server, Client
from django.contrib.auth.decorators import login_required
from administration.utils import validate_ip_address, server_filter
from django.http import JsonResponse


@login_required
@api_view(["GET"])
def servers(request):
    return render(request, "servers/servers.html")


@login_required
@api_view(["GET"])
def show_servers(request):
    servers = Server.objects.all().values(
        "name_server", "ip_server", "client__name_client", "id"
    )
    servers = [
        {
            "nombre": i["name_server"],
            "ip": i["ip_server"],
            "cliente": i["client__name_client"],
            "id": i["id"],
        }
        for i in servers
    ]
    return render(request, "servers/show_servers.html", {"data": servers})


@login_required
@api_view(["GET", "POST"])
def create_server(request):
    context = {}
    if request.method == "GET":
        return render(request, "servers/create_server.html")
    nit = request.POST["nit"]
    nombre = request.POST["nameServer"]
    ip = request.POST["ip"]
    validate_ip = validate_ip_address(ip)
    if not validate_ip:
        context["msj"] = f"La ip {ip} no es valida"
        context["alert"] = "danger"
        return render(request, "servers/create_server.html", {"context": context})

    # Validar que no exista otra ip
    server = Server.objects.filter(ip_server=ip)
    if server:
        context["msj"] = f"Ya se encuentra un servidor con esa ip"
        context["alert"] = "danger"
        return render(request, "servers/create_server.html", {"context": context})

    client = Client.objects.filter(nit=nit).get()
    new_server = Server.objects.create(
        name_server=nombre, ip_server=ip, client_id=client.id
    )
    new_server.save()
    context["msj"] = "Cliente creado correctamente"
    context["alert"] = "success"

    return render(request, "clients/create_client.html", {"context": context})


def validate_server(request):
    if request.is_ajax and request.method == "GET":
        ip_server = request.GET.get("ipServer", None)

        server: Server = Server.objects.filter(ip_server=ip_server)

        if not server:
            return JsonResponse({}, status=400)

        return JsonResponse({"nombre_servidor": server.get().name_server}, status=200)


@login_required
@api_view(["GET", "POST"])
def update_server(request, id_server=None):
    context = {}
    data_last_server = server_filter(id_server)
    if request.method == "GET":

        return render(
            request,
            "servers/update_server.html",
            data_last_server,
        )

    server = Server.objects.filter(id=id_server).get()
    # Validar ip
    ip = request.POST["ip"]
    validate_ip = validate_ip_address(ip)
    if not validate_ip:
        data_last_server["msj"] = f"La ip {ip} no es valida"
        data_last_server["alert"] = "danger"
        return render(
            request,
            "servers/update_server.html",
            data_last_server,
        )

    # Validar que la ip que va actualizar no exista

    if ip != server.ip_server:
        server_ip = Server.objects.filter(ip_server=ip)
        if server_ip:
            data_last_server["msj"] = f"Ya se encuentra un servidor con esa ip"
            data_last_server["alert"] = "danger"
            return render(
                request,
                "servers/update_server.html",
                data_last_server,
            )
    nit = request.POST["nit"]
    client = Client.objects.filter(nit=nit).get()
    server.name_server = request.POST["nameServer"]
    server.ip_server = ip
    server.client_id = client.id
    server.save()

    return redirect("show_servers")


@login_required
@api_view(["GET"])
def delete_server(request, id_server=None):
    server = Server.objects.filter(id=id_server).first()
    if request.method == "GET":
        server.delete()
        return redirect("show_servers")
