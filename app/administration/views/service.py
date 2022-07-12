from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Server, Client, Service
from django.contrib.auth.decorators import login_required
from administration.utils import validate_ip_address, service_filter
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


@login_required
@api_view(["GET"])
def show_all_service(request):
    services = Service.objects.all().values(
        "name_service", "capacity", "percent", "id", "server__ip_server"
    )
    services = [
        {
            "nombre": i["name_service"],
            "capacidad": i["capacity"],
            "porcentaje": i["percent"],
            "id": i["id"],
            "ip_server": i["server__ip_server"],
        }
        for i in services
    ]
    return render(request, "services/show_all_services.html", {"data": services})


# Falta implementar el comando que ejecuta las validaciones


@login_required
@api_view(["GET", "POST"])
def update_service(request, id_service=None):

    if request.method == "GET":
        data_service = service_filter(id_service)
        return render(
            request,
            "services/update_service.html",
            data_service,
        )
    # Obtener id server
    ip_server = request.POST["ipServer"]
    server = Server.objects.filter(ip_server=ip_server)
    service = Service.objects.filter(id=id_service).get()
    service.name_service = request.POST["nameService"]
    service.capacity = request.POST["capacity"]
    service.percent = request.POST["percent"]
    service.server_id = server.get().id
    service.save()

    return redirect("servers")
