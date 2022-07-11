import ipaddress
from administration.models import Server, Client


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
