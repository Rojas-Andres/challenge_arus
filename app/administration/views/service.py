from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Server, Client
from django.contrib.auth.decorators import login_required
from administration.utils import validate_ip_address


@login_required
@api_view(["GET"])
def servers(request):
    return render(request, "servers/servers.html")


@login_required
@api_view(["GET"])
def show_services(request):
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
def create_service(request):
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


# @login_required
# @api_view(["GET", "POST"])
# def update_client(request, id_client=None):
#     client = Client.objects.filter(id=id_client).first()
#     data = {"nameClient": client.name_client, "nit": client.nit, "id": client.id}
#     if request.method == "GET":
#         return render(
#             request,
#             "clients/update_client.html",
#             data,
#         )
#     nit = request.POST["nit"]
#     if len(nit) > 9:
#         data["msj"] = "El nit no puede tener mas de 9 digitos"
#         data["alert"] = "danger"
#         return render(request, "clients/update_client.html", data)
#     client.nit = nit
#     client.name_client = request.POST["nameClient"]
#     client.save()

#     return redirect("show_clients")
