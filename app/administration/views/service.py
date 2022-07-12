from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Server, Client, Service
from django.contrib.auth.decorators import login_required
from administration.utils import validate_ip_address
from django.http import JsonResponse
from administration.serializers import ServiceSerializer


@login_required
@api_view(["GET", "POST"])
def show_service_by_server(request):
    if "GET" == request.method:
        context = {}
        return render(
            request,
            "service/show_service_by_server.html",
        )
    else:
        ip_server = request.data["ip_server"]
        server = Server.objects.filter(ip_server=ip_server).get()
        services = Service.objects.filter(server_id=server.id)
        serializer_context = {
            "request": request,
        }
        serializer = ServiceSerializer(services, many=True, context=serializer_context)
        print(serializer.data)
        return JsonResponse({"data": serializer.data})


# Falta crear la peticion para validar si la ip del servidor existe


# @login_required
# @api_view(["GET", "POST"])
# def create_service(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, "servers/create_server.html")
#     nit = request.POST["nit"]
#     nombre = request.POST["nameServer"]
#     ip = request.POST["ip"]
#     validate_ip = validate_ip_address(ip)
#     if not validate_ip:
#         context["msj"] = f"La ip {ip} no es valida"
#         context["alert"] = "danger"
#         return render(request, "servers/create_server.html", {"context": context})

#     # Validar que no exista otra ip
#     server = Server.objects.filter(ip_server=ip)
#     if server:
#         context["msj"] = f"Ya se encuentra un servidor con esa ip"
#         context["alert"] = "danger"
#         return render(request, "servers/create_server.html", {"context": context})

#     client = Client.objects.filter(nit=nit).get()
#     new_server = Server.objects.create(
#         name_server=nombre, ip_server=ip, client_id=client.id
#     )
#     new_server.save()
#     context["msj"] = "Cliente creado correctamente"
#     context["alert"] = "success"

#     return render(request, "clients/create_client.html", {"context": context})


# # @login_required
# # @api_view(["GET", "POST"])
# # def update_client(request, id_client=None):
# #     client = Client.objects.filter(id=id_client).first()
# #     data = {"nameClient": client.name_client, "nit": client.nit, "id": client.id}
# #     if request.method == "GET":
# #         return render(
# #             request,
# #             "clients/update_client.html",
# #             data,
# #         )
# #     nit = request.POST["nit"]
# #     if len(nit) > 9:
# #         data["msj"] = "El nit no puede tener mas de 9 digitos"
# #         data["alert"] = "danger"
# #         return render(request, "clients/update_client.html", data)
# #     client.nit = nit
# #     client.name_client = request.POST["nameClient"]
# #     client.save()

# #     return redirect("show_clients")
