import ipaddress
from administration.models import Server, Client, Service


def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return None


def server_filter(id_server: int):
    server = (
        Server.objects.filter(id=id_server)
        .values("name_server", "ip_server", "client__name_client", "id", "client__nit")
        .first()
    )
    data = {
        "nameServer": server["name_server"],
        "ip_server": server["ip_server"],
        "id": server["id"],
        "nameClient": server["client__name_client"],
        "nit": server["client__nit"],
    }
    return data


def service_filter(id_service: int):
    service = (
        Service.objects.filter(id=id_service)
        .values(
            "name_service",
            "capacity",
            "id",
            "server__ip_server",
            "percent",
            "server__name_server",
        )
        .first()
    )

    data = {
        "nameService": service["name_service"],
        "capacity": service["capacity"],
        "id": service["id"],
        "percent": service["percent"],
        "ip_server": service["server__ip_server"],
        "nameServer": service["server__name_server"],
    }
    return data
