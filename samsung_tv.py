import base64
import socket
import time
import sys

def string_additive(string, raw=False):
    if isinstance(string, str):
        string = str.encode(string)
    if not raw:
        string = base64.b64encode(string)
    return bytes([len(string)]) + b"\x00" + string


"""retornamos la longitud de la string + un espaciador + la string, 
    la cual, si es de configuracion debemos de mandar en base64, el paquete quedaria algo como: 
    header(\x00\x00\x00) + length(payload) + payload((length(b64(descripcion)) + \x00 + b64(descripcion)), (length(b64(id)) + \x00 + b64(id)), (length(b64(name)) + \x00 + b64(name) + \x00))"""
global config
config = {
    "name": "aa",
    "descripcion": "ps",
    "id": "",
    "host": sys.argv[1],
    "port": 55000
}
def leer_con(comandos=False):
    header = connection.recv(3)
    nombre_television = connection.recv(int.from_bytes(header[1:3], byteorder="little"))
    print("Nos estamos conectando a ", nombre_television)
    response_len = int.from_bytes(connection.recv(2), byteorder="little")
    response = connection.recv(response_len)
    if comandos:
        return response
    if len(response) == 0:
        print("El host no ha enviado respuesta (Conexion finalizada)")
    if response == b"\x64\x00\x01\x00":
        print("Control cedido :)")
        comandos_tv()
    elif response == b"\x64\x00\x00\x00":
        print("Acceso denegado :(")
        return True
    elif response[0:1] == b"\x0a":
        print("Esperando al host...")
        leer_con()
    elif response[0:1] == b"\x65":
        print("Se ha cerrado el dialogo ._.")
        return True
    return response
def comandos_tv():
    while True:
        try:
            key = input("Consola -> ")
            payload = b"\x00\x00\x00" + string_additive(key)
            packet = b"\x00\x00\x00" + string_additive(payload, True)
            print("Enviando: %s", key)
            connection.send(packet)
            response = leer_con(True)
            print(response)
            print("Stroke mandado...")
        except key == "exit" or key == "Exit":
            exit("Sesion Consola cerrada")
def llamar():
    payload = b"\x64\x00" \
              + string_additive(config["descripcion"]) \
              + string_additive(config["id"]) \
              + string_additive(config["name"])
    packet = b"\x00\x00\x00" + string_additive(payload, True)
    connection.send(packet)
    leer_con()
while True:
    config["port"] = 55000
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((config["host"], config["port"]))
    llamar(config)
    time.sleep(3)

