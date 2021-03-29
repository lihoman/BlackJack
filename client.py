import socket
import json
from Cards import *


def info_from_json(json_info):
    python_format = json.loads(json_info.decode('utf-8'))
    return python_format


def info_in_json(*info):
    info = json.dumps(info)
    return info.encode('utf-8')


sock_client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
sock_client.connect(('localhost', 10000))

while True:
    pass



# sock_client.close()
