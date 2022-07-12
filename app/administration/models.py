from django.db import models


class Client(models.Model):
    name_client = models.CharField(verbose_name="Nombre", max_length=255)
    nit = models.CharField(verbose_name="Nit", max_length=9, unique=True)
    email = models.CharField(verbose_name="Correo", max_length=255, unique=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    @classmethod
    def get_by_id(cls, uid):
        return Client.objects.get(id=uid)


class Server(models.Model):
    ip_server = models.CharField(
        verbose_name="Ip servidor", max_length=255, unique=True
    )
    name_server = models.CharField(verbose_name="Nombre Servidor", max_length=255)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"

    @classmethod
    def get_by_id(cls, uid):
        return Server.objects.get(id=uid)


class Service(models.Model):
    name_service = models.CharField(verbose_name="Nombre servicio", max_length=255)
    capacity = models.IntegerField()
    percent = models.IntegerField(default=0)

    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    @classmethod
    def get_by_id(cls, uid):
        return Service.objects.get(id=uid)
