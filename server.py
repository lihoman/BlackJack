import socket
import json
from GameRound import GameRound

def write_in_log(info):
    with open('server_info.log', 'a') as f:
        f.write(info + '\n')


def info_in_json(*info):
    info = json.dumps(info)
    return info.encode('utf-8')


def info_from_json(info):
    info = json.loads(info.decode('utf-8'))
    return info


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
server.bind(('', 10000))
server.listen(1)

client_sock, client_addr = server.accept()

write_in_log(f'Client {client_addr[0]} connected')

while True:
    pass
