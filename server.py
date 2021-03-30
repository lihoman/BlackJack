import socket
import json
from GameRound import *


def write_in_log(info):
    with open('server_info.log', 'a') as f:
        f.write(info + '\n')


def info_in_json(info):
    info = json.dumps(info)
    return info.encode('utf-8')


def info_from_json(info):
    return json.loads(info.decode('utf-8'))


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
server.bind(('', 10000))
server.listen(1)

client_sock, client_address = server.accept()

write_in_log(f'Client {client_address[0]} connected')

while True:
    player_name = info_from_json(client_sock.recv(1024))  # receive info about client name
    game = GameRound(player_name)  # create player and dealer
    client_sock.send(info_in_json(game.player.count))  # send info about how much money client has
    player_rate = info_from_json(client_sock.recv(1024))  # receive info about client's rate

    game.player.my_cards = game.player.generate_start_cards()  # start cards for client
    player_card_1_suit, player_card_1_value = game.player.my_cards[0].suit, game.player.my_cards[0].value
    player_card_2_suit, player_card_2_value = game.player.my_cards[1].suit, game.player.my_cards[1].value
    game.player_result = game.player.finish_result()  # view in number what sum of cards client has
    client_sock.send(info_in_json((player_card_1_suit, player_card_1_value,
                                   player_card_2_suit, player_card_2_value,
                                   game.player_result)))  # send this info
    while True:
        answer = info_from_json(client_sock.recv(1024))
        if answer != 'Y':
            break
        game.player_result = game.one_more_card(player_name, answer)
        new_card_suit = game.player.my_cards[-1].suit
        new_card_value = game.player.my_cards[-1].value
        client_sock.send(info_in_json((new_card_suit, new_card_value, game.player_result)))

    game.dealer.my_cards = game.dealer.generate_start_cards()
    dealer_card_1_suit, dealer_card_1_value = game.dealer.my_cards[0].suit, game.dealer.my_cards[0].value
    dealer_card_2_suit, dealer_card_2_value = game.dealer.my_cards[1].suit, game.dealer.my_cards[1].value
    game.dealer_result = game.dealer.finish_result()
    client_sock.send(info_in_json((dealer_card_1_suit, dealer_card_1_value,
                                   dealer_card_2_suit, dealer_card_2_value,
                                   game.dealer_result)))
    client_sock.recv(1024)
    while game.dealer_result <= 17:
        game.dealer_result = game.one_more_card(game.dealer.name, 'Y')
        new_card_suit, new_card_value = game.dealer.my_cards[-1].suit, game.dealer.my_cards[-1].value
        client_sock.send(info_in_json((new_card_suit, new_card_value, game.dealer_result)))
        client_sock.recv(1024)
    client_sock.send(info_in_json("End dealer's game"))

    client_sock.recv(1024)
    if game.player_result <= 21 and game.dealer_result <= 21:
        game_result = game.compare_results(game.player_result, game.dealer_result)
        game.player.get_rate(player_rate, game_result)
        client_sock.send(info_in_json((game_result, game.player.count)))
    else:
        game_result = game.compare_results(game.dealer_result, game.player_result)
        game.player.get_rate(player_rate, game_result)
        client_sock.send(info_in_json((game_result, game.player.count)))

# client_sock.close()
