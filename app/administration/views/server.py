from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Server
from django.contrib.auth.decorators import login_required


@login_required
@api_view(["GET"])
def servers(request):
    return render(request, "servers/servers.html")


@login_required
@api_view(["GET"])
def show_servers(request):
    servers = Server.objects.all()
    servers = [
        {"nombre": i.name_server, "ip": i.ip_server, "cliente": "a"} for i in servers
    ]
    return render(request, "servers/show_servers.html", {"data": servers})


@login_required
@api_view(["GET", "POST"])
def create_server(request):
    context = {}
    if request.method == "GET":
        return render(request, "servers/create_server.html")


#     nit = request.POST["nit"]
#     nombre = request.POST["nameClient"]
#     client = Client.objects.filter(nit=nit)
#     if client:
#         context[
#             "msj"
#         ] = "Ya se encuentra un cliente con ese NIT, por lo tanto no se crea"
#         context["alert"] = "danger"
#         return render(request, "clients/create_client.html", {"context": context})

#     if len(nit) > 9:
#         context["msj"] = "El nit no puede tener mas de 9 digitos"
#         context["alert"] = "danger"
#         return render(request, "clients/create_client.html", {"context": context})

#     new_client = Client.objects.create(name_client=nombre, nit=nit)
#     new_client.save()

#     context["msj"] = "Cliente creado correctamente"
#     context["alert"] = "success"

#     return render(request, "clients/create_client.html", {"context": context})


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


# @login_required
# @api_view(["GET"])
# def delete_client(request, id_client=None):
#     client = Client.objects.filter(id=id_client).first()
#     if request.method == "GET":
#         client.delete()
#         return redirect("show_clients")
