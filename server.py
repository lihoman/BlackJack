import socket
import json
from GameRound import *


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
    player_name = info_from_json(client_sock.recv(1024))  # receive info about client name
    game = GameRound(player_name)  # create player and dealer
    client_sock.send(info_in_json(game.player.count))  # send info about how much money client has
    player_rate = info_from_json(client_sock.recv(1024))  # receive info about client's rate
    game.player.my_cards = game.player.generate_start_cards()  # start cards for client
    game.player_result = game.player.finish_result()  # view in number what sum of cards client has
    client_sock.send(info_in_json(game.player.my_cards))  # send this info
    client_sock.send(info_in_json(game.player_result))

# client_sock.close()
