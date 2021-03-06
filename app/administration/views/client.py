from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from administration.models import Client
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
@api_view(["GET"])
def clients(request):
    return render(request, "clients/clients.html")


def validate_client(request):
    if request.is_ajax and request.method == "GET":
        nit = request.GET.get("nit", None)

        client: Client = Client.objects.get(nit=nit)

        if not client:
            return JsonResponse({}, status=400)

        return JsonResponse({"nombre_cliente": client.name_client}, status=200)


@login_required
@api_view(["GET"])
def show_clients(request):
    clients = Client.objects.all()
    clients = [
        {"nombre": i.name_client, "nit": i.nit, "id": i.id, "correo": i.email}
        for i in clients
    ]
    return render(request, "clients/show_clients.html", {"data": clients})


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
    # Validate correo
    correo = request.POST["email"]
    client = Client.objects.filter(email=correo)
    if client:
        context[
            "msj"
        ] = "Ya se encuentra un cliente con ese correo, por lo tanto no se crea"
        context["alert"] = "danger"
        return render(request, "clients/create_client.html", {"context": context})
    # Validacion nit
    if len(nit) > 9:
        context["msj"] = "El nit no puede tener mas de 9 digitos"
        context["alert"] = "danger"
        return render(request, "clients/create_client.html", {"context": context})

    new_client = Client.objects.create(name_client=nombre, nit=nit, email=correo)
    new_client.save()

    context["msj"] = "Cliente creado correctamente"
    context["alert"] = "success"

    return render(request, "clients/create_client.html", {"context": context})


@login_required
@api_view(["GET", "POST"])
def update_client(request, id_client=None):
    client = Client.objects.filter(id=id_client).first()
    data = {
        "nameClient": client.name_client,
        "nit": client.nit,
        "id": client.id,
        "email": client.email,
    }
    if request.method == "GET":
        return render(
            request,
            "clients/update_client.html",
            data,
        )
    nit = request.POST["nit"]
    correo = request.POST["email"]
    if len(nit) > 9:
        data["msj"] = "El nit no puede tener mas de 9 digitos"
        data["alert"] = "danger"
        return render(request, "clients/update_client.html", data)

    # Validate nit
    if client.nit != nit:
        val_client = Client.objects.filter(nit=nit)
        if val_client:
            data[
                "msj"
            ] = "Ya se encuentra un cliente con ese nit por lo tanto no se actualiza"
            data["alert"] = "danger"
            return render(request, "clients/update_client.html", data)
    # Validate correo
    if client.email != correo:
        val_client = Client.objects.filter(email=correo)
        if val_client:
            data[
                "msj"
            ] = "Ya se encuentra un cliente con ese correo por lo tanto no se actualiza"
            data["alert"] = "danger"
            return render(request, "clients/update_client.html", data)
    client.nit = nit
    client.email = correo
    client.name_client = request.POST["nameClient"]
    client.save()

    return redirect("show_clients")


@login_required
@api_view(["GET"])
def delete_client(request, id_client=None):
    client = Client.objects.filter(id=id_client).first()
    if request.method == "GET":
        client.delete()
        return redirect("show_clients")
