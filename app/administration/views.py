from django.template import RequestContext
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Client
from django.contrib.auth.decorators import login_required


def Index(request):
    return render(request, "registration/index.html", {})


@login_required
@api_view(["GET"])
def clients(request):
    return render(request, "clients/clients.html")


@login_required
@api_view(["GET", "POST"])
def create_client(request):
    context = {}
    if request.method == "GET":
        return render(request, "clients/create_client.html")

    nit = request.POST["nit"]
    nombre = request.POST["nameClient"]
    client = Client.objects.filter(nit=nit)
    if client:
        context[
            "msj"
        ] = "Ya se encuentra un cliente con ese NIT, por lo tanto no se crea"
        context["alert"] = "danger"
        return render(request, "clients/create_client.html", {"context": context})

    if len(nit) > 9:
        context["msj"] = "El nit no puede tener mas de 9 digitos"
        context["alert"] = "danger"
        return render(request, "clients/create_client.html", {"context": context})

    new_client = Client.objects.create(name_client=nombre, nit=nit)
    new_client.save()

    context["msj"] = "Cliente creado correctamente"
    context["alert"] = "success"

    return render(request, "clients/create_client.html", {"context": context})
