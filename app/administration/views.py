from django.template import RequestContext
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view

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
    return render(request, "clients/create_client.html")
