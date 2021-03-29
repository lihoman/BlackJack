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
    card_1_suit = game.player.my_cards[0].suit
    card_1_value = game.player.my_cards[0].value
    card_2_suit = game.player.my_cards[1].suit
    card_2_value = game.player.my_cards[1].value
    game.player_result = game.player.finish_result()  # view in number what sum of cards client has
    client_sock.send(info_in_json(card_1_suit, card_1_value, card_2_suit, card_2_value))  # send this info
    client_sock.send(info_in_json(game.player_result))
    while True:
        answer = info_from_json(client_sock.recv(1024))
        game.player_result = game.one_more_card(player_name, answer)
        new_card_suit = game.player.my_cards[-1].suit
        new_card_value = game.player.my_cards[-1].value
        client_sock.send(info_in_json(new_card_suit, new_card_value, game.player_result))


# client_sock.close()
