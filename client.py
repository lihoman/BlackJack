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
    player_name = input('Welcome in BlackJack. What is your name?: ')  # give info about client
    sock_client.send(info_in_json(player_name))  # sending client name to server to create a player
    player_count = info_from_json(sock_client.recv(1024))  # receive info about client count in game
    print(player_count)
    player_rate = input("Please, make your bet: ")  # client rate in game
    sock_client.send(info_in_json(player_rate))  # sending info about client rate to server
    player_cards = info_from_json(sock_client.recv(1024))  # receive info what cards has client
    player_result = info_from_json(sock_client.recv(1024))
    print(player_cards, f'{player_name} result: {player_result}', sep='\n')

# sock_client.close()
