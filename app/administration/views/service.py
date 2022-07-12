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
            "services/show_service_by_server.html",
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


@login_required
@api_view(["GET", "POST"])
def create_service(request):
    context = {}
    if request.method == "GET":
        return render(request, "services/create_service.html")
    name_service = request.POST["nameService"]
    capacity = request.POST["capacity"]
    percent = request.POST["percent"]
    ip_server = request.POST["ipServer"]
    server = Server.objects.filter(ip_server=ip_server)
    new_service = Service.objects.create(
        name_service=name_service,
        capacity=capacity,
        percent=percent,
        server_id=server.get().id,
    )
    new_service.save()
    context["msj"] = "Servicio creado correctamente"
    context["alert"] = "success"

    return render(request, "services/create_service.html", {"context": context})


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
