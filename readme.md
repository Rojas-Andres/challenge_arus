Crear un superusuario para iniciar sesion
python manage.py createsuperuser

# Validaciones

## Cliente
- El nit no puede estar repetido
- EL nit no puede tener una longitud mayor a 9 

## Server
    - Validacion de ip


## Ejemplos de ip validas

validate_ip_address("10.10.10.10")
validate_ip_address("10.10.10.01")
validate_ip_address("10.10.10.300")
validate_ip_address("10.260.10.300")
validate_ip_address("192.168.1.20")

[output]
IP address 10.10.10.10 is valid. la funcion retorna True
IP address 10.10.10.01 is valid. la funcion retorna True
IP address 10.10.10.300 ,la funcion retorna False
IP address 10.260.10.300 ,la funcion retorna False
IP address 192.168.1.20 is valid. la funcion retorna True 