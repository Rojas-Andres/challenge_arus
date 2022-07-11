from django.shortcuts import render


def Index(request):
    return render(request, "registration/index.html", {})
