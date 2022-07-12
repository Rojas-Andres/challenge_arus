from django.core.management.base import BaseCommand

from administration.models import Service
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Este script se encarga de enviar correos a los clientes los cuales un servicio esta por encima del umbral
        """

        print("===============================================================")
        print("=============== Starting send emails       ====================")
        print("===============================================================")
        services = Service.objects.values(
            "name_service",
            "capacity",
            "id",
            "server__ip_server",
            "percent",
            "use",
            "server__name_server",
            "server__client__email",
        ).all()

        for service in services:
            umbral = (service["capacity"] * service["percent"]) / 100
            # print("este es el umbral -> ", umbral, " y este es el uso ", service["use"])
            if service["use"] > umbral:
                msj = f"""El servicio {service["name_service"]} que pertenece a la direccion IP {service["server__ip_server"]} supero el umbral establecido , tiene un uso de {service["use"]} y el umbral es {umbral}"""
                sbj = f"""Servicio {service["name_service"]} del servidor {service["server__ip_server"]} supero el umbral"""
                try:
                    send_mail(
                        subject=sbj,
                        message=msj,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[service["server__client__email"]],
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Se ha enviado el correo a {service['server__client__email']} correctamente"
                        )
                    )
                except Exception as e:
                    self.stderr.write(
                        f" fallo enviando correo a {service['server__client__email']} ",
                    )

        print("===============================================================")
        print("===============     Finished send emails   ====================")
        print("===============================================================")
