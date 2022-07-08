from django.db import models


class Client(models.Model):
    name_client = models.CharField(verbose_name="Nombre", max_length=255)
    nit = models.CharField(verbose_name="Nit", max_length=255, unique=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    @classmethod
    def get_by_id(cls, uid):
        return Client.objects.get(id=uid)
